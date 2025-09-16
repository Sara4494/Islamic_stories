from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, dashboard_stats

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("stats/", dashboard_stats, name="dashboard-stats"),
]

urlpatterns += router.urls
