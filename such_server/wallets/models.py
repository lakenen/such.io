import random
from django.db import models


class Wallet(models.Model):
    currency = models.ForeignKey('core.Currency')
    name = models.CharField(max_length=50)
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


class DepositAddress(models.Model):
    wallet = models.ForeignKey('Wallet')
    balance = models.ForeignKey('core.Balance')
    address = models.CharField(max_length=34, unique=True)

    def __unicode__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.address)
