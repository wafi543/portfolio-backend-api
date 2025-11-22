from django.db import models
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage


class Portfolio(models.Model):
    CATEGORY_CHOICES = (
        ('photography', 'Photography'),
        ('video', 'Video Editing'),
        ('branding', 'Branding'),
        ('design', 'Design'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(
        upload_to='portfolios/%Y/%m/%d/',
        blank=True,
        null=True,
        storage=GoogleCloudStorage()
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class PortfolioInfo(models.Model):
    """Store portfolio owner's information linked to a User"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio_info', null=True, blank=True)
    portfolio_title = models.CharField(max_length=200, default='My Portfolio')
    portfolio_title_ar = models.CharField(max_length=200, default='منصة أعمالي')
    background_image = models.ImageField(
        upload_to='portfolio_background/',
        blank=True,
        null=True,
        storage=GoogleCloudStorage(),
        help_text='Portfolio background image for website'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portfolio Info"
        verbose_name_plural = "Portfolio Info"

    def __str__(self) -> str:
        if self.user:
            return f"{self.portfolio_title} - {self.user.get_full_name()}"
        return self.portfolio_title
