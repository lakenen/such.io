from rest_framework import serializers

from core.serializers import CoinAmountField
from core.serializers import BalanceOutputSerializer
from .models import Transaction


class TransactionOutputSerializer(serializers.ModelSerializer):
    type = serializers.Field(source='get_type_display')
    balance = BalanceOutputSerializer()
    amount = CoinAmountField()

    class Meta:
        model = Transaction
        exclude = ['id', 'wallet', 'tx_id']
        depth = 2
