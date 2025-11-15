from django.urls import path

from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Posts CRUD
    path('posts/', PostListCreateView.as_view(), name='api_post_list_create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='api_post_detail'),
]
