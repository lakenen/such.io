from django.contrib import admin

from .models import Market, Order

class MarketAdmin(admin.ModelAdmin):
    list_display = ['base_currency', 'market_currency']
admin.site.register(Market, MarketAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'market', 'type', 'status', 'amount', 'rate', 'filled_amount', 'filled_rate', 'is_partial', 'ordered_at']
admin.site.register(Order, OrderAdmin)
