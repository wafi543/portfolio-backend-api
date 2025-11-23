from django.urls import path


from .views import (
    LoginView,
    LogoutView,
    MeView,
    PasswordChangeView,
    TokenVerifyView,
    TokenRefreshView,
)
from .serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
)

urlpatterns = [    # Auth
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('me/', MeView.as_view(), name='api_me'),
    path('password-change/', PasswordChangeView.as_view(), name='api_password_change'),
    path('token/verify/', TokenVerifyView.as_view(), name='api_token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]