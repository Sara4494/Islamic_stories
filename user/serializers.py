from rest_framework import serializers
from .models import User
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "full_name", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # مش هنخزنها
        user = User.objects.create_user(**validated_data)
        return user
    
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name", "profile_image"]


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["email", "full_name", "password", "profile_image"]

    def update(self, instance, validated_data):
        # لو فيه باسورد جديد → نعمل set_password
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)

