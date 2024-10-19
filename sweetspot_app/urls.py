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
    path('customers/login/', CustomerViewSet.as_view({'post': 'login'}), name='customer-login'),
    path('carts/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    path('orders/place_order/', OrderViewSet.as_view({'post': 'place_order'}), name='place_order'),
    
    
]