from django.contrib import admin

from .models import Wallet, DepositAddress


class WalletAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency', 'rpc_host', 'rpc_port', 'rpc_username', 'rpc_password']
admin.site.register(Wallet, WalletAdmin)


class DepositAddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'wallet', 'balance']
admin.site.register(DepositAddress, DepositAddressAdmin)
