from rest_framework import generics

from .models import Product
from .permissions import IsOwnerOrReadOnly
from .serializers import ProductDetailSerializer, CategoryDetailSerializer, ProductListSerializer


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryDetailSerializer


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    # permission_classes = (IsOwnerOrReadOnly, )