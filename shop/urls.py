from django.urls import path

from shop.views import *

app_name = 'shop'

urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('category/create/', CategoryCreateView.as_view()),
    path('category/detail/<slug:pk>', CategoryDetailView.as_view()),
    path('product/', ProductListView.as_view()),
    path('product/create/', ProductCreateView.as_view()),
    path('product/detail/<int:pk>', ProductDetailView.as_view()),


]