from rest_framework.routers import DefaultRouter

from core.views import BalanceViewSet
from markets.views import MarketViewSet, OrderViewSet
from wallets.views import TransactionViewSet


urlpatterns = []

router = DefaultRouter(trailing_slash=False)
router.register(r'balances', BalanceViewSet)
router.register(r'markets', MarketViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'transactions', TransactionViewSet)
urlpatterns += router.urls
