from rest_framework import viewsets
from .models import Councilors, CouncilorsDetail
from .serializers import CouncilorsSerializer, CouncilorsDetailSerializer

# Create your views here.
class CouncilorsDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CouncilorsDetail.objects.all().select_related('councilor')
    serializer_class = CouncilorsDetailSerializer
    filter_fields = ('councilor', 'election_year', 'name', 'gender', 'party', 'title', 'constituency', 'county', 'in_office', 'term_start')

class CouncilorsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Councilors.objects.all().prefetch_related('each_terms')
    serializer_class = CouncilorsSerializer
    filter_fields = ('uid', 'name')
