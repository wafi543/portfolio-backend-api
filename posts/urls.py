from django.urls import path

from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Posts CRUD
    path('', PostListCreateView.as_view(), name='api_post_list_create'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='api_post_detail'),
]
