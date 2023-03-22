from django.urls import path

from shop.views import *

app_name = 'shop'

urlpatterns = [
    path('category/create/', CategoryCreateView.as_view()),
    path('product/create/', ProductCreateView.as_view()),
    path('product/all/', ProductListView.as_view()),
    path('product/detail/<int:pk>', ProductDetailView.as_view()),

]