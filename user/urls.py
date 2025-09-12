from django.urls import path
from .views import RegisterView, LoginView ,GoogleLoginCallbackView ,RequestPasswordResetView ,ResetPasswordConfirmView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("api/auth/google/callback/", GoogleLoginCallbackView.as_view(), name="google_callback"),
  
     path("password-reset/", RequestPasswordResetView.as_view(), name="password_reset"),

    # تأكيد OTP + تعيين باسورد جديد
    path("password-reset-confirm/", ResetPasswordConfirmView.as_view(), name="password_reset_confirm"),
]


 