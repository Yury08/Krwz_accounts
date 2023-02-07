from rest_framework import serializers
from ..models import (
    GameCategory,
    Product,
    ImageGallery,
    Comments
)

class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCategory
        fields = '__all__'

class ImageGallerySerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = ['product', 'image']

class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['product', 'name', 'created', 'text', 'active']

class ProductSerializer(serializers.ModelSerializer):
    images = ImageGallerySerializers(many=True)
    comm = CommentsSerializers(many=True)

    class Meta:
        model = Product
        fields = ['pk', 'category', 'title', 'slug', 'desc', 'availability',
                  'available', 'created', 'updated', 'price',
                  'overview', 'salesman', 'region', 'comm', 'images']