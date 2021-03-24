from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        #모델안에 있는 모든 필드들을 가져옴
        fields = '__all__'