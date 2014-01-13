from django.contrib import admin

from .models import UserProfile, Currency, Balance


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(UserProfile, UserProfileAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']
admin.site.register(Currency, CurrencyAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'amount']
admin.site.register(Balance, BalanceAdmin)
