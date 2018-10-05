from rest_framework import viewsets
from .models import Terms
from .serializers import CandidatesTermsSerializer
from django.db.models import Prefetch, Count, Q, F
from boards.models import Boards
from .filters import TermsFilter
from app.filters import MaxResults

class CandidatesTermsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Terms.objects.select_related('candidate') \
    .prefetch_related(Prefetch('boards', queryset=Boards.objects.annotate(not_board_amount=Count('board_checks', filter=Q(board_checks__type=2, board_checks__is_board=False))).filter(not_board_amount__lte=2).order_by('-uploaded_at'))) \
    .annotate(verified_board_amount=Count('boards', filter=Q(boards__verified_amount__gte=3)))
    serializer_class = CandidatesTermsSerializer
    filter_fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy', 'verified_board_amount')
    filterset_class = TermsFilter
    pagination_class = MaxResults