from rest_framework.routers import DefaultRouter
from .views import BannerViewSet

router = DefaultRouter()
router.register("", BannerViewSet, basename="banner")

urlpatterns = router.urls
