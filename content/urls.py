from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, StoryViewSet, EpisodeViewSet ,FavoriteStoriesView

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
 
router.register("episodes", EpisodeViewSet, basename="episode")
router.register("stories", StoryViewSet, basename="story")

router.register("favorite-stories", FavoriteStoriesView, basename="favorite-stories")


urlpatterns = router.urls
