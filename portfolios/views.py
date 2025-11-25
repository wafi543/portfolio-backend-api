from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Portfolio, PortfolioInfo, Category
from .serializers import (
    PortfolioSerializer,
    PortfolioInfoSerializer,
    CategorySerializer,
)
from .permissions import IsOwner, IsCategoryOwner
from authentication.permissions import IsSuperUser

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsSuperUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Category]:
        return Category.objects.all()

    def paginate_queryset(self, queryset):
        """Disable pagination if no_pagination query parameter is present"""
        if self.request.query_params.get('no_pagination'):
            return None
        return super().paginate_queryset(queryset)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Category]:
        return Category.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        Prevent deletion of categories with linked portfolios.
        Catch ProtectedError from on_delete=models.PROTECT.
        """
        instance = self.get_object()
        try:
            return super().destroy(request, *args, **kwargs)
        except models.ProtectedError:
            return Response(
                {'detail': format_lazy(_('Cannot delete category with associated portfolios. Please reassign or delete the portfolios first.'))},
                status=status.HTTP_400_BAD_REQUEST
            )


class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsSuperUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Portfolio]:
        queryset = Portfolio.objects.all()
        
        # Filter by category if ?category query parameter is present
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter latest 6 portfolios if ?recent query parameter is present
        if self.request.query_params.get('recent'):
            queryset = queryset.order_by('-created_at')[:6]
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PortfolioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Portfolio]:
        # Also filter queryset to user portfolios for list safety
        return Portfolio.objects.all()


class PortfolioInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Retrieve portfolio info"""
        try:
            portfolio_info = PortfolioInfo.objects.first()
            if not portfolio_info:
                return Response(
                    {'detail': _('Portfolio info not found')},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = PortfolioInfoSerializer(portfolio_info)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
