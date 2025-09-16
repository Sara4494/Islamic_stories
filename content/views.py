from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Category, Story, Episode
from .serializers import CategorySerializer, StorySerializer, EpisodeSerializer
from .permissions import IsAdminOrReadOnlyForAuthenticated


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyForAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "تم إضافة القسم بنجاح 🎉", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "تم تحديث القسم ✅", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف القسم 🗑️"}, status=status.HTTP_204_NO_CONTENT)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAdminOrReadOnlyForAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "تم إضافة القصة بنجاح 🎉", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "تم تحديث القصة ✅", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف القصة 🗑️"}, status=status.HTTP_204_NO_CONTENT)


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "story__title"]
    permission_classes = [IsAdminOrReadOnlyForAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        story_id = self.request.query_params.get("story")
        if story_id:
            queryset = queryset.filter(story_id=story_id)
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "تم إضافة الحلقة بنجاح 🎉", "data": response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "تم تحديث الحلقة ✅", "data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف الحلقة 🗑️"}, status=status.HTTP_204_NO_CONTENT)

