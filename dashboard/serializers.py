
from rest_framework import serializers  
from user.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "profile_image", "is_banned", "is_active"]
