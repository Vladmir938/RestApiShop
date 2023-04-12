from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Product, Category, Order
from .permissions import IsManagerOrReadOnly, IsAuthenticatedOrReadOnly, IsUnauthenticated
from .serializers import ProductDetailSerializer, CategoryDetailSerializer, ProductListSerializer, \
    ShoppingCartSerializer, OrderSerializer, UserSerializer


# Категории


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    permission_classes = [IsManagerOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


# Товары


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class ShoppingCartAddItem(generics.CreateAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Create a new order for the currently authenticated user.
        """
        serializer.save(user=self.request.user)


User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(token, status=status.HTTP_201_CREATED)
