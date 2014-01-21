from rest_framework import serializers

from .models import Currency, Balance


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
