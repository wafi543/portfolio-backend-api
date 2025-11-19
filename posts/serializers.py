from rest_framework import serializers

from .models import Post
from auth.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'subtitle', 'image', 'category', 'body', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_image(self, value):
        """
        Validate image file size (max 5MB to minimize GCS costs).
        """
        if not value:
            return value
        
        # Check file size (5MB limit)
        size_mb = value.size / (1024 * 1024)
        if size_mb > 5:
            raise serializers.ValidationError(f'Image size ({size_mb:.2f}MB) exceeds 5MB limit')
        
        return value
