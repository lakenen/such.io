from django.db import transaction
from django.db.models import F
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.models import Balance
from .models import Order, Market
from .serializers import OrderInputSerializer, OrderOutputSerializer
from .serializers import MarketOutputSerializer
from .tasks import clear_market


class MarketViewSet(ViewSet):
    model = Market
    permission_classes = [AllowAny]

    def list(self, reqeust):
        markets = Market.objects.filter()
        output_serializer = MarketOutputSerializer(markets, many=True)
        return Response(output_serializer.data)

    def retrieve(self, request, pk=None):
        try:
            market = Market.objects.get(id=int(pk))
        except Market.DoesNotExist:
            return Response({'error': 'market not found'}, status=status.HTTP_404_NOT_FOUND)

        output_serializer = MarketOutputSerializer(market)
        return Response(output_serializer.data)


class OrderViewSet(ViewSet):
    model = Order

    def list(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-modified_at')
        output_serializer = OrderOutputSerializer(orders, many=True)
        return Response(output_serializer.data)

    def create(self, request):
        context = {
            'request': request,
        }

        serializer = OrderInputSerializer(
                data=request.DATA,
                context=context
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():

            order = serializer.object
            order.save()

            _, sell_currency = order.get_buy_and_sell_currencies()
            _, sell_amount = order.get_buy_and_sell_amounts()

            balance = Balance.objects.get(user=order.user, currency=sell_currency)

            balance_query = Balance.objects.filter(id=balance.id, amount__gte=sell_amount)
            num_updated = balance_query.update(amount=F('amount') - sell_amount)

            if num_updated != 1:
                raise Exception('updated %d rows when placing order %s' % (num_updated, order))

        #TODO fire this asynchronously
        clear_market(order.market_id)

        output_serializer = OrderOutputSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(user=request.user, id=int(pk))
        except Order.DoesNotExist:
            return Response({'error': 'order does not exist'}, status=status.HTTP_404_NOT_FOUND)


        num_updated = Order.objects.filter(
                id=int(pk),
                status=Order.STATUS.OPEN,
                cancel_requested_at__isnull=True
        ).update(cancel_requested_at=now())

        if num_updated == 1:
            clear_market(order.market_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif num_updated == 0:
            return Response({'error': 'cannot cancel this order'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception('updated %d rows when requesting cancel for order %s' % (num_updated, order.id))
