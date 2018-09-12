from django.shortcuts import render
from rest_framework import viewsets
from .models import Elections
from .serializers import ElectionsSerializer

# Create your views here.
class ElectionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Elections.objects.all()
    serializer_class = ElectionsSerializer
    filter_fields = ('id', )
