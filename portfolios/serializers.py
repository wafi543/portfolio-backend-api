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
    bio = serializers.SerializerMethodField()
    bio_ar = serializers.SerializerMethodField()
    about_me = serializers.SerializerMethodField()
    about_me_ar = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioInfo
        fields = ['id', 'portfolio_title', 'portfolio_title_ar', 'full_name', 'email', 'job_title', 'phone_number', 'location', 'bio', 'bio_ar', 'about_me', 'about_me_ar', 'background_image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'full_name', 'email', 'job_title', 'phone_number', 'location', 'bio', 'bio_ar', 'about_me', 'about_me_ar', 'created_at', 'updated_at']

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
    
    def get_about_me(self, obj):
        """Get about_me from related User"""
        return obj.user.about_me if obj.user else None
    
    def get_about_me_ar(self, obj):
        """Get about_me_ar from related User"""
        return obj.user.about_me_ar if obj.user else None
    
    def get_bio(self, obj):
        """Get bio from related User"""
        return obj.user.bio if obj.user else None
    
    def get_bio_ar(self, obj):
        """Get bio_ar from related User"""
        return obj.user.bio_ar if obj.user else None
