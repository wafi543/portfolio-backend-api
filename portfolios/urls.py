from django.urls import path

from .views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    PortfolioListCreateView,
    PortfolioRetrieveUpdateDestroyView,
    PortfolioInfoView,
)

urlpatterns = [
    # Category CRUD
    path('categories/', CategoryListCreateView.as_view(), name='api_category_list_create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='api_category_detail'),
    # Portfolio CRUD
    path('', PortfolioListCreateView.as_view(), name='api_portfolio_list_create'),
    path('<int:pk>/', PortfolioRetrieveUpdateDestroyView.as_view(), name='api_portfolio_detail'),
    # Portfolio Info (public metadata)
    path('info/', PortfolioInfoView.as_view(), name='portfolio_info'),
]
