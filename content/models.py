from django.db import models
from django.utils import timezone

# قسم
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def stories_count(self):
        return self.stories.count()  # عدد القصص المرتبطة بالقسم


# قصة
class Story(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="stories", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="stories/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.title


# حلقة
class Episode(models.Model):
    story = models.ForeignKey(Story, related_name="episodes", on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="episodes/thumbnails/", blank=True, null=True)

    # وسائط
    video_file = models.FileField(upload_to="episodes/videos/", blank=True, null=True)
    audio_file = models.FileField(upload_to="episodes/audios/", blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    duration_minutes = models.PositiveIntegerField(default=0)  # مدة الحلقة بالدقائق
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.story.title} - Episode {self.episode_number}"
