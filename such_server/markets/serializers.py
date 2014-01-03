from decimal import Decimal
from rest_framework import serializers

from .models import Order
from core.models import Balance


class OrderOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'market', 'type', 'status', 'amount', 'rate', 'is_partial', 'filled_amount', 'filled_rate']
        depth = 2


class OrderInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order

    market = serializers.PrimaryKeyRelatedField()
    type = serializers.CharField()
    amount = serializers.DecimalField()
    rate = serializers.DecimalField()

    def validate_type(self, attrs, source):
        order_type = attrs[source].lower()

        if order_type == 'buy':
            attrs[source] = Order.TYPE.BUY
        elif order_type == 'sell':
            attrs[source] = Order.TYPE.SELL
        else:
            raise serializers.ValidationError('Order type must be "buy" or "sell".')

        return attrs

    def validate(self, attrs):
        if attrs['type'] == Order.TYPE.BUY:
            buy_amount = attrs['amount']
            sell_amount = buy_amount * attrs['rate']
            sell_currency = attrs['market'].base_currency

        elif attrs['type'] == Order.TYPE.SELL:
            sell_amount = attrs['amount']
            sell_currency = attrs['market'].market_currency
            buy_amount =  sell_amount * attrs['rate']

        else:
            raise Exception('Unexpected order type %s' % attrs['type'])

        balance = Balance.objects.get(user=attrs['user'], currency=sell_currency)
        if balance.cleared_amount < sell_amount:
            raise serializers.ValidationError('Insufficient funds')

        min_amount = Decimal('0.00000001')
        if buy_amount < min_amount or sell_amount < min_amount:
            raise serializers.ValidationError('Order is too small')

        return attrs
