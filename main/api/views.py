from rest_framework import generics
from rest_framework import viewsets

from ..models import (
    GameCategory,
    Product,
    Comments,
    ImageGallery
)
from .serializers import (
    GameCategorySerializer,
    ProductSerializer,
)


class GameCategoryListView(generics.ListAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer


class GameCategoryDetailView(generics.RetrieveAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



