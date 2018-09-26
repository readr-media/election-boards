from django_filters import rest_framework as filters
from .models import Boards

class BoardsFilter(filters.FilterSet):
    uploaded_by = filters.UUIDFilter(field_name='uploaded_by', lookup_expr='exact')

    class Meta:
        model = Boards
        fields = ('uploaded_by',)
