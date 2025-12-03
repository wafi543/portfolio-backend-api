from django.urls import path

from .views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    PortfolioListCreateView,
    PortfolioRetrieveUpdateDestroyView,
    PortfolioInfoView,
    PortfolioImageListCreateView,
    PortfolioImageRetrieveDestroyView,
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
    # Portfolio Images
    path('<int:portfolio_id>/images/', PortfolioImageListCreateView.as_view(), name='api_portfolio_image_list_create'),
    path('<int:portfolio_id>/images/<int:image_id>/', PortfolioImageRetrieveDestroyView.as_view(), name='api_portfolio_image_detail'),
]
