from rest_framework import serializers
from django.apps import apps


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    portfolio_title = serializers.SerializerMethodField()
    portfolio_title_ar = serializers.SerializerMethodField()
    background_image = serializers.SerializerMethodField()

    class Meta:
        model = apps.get_model('users', 'User')
        fields = ['id', 'full_name', 'first_name', 'last_name', 'email', 'job_title', 'phone_number', 'location', 'about_me', 'about_me_ar', 'portfolio_title', 'portfolio_title_ar', 'background_image']
        read_only_fields = ['id', 'full_name', 'portfolio_title', 'portfolio_title_ar']

    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_portfolio_title(self, obj):
        """Get portfolio_title from related PortfolioInfo"""
        return obj.portfolio_info.portfolio_title if hasattr(obj, 'portfolio_info') and obj.portfolio_info else None
    
    def get_portfolio_title_ar(self, obj):
        """Get portfolio_title_ar from related PortfolioInfo"""
        return obj.portfolio_info.portfolio_title_ar if hasattr(obj, 'portfolio_info') and obj.portfolio_info else None

    def get_background_image(self, obj):
        """Get background_image from related PortfolioInfo"""
        return obj.portfolio_info.background_image.url if hasattr(obj, 'portfolio_info') and obj.portfolio_info and obj.portfolio_info.background_image else None

    def update(self, instance, validated_data):
        """
        Update user profile and related PortfolioInfo on PUT request.
        """
        # Extract portfolio fields from request
        request = self.context.get('request')
        portfolio_title = request.data.get('portfolio_title') if request else None
        portfolio_title_ar = request.data.get('portfolio_title_ar') if request else None
        background_image = request.FILES.get('background_image') if request else None
        
        # Update User model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update PortfolioInfo if portfolio fields are provided
        if portfolio_title is not None or portfolio_title_ar is not None or background_image is not None:
            from portfolios.models import PortfolioInfo
            portfolio_info, created = PortfolioInfo.objects.get_or_create(user=instance)
            
            if portfolio_title is not None:
                portfolio_info.portfolio_title = portfolio_title
            if portfolio_title_ar is not None:
                portfolio_info.portfolio_title_ar = portfolio_title_ar
            if background_image is not None:
                portfolio_info.background_image = background_image
            
            portfolio_info.save()
        
        return instance
