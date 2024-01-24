from django.urls import include, path
from rest_framework.routers import DefaultRouter

from supply_chain.apps import SupplyChainConfig
from supply_chain.views import NetworkEntityViewSet

app_name = SupplyChainConfig.name

router = DefaultRouter()
router.register(r'network_entity', NetworkEntityViewSet)

urlpatterns = [
    path('supply_chain/', include(router.urls)),
]
