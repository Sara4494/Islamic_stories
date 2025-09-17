from rest_framework import serializers
from .models import Category, Story, Episode


class CategorySerializer(serializers.ModelSerializer):
    stories_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "stories_count"]


class StorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Story
        fields = ["id", "title", "description", "image", "created_at", "category", "category_name"]


class EpisodeSerializer(serializers.ModelSerializer):
    story_title = serializers.ReadOnlyField(source="story.title")
    video_file = serializers.FileField(write_only=True, required=False)  # يقبل الملف
    video_url = serializers.CharField(read_only=True)  # نخزن فيه اللينك

    class Meta:
        model = Episode
        fields = [
            "id", "story", "story_title", "episode_number", "title", "description",
            "thumbnail", "video_file", "audio_file", "youtube_url",
            "video_url", "duration_minutes", "created_at"
        ]

    def create(self, validated_data):
        validated_data.pop("video_file", None)  # نتأكد إننا مانبعتش الفيديو للـ model
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("video_file", None)  # برضو في التحديث
        return super().update(instance, validated_data)

