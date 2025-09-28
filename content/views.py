from rest_framework import viewsets, status, filters ,permissions
from rest_framework.response import Response
from .models import Category, Story, Episode
from .serializers import CategorySerializer, StorySerializer, EpisodeSerializer
from .permissions import IsAdminOrReadOnlyForAuthenticated
from rest_framework.views import APIView 
from rest_framework.decorators import action
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyForAuthenticated]
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {"message": "تم جلب قائمة الاقسام بنجاح ✅", "data": response.data},
            status=status.HTTP_200_OK,
        )
 

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
    serializer_class = StorySerializer
    permission_classes = [IsAdminOrReadOnlyForAuthenticated]

    def get_queryset(self):
        queryset = Story.objects.all().order_by("-created_at")  
        category_id = self.request.query_params.get("category")  
        if category_id:
            queryset = queryset.filter(category_id=category_id).order_by("-created_at")
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {"message": "تم جلب قائمة القصص بنجاح ✅", "data": response.data},
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # ✅ زيادة العداد كل مرة القصة تتشاف
        instance.views_count = instance.views_count + 1
        instance.save(update_fields=["views_count"])

        serializer = self.get_serializer(instance)
        return Response(
            {"message": "تم جلب القصه بنجاح ✅", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "تم إضافة القصة بنجاح 🎉", "data": response.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "تم تحديث القصة ✅", "data": response.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "تم حذف القصة 🗑️"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # ✅ API إضافية للقصص الأكثر شعبية
    @action(detail=False, methods=["get"])
    def popular(self, request):
        queryset = Story.objects.all().order_by("-views_count")[:10]  # أول 10 قصص
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"message": "تم جلب القصص الأكثر شعبية 🔥", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class FavoriteStoriesView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """عرض المفضلة"""
        favorites = request.user.favorites.all()
        data = [{"id": s.id, "title": s.title, "description": s.description, "image": s.image.url if s.image else None} for s in favorites]
        return Response(
            {"message": "تم جلب القصص المفضلة ✅", "data":  data},
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        """إضافة قصة"""
        story_id = request.data.get("story_id")
        if not story_id:
            return Response({"error": "story_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return Response({"error": "القصة غير موجودة"}, status=status.HTTP_404_NOT_FOUND)

        request.user.favorites.add(story)
        return Response({"message": "تم إضافة القصة إلى المفضلة ✅"})

    def destroy(self, request, pk=None):
        """حذف قصة"""
        story_id = request.data.get("story_id")
        if not story_id:
            return Response({"error": "story_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return Response({"error": "القصة غير موجودة"}, status=status.HTTP_404_NOT_FOUND)

        request.user.favorites.remove(story)
        return Response({"message": "تم حذف القصة من المفضلة 🗑️"})


import os
 

import dropbox
from django.conf import settings
import requests


def get_dropbox_access_token():
    url = "https://api.dropboxapi.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": settings.DROPBOX_REFRESH_TOKEN,
        "client_id": settings.DROPBOX_APP_KEY,
        "client_secret": settings.DROPBOX_APP_SECRET,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def upload_to_dropbox(file_obj, filename):
    access_token = get_dropbox_access_token()  # نجيب Access Token جديد
    dbx = dropbox.Dropbox(access_token)
    dropbox_path = os.path.join(settings.DROPBOX_BASE_PATH, filename)

    # رفع الملف (overwrite)
    dbx.files_upload(file_obj.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))

    # الأول نبحث لو فيه لينك موجود
    links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True).links
    if links:
        url = links[0].url
    else:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        url = shared_link_metadata.url

    return url.replace("?dl=0", "?dl=1") 

 

class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnlyForAuthenticated]
    search_fields = ["title", "description", "story__title"]

    def get_queryset(self):
        queryset = Episode.objects.all()
        story_id = self.request.query_params.get("story") 
        if story_id:
            queryset = queryset.filter(story_id=story_id)
        return queryset

    def perform_create(self, serializer):
        video_file = self.request.FILES.get("video_file")
        if video_file:
            filename = f"{serializer.validated_data['title']}.mp4"
            dropbox_url = upload_to_dropbox(video_file, filename)
            serializer.save(video_url=dropbox_url)  # نخزن اللينك فقط
        else:
            serializer.save()

    # GET all
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {"message": "تم جلب قائمة الحلقات بنجاح ✅", "data": response.data},
            status=status.HTTP_200_OK,
        )

    # GET one
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # ✅ نزوّد عداد المشاهدات للقصة المرتبطة
        story = instance.story
        story.views_count = story.views_count + 1
        story.save(update_fields=["views_count"])

        serializer = self.get_serializer(instance)
        return Response(
            {"message": "تم جلب الحلقة بنجاح ✅", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "تم إضافة الحلقة بنجاح 🎉", "data": response.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "تم تحديث الحلقة ✅", "data": response.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "تم حذف الحلقة 🗑️"},
            status=status.HTTP_204_NO_CONTENT,
        )

 