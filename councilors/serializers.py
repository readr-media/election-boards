from rest_framework import serializers
from .models import Councilors, CouncilorsDetail

class CouncilorsDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CouncilorsDetail
        fields = '__all__'

class CouncilorsSerializer(serializers.HyperlinkedModelSerializer):
    each_terms = CouncilorsDetailSerializer(many=True)
    class Meta:
        model = Councilors
        fields = '__all__'
