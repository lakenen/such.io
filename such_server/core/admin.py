from django.contrib import admin

from .models import UserProfile, Currency, Balance, Transaction


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(UserProfile, UserProfileAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']
admin.site.register(Currency, CurrencyAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'cleared_amount']
admin.site.register(Balance, BalanceAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'address', 'tx_id', 'amount', 'is_cleared']
admin.site.register(Transaction, TransactionAdmin)
