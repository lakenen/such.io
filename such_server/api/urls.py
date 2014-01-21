from rest_framework.routers import DefaultRouter

from core.views import BalanceViewSet
from markets.views import MarketViewSet, OrderViewSet


urlpatterns = []

router = DefaultRouter(trailing_slash=False)
router.register(r'balances', BalanceViewSet)
router.register(r'markets', MarketViewSet)
router.register(r'orders', OrderViewSet)
urlpatterns += router.urls
