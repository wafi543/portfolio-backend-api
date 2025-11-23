from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


class IsAccessTokenValid(BasePermission):
    """
    Allows access only if the user has a valid access token.
    """
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return False
        
        try:
            jwt_authenticator = JWTAuthentication()
            validated_user, validated_token = jwt_authenticator.authenticate(request)
            request.user = validated_user
            return True
        except (InvalidToken, AuthenticationFailed):
            return False