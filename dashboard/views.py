from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view ,action
from content.models import  Category, Story
from user.models import User
from banners.models import Banner
from .serializers import UserSerializer 
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAdminUser


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "full_name"]
    # permission_classes = [IsAdminUser]  # ✅ admin بس

    @action(detail=True, methods=["put", "patch"], permission_classes=[IsAdminUser])
    def update_user(self, request, pk=None):
        user = self.get_object()
        is_banned = request.data.get("is_banned")
        if is_banned is not None:
            if isinstance(is_banned, str):
                is_banned = is_banned.lower() in ["true", "1", "yes"]
            user.set_ban(is_banned)

        return Response(
            {"message": "تم تحديث حالة المستخدم ✅", "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
@permission_classes([IsAdminUser])  # ✅ admin بس
def dashboard_stats(request):
    data = {
        "categories_count": Category.objects.count(),
        "stories_count": Story.objects.count(),
        "banners_count": Banner.objects.count(),
        "users_count": User.objects.filter(is_active=True).count(),
    }
    return Response(
        {"message": "تم جلب الإحصائيات بنجاح 📊", "data": data},
        status=status.HTTP_200_OK,
    )
 