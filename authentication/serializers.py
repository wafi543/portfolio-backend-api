from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.apps import apps
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('users', 'User')
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        user = self.context['request'].user
        try:
            validate_password(value, user=user)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        return value


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate_refresh(self, value):
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        
        try:
            RefreshToken(value)
        except (InvalidToken, TokenError):
            raise serializers.ValidationError(_('Invalid refresh token'))
        return value
