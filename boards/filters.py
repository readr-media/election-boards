from django_filters import rest_framework as filters
from .models import Boards
import re
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from django.db.models import Count, Q

class BoardsFilter(filters.FilterSet):
    uploaded_by = filters.UUIDFilter(field_name='uploaded_by', lookup_expr='exact')
    verified_amount = filters.NumberFilter(field_name='verified_amount', lookup_expr='gte')
    not_board_amount = filters.NumberFilter(method='filter_not_board_amount')
    coordinates = filters.CharFilter(method='filter_coordinates')

    def filter_coordinates(self, qs, name, value):
        if not value:
            return qs
        radius = self.request.query_params.get('radius', None)
        if radius is None:
            radius = 100
        m = re.match(r'\((?P<lat>[0-9\.]+)\s+(?P<lon>[0-9\.]+)\)', value)
        p = Point(float(m.group('lat')), float(m.group('lon')), srid=4326)
        # qs = Boards.objects.annotate(distance=Distance('coordinates', p)).filter(distance__lte=radius)
        return qs.filter(coordinates__distance_lte=(p,D(m=radius)))
        
    def filter_not_board_amount(self, qs, name, value):
        if not value:
            return qs
        
        return qs.annotate(not_board_amount=Count('board_checks', filter=Q(board_checks__type=2, board_checks__is_board=False))).filter(not_board_amount__lte=value)

    class Meta:
        model = Boards
        fields = ('uploaded_by','coordinates', 'verified_amount', 'not_board_amount')

class SingleCheckFilter(filters.FilterSet):
    uploaded_by = filters.UUIDFilter(field_name='uploaded_by', lookup_expr='exact', exclude=True)
    skip_board = filters.NumberFilter(field_name='id', lookup_expr='gt')

    class Meta:
        model = Boards
        fields = ('uploaded_by','skip_board')