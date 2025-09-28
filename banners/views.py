from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer
from .permissions import IsAdminOrReadOnlyForAuthenticated  # استدعاء ال permission الجديد
class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all().order_by("-created_at")
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnlyForAuthenticated]

    def list(self, request, *args, **kwargs):
        # نعرض آخر 3 بانرات فقط
        queryset = Banner.objects.all().order_by("-created_at")[:3]
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"message": "تم جلب قائمة البانرات بنجاح ✅", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # ✅ بعد ما نضيف البانر الجديد نتحقق من العدد
        banners = Banner.objects.all().order_by("-created_at")
        if banners.count() > 3:
            # نحذف الأقدم (آخر واحد في الترتيب العكسي = أول واحد في الطبيعي)
            banners.last().delete()

        return Response(
            {"message": "تم إضافة البانر بنجاح 🎉", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": "تم تحديث بيانات البانر ✅", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "تم حذف البانر 🗑️"},
            status=status.HTTP_204_NO_CONTENT,
        )
