from rest_framework import serializers
from core.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['img']


class UserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=56)





