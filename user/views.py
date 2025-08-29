from rest_framework import status, permissions
from rest_framework import generics
from django.contrib.auth import authenticate
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from google.oauth2 import id_token
import requests  
from django.conf import settings

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data["email"])
        token, _ = Token.objects.get_or_create(user=user)
        response.data["token"] = token.key
        return response


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class GoogleLoginCallbackView(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # تبادل الكود مع Google OAuth2 token endpoint
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": "http://localhost:8000/api/auth/google/callback/",
            "grant_type": "authorization_code",
        }
        token_res = requests.post(token_url, data=data).json()

        if "error" in token_res:
            return Response(token_res, status=status.HTTP_400_BAD_REQUEST)

        # جلب بيانات المستخدم من Google API
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"alt": "json", "access_token": token_res["access_token"]}
        ).json()

        # إنشاء أو جلب المستخدم
        user, _ = User.objects.get_or_create(
            email=user_info["email"],
            defaults={"full_name": user_info.get("name", "")}
        )

        # إصدار توكن API عادي
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "email": user.email,
                "full_name": user.full_name,
            }
        })