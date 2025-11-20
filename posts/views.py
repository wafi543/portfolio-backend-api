from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import QuerySet

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Post
from .serializers import (
    PostSerializer,
)
from .permissions import IsOwner

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Post]:
        if self.request.user.is_authenticated:
            queryset = Post.objects.filter(author=self.request.user)
        else:
            queryset = Post.objects.all()
        
        # Filter latest 6 posts if ?recent query parameter is present
        if self.request.query_params.get('recent'):
            queryset = queryset.order_by('-created_at')[:6]
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()

    def get_queryset(self) -> QuerySet[Post]:
        # Also filter queryset to user posts for list safety
        return Post.objects.filter(author=self.request.user)
