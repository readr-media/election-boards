from django_filters import rest_framework as filters
from .models import Terms
from boards.models import Boards
from django.db.models import Prefetch, Q, Count, Subquery

class TermsFilter(filters.FilterSet):
    county = filters.CharFilter(method='filter_county')
    verified_amount = filters.NumberFilter(method='filter_verified_amount')
    not_board_amount = filters.NumberFilter(method='filter_not_board_amount')

    def __init__(self, data=None, *args, **kwargs):

        data = data.copy()
        
        # Set default verified_amount to 3
        if 'verified_amount' not in data:
            data['verified_amount'] = 3          
        
        # Set default not_board_amount to 2
        if 'not_board_amount' not in data:
            data['not_board_amount'] = 2

        super(TermsFilter, self).__init__(data, *args, **kwargs)

    def filter_county(self, qs, name, value):
        if not value:
            return qs
            
        filter_value = value.lstrip('[').rstrip(']').split(',')
        filter_value = [x.strip('"').strip() for x in filter_value]
        return qs.filter(**{name+'__in':filter_value})

    def filter_not_board_amount(self, qs, name, not_board_amount):

        return qs.prefetch_related(Prefetch('boards', queryset=Boards.objects.annotate(not_board_amount=Count('board_checks', filter=Q(board_checks__type=2, board_checks__is_board=False))).filter(not_board_amount__lte=not_board_amount).order_by('-uploaded_at')))

    def filter_verified_amount(self, qs, name, verified_amount):

        return qs.annotate(verified_board_amount=Count('boards', filter=Q(boards__verified_amount__gte=verified_amount)))
            


    class Meta:
        model = Terms
        fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy')
