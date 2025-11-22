from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db import models

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

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Category]:
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsCategoryOwner]
    queryset = Category.objects.all()

    def get_queryset(self) -> QuerySet[Category]:
        return Category.objects.filter(user=self.request.user)

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
                {'detail': f'Cannot delete category with {instance.portfolios.count()} existing portfolio(s).'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Portfolio]:
        if self.request.user.is_authenticated:
            queryset = Portfolio.objects.filter(author=self.request.user)
        else:
            queryset = Portfolio.objects.all()
        
        # Filter latest 6 portfolios if ?recent query parameter is present
        if self.request.query_params.get('recent'):
            queryset = queryset.order_by('-created_at')[:6]
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PortfolioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Portfolio.objects.all()

    def get_queryset(self) -> QuerySet[Portfolio]:
        # Also filter queryset to user portfolios for list safety
        return Portfolio.objects.filter(author=self.request.user)


class PortfolioInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Retrieve portfolio info"""
        try:
            portfolio_info = PortfolioInfo.objects.first()
            if not portfolio_info:
                return Response(
                    {'detail': 'Portfolio info not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = PortfolioInfoSerializer(portfolio_info)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
