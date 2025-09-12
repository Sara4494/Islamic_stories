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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
 
 

from .models import User 
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


class LoginView(APIView):
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
from .models import User, PasswordResetOTP    
import random
from django.core.mail import send_mail

class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No user with this email"}, status=status.HTTP_404_NOT_FOUND)

        # توليد OTP (6 أرقام)
        otp = str(random.randint(100000, 999999))

        # حفظه في جدول
        PasswordResetOTP.objects.create(user=user, otp=otp)

        # إرسال OTP بالإيميل
        send_mail(
            subject="Your Password Reset Code",
            message=f"Your OTP code is: {otp}. It will expire in 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"message": "OTP sent to your email!"}, status=status.HTTP_200_OK)

class ResetPasswordConfirmView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not (email and otp and password and confirm_password):
            return Response({"error": "Email, OTP, password, and confirm_password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # التحقق من المستخدم
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email"}, status=status.HTTP_404_NOT_FOUND)

        # التحقق من OTP
        try:
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).latest("created_at")
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if not otp_obj.is_valid():
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

        # تغيير الباسورد
        user.set_password(password)
        user.save()

        # حذف الـ OTP بعد الاستخدام
        otp_obj.delete()

        return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
