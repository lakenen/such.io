from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Transaction
from .serializers import TransactionOutputSerializer


class TransactionViewSet(ViewSet):
    model = Transaction

    def list(self, reqeust):
        txs = Transaction.objects.filter(type__in=[Transaction.TYPE.DEPOSIT, Transaction.TYPE.WITHDRAWAL])
        output_serializer = TransactionOutputSerializer(txs, many=True)
        return Response(output_serializer.data)
