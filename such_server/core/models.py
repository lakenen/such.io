from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CoinAmountField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 16
        kwargs['decimal_places'] = 8
        kwargs['default'] = Decimal('0.0')
        super(CoinAmountField, self).__init__(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile')


class Currency(models.Model):
    name = models.CharField(max_length=32)
    symbol = models.CharField(max_length=4, unique=True)

    def __unicode__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.symbol)


class Balance(models.Model):
    user = models.ForeignKey(User)
    currency = models.ForeignKey('Currency')
    cleared_amount = CoinAmountField()

    def __unicode__(self):
        return '<%s: %s %s %s>' % (self.__class__.__name__, self.user.username, self.cleared_amount, self.currency.symbol)


class Transaction(models.Model):
    class TYPE:
        DEPOSIT         = 1
        WITHDRAW        = 2
        WITHDRAW_FEE    = 4
        TRADE_FEE       = 5
    TYPE_CHOICES = [(TYPE.__dict__[name], name) for name in dir(TYPE) if not name.startswith('_')]

    type = models.IntegerField(choices=TYPE_CHOICES)
    address = models.ForeignKey('wallets.DepositAddress')
    tx_id = models.CharField(max_length=64, unique=True)
    amount = CoinAmountField()
    is_cleared = models.BooleanField(default=False)

    @classmethod
    def is_enough_confirmations(cls, confirmations):
        return confirmations >= settings.MINIMUM_CONFIRMATIONS

    def __unicode__(self):
        return '<%s: %s %s>' % (self.__class__.__name__, self.get_type_display(), self.amount)


class Exchange(models.Model):
    base_currency = models.ForeignKey('Currency', related_name='+')
    market_currency = models.ForeignKey('Currency', related_name='+')

    def __unicode__(self):
        return '<%s: %s/%s>' % (self.__class__.__name__, self.base_currency.symbol, self.market_currency.symbol)


class Order(models.Model):
    class TYPE:
        BUY         = 1
        SELL        = 2
    TYPE_CHOICES = [(TYPE.__dict__[name], name) for name in dir(TYPE) if not name.startswith('_')]

    class STATUS:
        OPEN        = 1
        FILLED      = 2
        CANCELLED   = 3
    STATUS_CHOICES = [(STATUS.__dict__[name], name) for name in dir(STATUS) if not name.startswith('_')]

    user = models.ForeignKey(User)
    exchange = models.ForeignKey('Exchange')
    status = models.IntegerField(choices=STATUS_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES)
    from_partial = models.BooleanField(default=False)
    opened_at = models.DateTimeField(auto_now_add=True)
    filled_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    amount = CoinAmountField()
    rate = CoinAmountField()
    filled_amount = CoinAmountField(null=True, blank=True)
    filled_rate = CoinAmountField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    user = kwargs['instance']

    # disable for loaddata/fixtures
    if kwargs['raw']:
        return

    # only create user profile if the User is being created
    if not kwargs['created']:
        return

    #TODO log an error if this fails
    UserProfile.objects.create(user=user)
