from rest_framework import serializers
import re

from .models import Portfolio, PortfolioInfo, Category
from auth.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for user-scoped portfolio categories with immutable slug."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def validate_name(self, value):
        """Ensure category name contains only English alphabetical characters and spaces."""
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError('Category name must contain only English alphabetical characters and spaces.')
        return value

    def validate_name_ar(self, value):
        """Ensure category Arabic name contains only Arabic characters and spaces."""
        if not re.match(r'^[\u0600-\u06FF\s]+$', value):
            raise serializers.ValidationError('Category Arabic name must contain only Arabic characters and spaces.')
        return value

    def create(self, validated_data):
        """Auto-generate slug from name on creation."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Prevent slug changes (keep slug immutable)."""
        # Allow updating name and name_ar; slug remains immutable
        instance.name = validated_data.get('name', instance.name)
        instance.name_ar = validated_data.get('name_ar', instance.name_ar)
        instance.save()
        return instance


class PortfolioSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'title', 'subtitle', 'image', 'category', 'category_id', 'body', 'author', 'created_at', 'updated_at']
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

    def validate_category_id(self, value):
        """
        Ensure category belongs to the authenticated user.
        """
        if value is None:
            return value
        
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('Category selection requires authentication.')
        
        try:
            category = Category.objects.get(id=value, user=request.user)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category does not exist or does not belong to you.')
        
        return value

    def create(self, validated_data):
        """Set author to current user and handle category FK."""
        category_id = validated_data.pop('category_id', None)
        portfolio = Portfolio.objects.create(author=self.context['request'].user, **validated_data)
        
        if category_id:
            portfolio.category_id = category_id
            portfolio.save()
        
        return portfolio

    def update(self, instance, validated_data):
        """Handle category FK update."""
        category_id = validated_data.pop('category_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if category_id is not None:
            instance.category_id = category_id
        
        instance.save()
        return instance


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
