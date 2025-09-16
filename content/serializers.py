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

    class Meta:
        model = Episode
        fields = [
            "id", "story", "story_title", "episode_number", "title", "description",
            "thumbnail", "video_file", "audio_file", "youtube_url",
            "duration_minutes", "created_at"
        ]
