from django.contrib import admin
from .models import Portfolio, PortfolioInfo, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'slug', 'user', 'created_at')
    search_fields = ('name', 'name_ar', 'user__username')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    list_filter = ('user',)
    fields = ('user', 'name', 'name_ar', 'slug', 'created_at', 'updated_at')


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'body', 'author__username')
    list_filter = ('author', 'category')


@admin.register(PortfolioInfo)
class PortfolioInfoAdmin(admin.ModelAdmin):
    list_display = ('portfolio_title', 'get_full_name', 'get_email')
    fields = ('user', 'portfolio_title', 'background_image')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_full_name(self, obj):
        """Display full name from related User"""
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        """Display email from related User"""
        return obj.user.email
    get_email.short_description = 'Email'
    
    def has_delete_permission(self, request):
        """Prevent deletion of portfolio info"""
        return False
    
    def has_add_permission(self, request):
        """Prevent adding new portfolio info instances"""
        return PortfolioInfo.objects.count() == 0
