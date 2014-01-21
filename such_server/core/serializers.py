from rest_framework import serializers

from . import fields
from .models import Currency, Balance


class CoinAmountField(serializers.DecimalField):
    def __init__(self, value='', **kwargs):
        kwargs['max_digits'] = fields.CoinAmountField.MAX_DIGITS
        kwargs['decimal_places'] = fields.CoinAmountField.DECIMAL_PLACES
        super(CoinAmountField, self).__init__(value, **kwargs)


class CurrencyOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ['id', 'min_confirmations']


class BalanceOutputSerializer(serializers.ModelSerializer):
    currency = CurrencyOutputSerializer()

    class Meta:
        model = Balance
        exclude = ['id', 'user']
        depth = 2
