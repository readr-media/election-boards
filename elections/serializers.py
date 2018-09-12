from .models import Elections
from rest_framework import serializers

class ElectionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Elections
        fields = '__all__'
