from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``modified_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True

    def save(self, *args, **kwargs):
        if 'update_fields' in kwargs:
            kwargs['update_fields'] = list(kwargs['update_fields']) + ['modified_at']
        super(TimeStampedModel, self).save(*args, **kwargs)


class CoinAmountField(models.DecimalField):
    MAX_DIGITS = 16
    DECIMAL_PLACES = 8

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = self.__class__.MAX_DIGITS
        kwargs['decimal_places'] = self.__class__.DECIMAL_PLACES
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, **kwargs):
    user = kwargs['instance']

    # disable for loaddata/fixtures
    if kwargs['raw']:
        return

    # only create user profile if the user is being created
    if not kwargs['created']:
        return

    #TODO log an error if this fails
    UserProfile.objects.create(user=user)
