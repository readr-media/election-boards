from rest_framework import viewsets, serializers
from .models import Terms

# Create your views here.

class CandidatesTermsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'

class CandidatesTermsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Terms.objects.all().select_related('candidate')
    serializer_class = CandidatesTermsSerializer
    filter_fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy')
