from rest_framework import serializers
from .models import Terms, Candidates

# Create your views here.
class CandidatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidates
        fields = '__all__'
        
class CandidatesTermsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'

