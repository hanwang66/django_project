from rest_framework import serializers
from .models import RealEstate

class RealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate
        fields = '__all__'