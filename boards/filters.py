from django_filters import rest_framework as filters
from .models import Boards
import re
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

class BoardsFilter(filters.FilterSet):
    uploaded_by = filters.UUIDFilter(field_name='uploaded_by', lookup_expr='exact')
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
        
    class Meta:
        model = Boards
        fields = ('uploaded_by','coordinates')

class SingleCheckFilter(filters.FilterSet):
    uploaded_by = filters.UUIDFilter(field_name='uploaded_by', lookup_expr='exact', exclude=True)
    skip_board = filters.NumberFilter(field_name='id', lookup_expr='gt')

    class Meta:
        model = Boards
        fields = ('uploaded_by','skip_board')