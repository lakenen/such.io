from rest_framework.routers import DefaultRouter

from .views import MarketViewSet, OrderViewSet


urlpatterns = []


router = DefaultRouter(trailing_slash=False)
router.register(r'markets', MarketViewSet)
router.register(r'orders', OrderViewSet)
urlpatterns += router.urls
