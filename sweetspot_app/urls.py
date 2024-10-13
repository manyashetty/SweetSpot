from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CakeViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'cakes', CakeViewSet)

urlpatterns = router.urls
