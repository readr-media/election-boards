from rest_framework import serializers, viewsets
from .models import Councilors, CouncilorsDetail

# Create your views here.
class CouncilorsDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CouncilorsDetail
        fields = '__all__'

class CouncilorsSerializer(serializers.HyperlinkedModelSerializer):
    each_terms = CouncilorsDetailSerializer(many=True)
    class Meta:
        model = Councilors
        fields = '__all__'

class CouncilorsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Councilors.objects.all().prefetch_related('each_terms')
    serializer_class = CouncilorsSerializer
    filter_fields = ('uid', 'name')

class CouncilorsDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CouncilorsDetail.objects.all().select_related('councilor')
    serializer_class = CouncilorsDetailSerializer
    filter_fields = ('councilor', 'election_year', 'name', 'gender', 'party', 'title', 'constituency', 'county', 'in_office', 'term_start')
