from django.db import models
from django.conf import settings
from django.utils.text import slugify
from storages.backends.gcloud import GoogleCloudStorage


class Category(models.Model):
    """Custom, per-user portfolio categories with auto-generated, immutable slug."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, help_text="Category name in English")
    name_ar = models.CharField(max_length=100, help_text="Category name in Arabic")
    slug = models.CharField(max_length=100, editable=False)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Icon name from lucide-react (e.g., 'camera', 'video')")
    description = models.TextField(blank=True, null=True, help_text="Category description in English")
    description_ar = models.TextField(blank=True, null=True, help_text="Category description in Arabic")
    features = models.JSONField(default=list, blank=True, help_text="List of features/services offered")
    order = models.PositiveIntegerField(default=0, help_text="Display order for frontend")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'slug']]
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        # Auto-generate slug from English name on creation only
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} / {self.name_ar} ({self.user.username})"


class Portfolio(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(
        upload_to='portfolios/%Y/%m/%d/',
        blank=True,
        null=True,
        storage=GoogleCloudStorage()
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='portfolios')
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
