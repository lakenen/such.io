from decimal import Decimal
from django.db import models


class CoinAmountField(models.DecimalField):
    MAX_DIGITS = 16
    DECIMAL_PLACES = 8

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = self.__class__.MAX_DIGITS
        kwargs['decimal_places'] = self.__class__.DECIMAL_PLACES
        kwargs['default'] = Decimal('0.0')
        super(CoinAmountField, self).__init__(*args, **kwargs)
