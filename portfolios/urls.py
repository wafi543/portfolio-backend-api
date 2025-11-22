from django.urls import path

from .views import (
    PortfolioListCreateView,
    PortfolioRetrieveUpdateDestroyView,
    PortfolioInfoView,
)

urlpatterns = [
    # Portfolio CRUD
    path('', PortfolioListCreateView.as_view(), name='api_portfolio_list_create'),
    path('<int:pk>/', PortfolioRetrieveUpdateDestroyView.as_view(), name='api_portfolio_detail'),
    # Portfolio Info (public metadata)
    path('info/', PortfolioInfoView.as_view(), name='portfolio_info'),
]
