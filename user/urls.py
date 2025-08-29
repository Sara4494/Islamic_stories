from django.urls import path
from .views import RegisterView, LoginView ,GoogleLoginCallbackView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
      path("api/auth/google/callback/", GoogleLoginCallbackView.as_view(), name="google_callback"),
]
