from django.conf import settings
from django.db import models
from django.db.models import Sum

from core.models import TimeStampedModel, CoinAmountField


class Market(models.Model):
    base_currency = models.ForeignKey('core.Currency', related_name='+')
    market_currency = models.ForeignKey('core.Currency', related_name='+')

    def __unicode__(self):
        return '<%s: %s/%s>' % (self.__class__.__name__, self.base_currency.symbol, self.market_currency.symbol)

    def open_orders(self):
        return self.order_set.filter(status=Order.STATUS.OPEN)

    def open_sells(self):
        return self.order_set.filter(status=Order.STATUS.OPEN, type=Order.TYPE.SELL)

    def open_buys(self):
        return self.order_set.filter(status=Order.STATUS.OPEN, type=Order.TYPE.BUY)

    def get_aggregated_open_orders(self):
        buys = self.open_buys().values('rate').annotate(amount=Sum('amount')).order_by('-rate')
        sells = self.open_sells().values('rate').annotate(amount=Sum('amount')).order_by('rate')
        return {
            'buy': buys,
            'sell': sells,
        }


class Order(TimeStampedModel):
    class TYPE:
        BUY         = 1
        SELL        = 2
    TYPE_CHOICES = [(TYPE.__dict__[name], name) for name in dir(TYPE) if not name.startswith('_')]

    class STATUS:
        OPEN        = 1
        FILLED      = 2
        CANCELED    = 3
    STATUS_CHOICES = [(STATUS.__dict__[name], name) for name in dir(STATUS) if not name.startswith('_')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    market = models.ForeignKey('Market')
    status = models.IntegerField(choices=STATUS_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES)
    is_partial = models.BooleanField(default=False)
    ordered_at = models.DateTimeField()
    filled_at = models.DateTimeField(null=True, blank=True)
    cancel_requested_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    amount = CoinAmountField()
    rate = CoinAmountField()
    filled_amount = CoinAmountField(null=True, blank=True)
    filled_rate = CoinAmountField(null=True, blank=True)

    def __unicode__(self):
        return '<%s: %s %s %s>' % (self.__class__.__name__,
                self.get_status_display(),
                self.get_type_display(),
                self.amount
        )

    def get_buy_and_sell_currencies(self):
        if self.type == Order.TYPE.BUY:
            return self.market.market_currency, self.market.base_currency
        elif self.type == Order.TYPE.SELL:
            return self.self.market.base_currency, self.market.market_currency

    def get_buy_and_sell_amounts(self):
        if self.type == Order.TYPE.BUY:
            return self.amount, self.amount * self.rate
        elif self.type == Order.TYPE.SELL:
            return self.amount * self.rate, self.amount

    def get_buy_and_sell_filled_amounts(self):
        if self.type == Order.TYPE.BUY:
            return self.filled_amount, self.filled_amount * self.filled_rate
        elif self.type == Order.TYPE.SELL:
            return self.filled_amount * self.filled_rate, self.filled_amount

    def clone(self):
        kwargs = {}
        for field in self._meta.fields:
            if field != self._meta.pk:
                kwargs[field.name] = getattr(self, field.name)
        return self.__class__(**kwargs)
