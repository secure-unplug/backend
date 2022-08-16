from operator import index
from rest_framework import serializers
from .models import Entries

class indexserializer(serializers.ModelSerializer) :
    class Meta :
        model = index        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함