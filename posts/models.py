from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('photography', 'Photography'),
        ('video', 'Video Editing'),
        ('branding', 'Branding'),
        ('design', 'Design'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
