from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryDetailView,
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ShoppingCartAddItem,
    OrderList,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/create/', CategoryCreateView.as_view()),
    path('categories/detail/<int:pk>/', CategoryDetailView.as_view()),

    path('products/', ProductListView.as_view()),
    path('products/create/', ProductCreateView.as_view()),
    path('products/detail/<int:pk>/', ProductDetailView.as_view()),

    path('cart/add/', ShoppingCartAddItem.as_view()),
    path('orders/', OrderList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)