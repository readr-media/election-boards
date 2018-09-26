from rest_framework import viewsets
from .models import Terms
from .serializers import CandidatesTermsSerializer
from django.db.models import Prefetch
from boards.models import Boards
from .filters import TermsFilter

class CandidatesTermsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Terms.objects.all().select_related('candidate').prefetch_related(Prefetch('boards', queryset=Boards.objects.order_by('-uploaded_at')))
    serializer_class = CandidatesTermsSerializer
    filter_fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy')
    filterset_class = TermsFilter