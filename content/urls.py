from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, StoryViewSet, EpisodeViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
 
router.register("episodes", EpisodeViewSet, basename="episode")
router.register("stories", StoryViewSet, basename="story")

urlpatterns = router.urls
