from decimal import Decimal
from django.utils.timezone import now
from rest_framework import serializers

from .models import Order, Market
from core.serializers import MethodField, CoinAmountField
from core.serializers import CurrencyOutputSerializer
from core.models import Balance


class ConstantField(serializers.Field):
    """
    A field that serializes/deserializer to/from a constant value.
    """
    def __init__(self, value='', **kwargs):
        super(ConstantField, self).__init__(**kwargs)
        self._const_value = value

    def field_from_native(self, data, files, field_name, into):
        into[field_name] = self._const_value

    def field_to_native(self, obj, field_name):
        return self.to_native(self._const_value)


class MarketOutputSerializer(serializers.ModelSerializer):
    base_currency = CurrencyOutputSerializer()
    market_currency = CurrencyOutputSerializer()
    aggregated_open_orders = serializers.Field(source='get_aggregated_open_orders')

    class Meta:
        model = Market
        depth = 2


class OrderOutputSerializer(serializers.ModelSerializer):
    market = MarketOutputSerializer()
    status = serializers.Field(source='get_status_display')
    type = serializers.Field(source='get_type_display')

    class Meta:
        model = Order
        exclude = ['id', 'user']
        depth = 2


class OrderInputSerializer(serializers.Serializer):
    user = MethodField('_get_user')
    status = ConstantField(value=Order.STATUS.OPEN)

    market = serializers.IntegerField()
    type = serializers.CharField()
    amount = CoinAmountField()
    rate = CoinAmountField()

    def _get_user(self):
        return self.context['request'].user

    def validate_market(self, attrs, source):
        market_id = attrs.pop(source)
        market = Market.objects.get(id=market_id)
        attrs['market'] = market
        return attrs

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
        if balance.amount < sell_amount:
            raise serializers.ValidationError('Insufficient funds')

        min_amount = Decimal('0.00000001')
        if buy_amount < min_amount or sell_amount < min_amount:
            raise serializers.ValidationError('Order is too small')

        return attrs

    def restore_object(self, attrs, instance=None):
        attrs['ordered_at'] = now()
        order = Order(**attrs)
        return order
