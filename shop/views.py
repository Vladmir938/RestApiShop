from rest_framework import generics

from .models import Product, Category
from .permissions import IsOwnerOrReadOnly
from .serializers import ProductDetailSerializer, CategoryDetailSerializer, ProductListSerializer

#Категории


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryDetailSerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()


#Товары


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    # permission_classes = (IsOwnerOrReadOnly, )