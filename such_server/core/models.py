from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .fields import CoinAmountField


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


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile')


class Currency(models.Model):
    name = models.CharField(max_length=32)
    symbol = models.CharField(max_length=4, unique=True)
    min_confirmations = models.IntegerField()

    def is_enough_confirmations(self, confirmations):
        return confirmations >= self.min_confirmations

    def __unicode__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.symbol)


class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    currency = models.ForeignKey('Currency')
    amount = CoinAmountField()

    def __unicode__(self):
        return '<%s: %s %s %s>' % (self.__class__.__name__, self.user.email, self.amount, self.currency.symbol)


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
