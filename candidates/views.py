from rest_framework import viewsets
from .models import Terms
from .serializers import CandidatesTermsSerializer
from django.db.models import Prefetch, Count, Q, F
from boards.models import Boards
from .filters import TermsFilter
from app.filters import MaxResults

class CandidatesTermsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Terms.objects.select_related('candidate')
    serializer_class = CandidatesTermsSerializer
    filter_fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy', 'verified_board_amount')
    filterset_class = TermsFilter
    pagination_class = MaxResults