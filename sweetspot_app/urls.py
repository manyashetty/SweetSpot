from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CakeViewSet, CakeCustomizationViewSet, CartViewSet, OrderViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'cakes', CakeViewSet)
router.register(r'cake_customizations', CakeCustomizationViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)

# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
]