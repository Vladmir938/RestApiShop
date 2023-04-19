from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, Category, Order
from .permissions import IsManagerOrReadOnly, IsAuthorizedUser, IsManagerOrAdmin, IsReadOnly, IsAdminOrReadOnly, \
    IsAdminOrReadOnlyProductDetail, IsAuthorizedUserProductDetail
from .serializers import ProductDetailSerializer, CategoryDetailSerializer, ProductListSerializer, \
    ShoppingCartSerializer, OrderSerializer, UserSerializer


# Категории
class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsManagerOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsManagerOrReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminOrReadOnlyProductDetail | IsAuthorizedUserProductDetail]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthorizedUserProductDetail()]
        return [IsAdminOrReadOnlyProductDetail()]


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsManagerOrReadOnly | IsAdminOrReadOnly | IsReadOnly]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrReadOnlyProductDetail | IsAuthorizedUserProductDetail]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthorizedUserProductDetail()]
        return [IsAdminOrReadOnlyProductDetail()]


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [IsManagerOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ShoppingCartAddItem(generics.CreateAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

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
