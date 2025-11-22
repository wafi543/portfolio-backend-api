from rest_framework import serializers

from .models import Portfolio, PortfolioInfo
from auth.serializers import UserSerializer

class PortfolioSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Portfolio
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


class PortfolioInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioInfo
        fields = ['id', 'portfolio_title', 'full_name', 'email', 'job_title', 'phone_number', 'location', 'background_image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'full_name', 'email', 'job_title', 'phone_number', 'location', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        """Get full name from related User"""
        return obj.user.get_full_name() if obj.user else None
    
    def get_email(self, obj):
        """Get email from related User"""
        return obj.user.email if obj.user else None
    
    def get_job_title(self, obj):
        """Get job title from related User"""
        return obj.user.job_title if obj.user else None
    
    def get_phone_number(self, obj):
        """Get phone number from related User"""
        return obj.user.phone_number if obj.user else None
    
    def get_location(self, obj):
        """Get location from related User"""
        return obj.user.location if obj.user else None
