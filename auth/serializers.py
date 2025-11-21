from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


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
            raise serializers.ValidationError('Invalid refresh token')
        return value
