from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, CoinAmountField


class Market(models.Model):
    base_currency = models.ForeignKey('core.Currency', related_name='+')
    market_currency = models.ForeignKey('core.Currency', related_name='+')

    def __unicode__(self):
        return '<%s: %s/%s>' % (self.__class__.__name__, self.base_currency.symbol, self.market_currency.symbol)


class Order(TimeStampedModel):
    class TYPE:
        BUY         = 1
        SELL        = 2
    TYPE_CHOICES = [(TYPE.__dict__[name], name) for name in dir(TYPE) if not name.startswith('_')]

    class STATUS:
        OPEN        = 1
        FILLED      = 2
        CANCELLED   = 3
    STATUS_CHOICES = [(STATUS.__dict__[name], name) for name in dir(STATUS) if not name.startswith('_')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    market = models.ForeignKey('Market')
    status = models.IntegerField(choices=STATUS_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES)
    is_partial = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(auto_now_add=True)
    filled_at = models.DateTimeField(null=True, blank=True)
    cancel_requested_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
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

    def clone(self):
        kwargs = {}
        for field in self._meta.fields:
            if field != self._meta.pk:
                kwargs[field.name] = getattr(self, field.name)
        return self.__class__(**kwargs)