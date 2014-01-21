from rest_framework import serializers

from . import fields
from .models import Currency, Balance


class MethodField(serializers.Field):
    """
    A field that gets its value by calling a method on the serializer it's attached to.
    """

    def __init__(self, method_name):
        self.method_name = method_name
        super(MethodField, self).__init__()

    def field_from_native(self, data, files, field_name, into):
        value = getattr(self.parent, self.method_name)()
        into[field_name] = value

    def field_to_native(self, obj, field_name):
        value = getattr(self.parent, self.method_name)()
        return self.to_native(value)


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
    deposit_address = serializers.SerializerMethodField('_get_deposit_address')
    currency = CurrencyOutputSerializer()

    class Meta:
        model = Balance
        exclude = ['id', 'user']
        depth = 2

    def _get_deposit_address(self, obj):
        addresses = obj.depositaddress_set.all()
        if not addresses:
            return None
        return addresses[0].address
