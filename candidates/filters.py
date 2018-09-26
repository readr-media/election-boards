from django_filters import rest_framework as filters
from .models import Terms

class TermsFilter(filters.FilterSet):
    county = filters.CharFilter(method='filter_county')

    def filter_county(self, qs, name, value):
        if not value:
            return qs
            
        filter_value = value.lstrip('[').rstrip(']').split(',')
        filter_value = [x.strip('"').strip() for x in filter_value]
        return qs.filter(**{name+'__in':filter_value})

    class Meta:
        model = Terms
        fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy')
