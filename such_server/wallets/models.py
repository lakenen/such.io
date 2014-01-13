import random
from django.db import models

from core.models import CoinAmountField


class Wallet(models.Model):
    currency = models.ForeignKey('core.Currency')
    name = models.CharField(max_length=50)
    last_cleared_tx_id = models.CharField(max_length=64, blank=True, null=True)
    rpc_host = models.CharField(max_length=64)
    rpc_port = models.SmallIntegerField()
    rpc_username = models.CharField(max_length=64)
    rpc_password = models.CharField(max_length=64)

    @classmethod
    def choose_wallet_for_user(cls, user, currency):
        """
        Chooses a random wallet for the user in the given currency.
        """

        if isinstance(currency, basestring):
            wallets = cls.objects.filter(currency_id=currency)
        else:
            wallets = cls.objects.filter(currency=currency)

        return random.choice(wallets)

    def __unicode__(self):
        return '<%s: %s host=%s:%s>' % (self.__class__.__name__, self.currency.symbol, self.rpc_host, self.rpc_port)


class Transaction(models.Model):
    class TYPE:
        DEPOSIT         = 1
        WITHDRAW        = 2
        WITHDRAW_FEE    = 4
        TRADE_FEE       = 5
    TYPE_CHOICES = [(TYPE.__dict__[name], name) for name in dir(TYPE) if not name.startswith('_')]

    type = models.IntegerField(choices=TYPE_CHOICES)
    balance = models.ForeignKey('core.Balance')
    wallet = models.ForeignKey('Wallet')
    tx_id = models.CharField(max_length=64, unique=True)
    amount = CoinAmountField()
    is_cleared = models.BooleanField(default=False)
    is_orphaned = models.BooleanField(default=False)

    def __unicode__(self):
        return '<%s: %s %s>' % (self.__class__.__name__, self.get_type_display(), self.amount)


class DepositAddress(models.Model):
    wallet = models.ForeignKey('Wallet')
    balance = models.ForeignKey('core.Balance')
    address = models.CharField(max_length=34, unique=True)

    def __unicode__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.address)
