from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import QuerySet

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Post
from .serializers import (
    PostSerializer,
)
from .permissions import IsOwner

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()

    def get_queryset(self) -> QuerySet[Post]:
        # Also filter queryset to user posts for list safety
        return Post.objects.filter(author=self.request.user)
