from django_filters import rest_framework as filters
from .models import Terms
from boards.models import Boards
from django.db.models import Prefetch, Q, Count, Subquery

class TermsFilter(filters.FilterSet):
    county = filters.CharFilter(method='filter_county')
    verified_amount = filters.NumberFilter(method='filter_verified_amount')
    not_board_amount = filters.NumberFilter(method='filter_not_board_amount')

    def filter_county(self, qs, name, value):
        if not value:
            return qs
            
        filter_value = value.lstrip('[').rstrip(']').split(',')
        filter_value = [x.strip('"').strip() for x in filter_value]
        return qs.filter(**{name+'__in':filter_value})

    def filter_verified_amount(self, qs, name, verified_amount):
        if not verified_amount:
            return qs

        not_board_amount = self.request.query_params.get('not_board_amount', None)
        if not_board_amount is None:
            not_board_amount = 2
        boards = Boards.objects.annotate(not_board_amount=Count('board_checks', filter=Q(board_checks__type=2, board_checks__is_board=False))).filter(not_board_amount__lte=not_board_amount).order_by('-uploaded_at') 
        qs = Terms.objects.select_related('candidate') \
            .prefetch_related(Prefetch('boards', queryset=boards)) \
            .annotate(verified_board_amount=Count('boards', filter=Q(boards__verified_amount__gte=verified_amount)))

    def filter_not_board_amount(self, qs, name, not_board_amount):
        if not not_board_amount:
            return qs

        verified_amount = self.request.query_params.get('verified_amount', None)
        if verified_amount is None:
            verified_amount = 3
        return Terms.objects.select_related('candidate') \
            .prefetch_related(Prefetch('boards', queryset=Boards.objects.annotate(not_board_amount=Count('board_checks', filter=Q(board_checks__type=2, board_checks__is_board=False))).filter(not_board_amount__lte=not_board_amount).order_by('-uploaded_at'))) \
            .annotate(verified_board_amount=Count('boards', filter=Q(boards__verified_amount__gte=verified_amount)))

    class Meta:
        model = Terms
        fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy')
