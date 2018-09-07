from rest_framework import serializers
from .models import Terms, Candidates
from boards.models import Boards

# Create your views here.
class CandidatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidates
        fields = '__all__'

# special TermsSerializer for Boards
class SingleBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ('image','coordinates','county','district','road','took_at','uploaded_at','uploaded_by','verified_amount')

    def to_representation(self, instance):
        location = instance.coordinates
        ret = super(SingleBoardSerializer, self).to_representation(instance)
        del ret['coordinates']
        ret['coordinates'] = '({},{})'.format(location[0],location[1])
        return ret

class CandidatesTermsSerializer(serializers.HyperlinkedModelSerializer):
    boards = SingleBoardSerializer(many=True)
    class Meta:
        model = Terms
        fields = ('uid', 'election_year', 'type', 'county', 'district', 'name', 'party', 'number', 'image','boards')
    
    def to_representation(self, instance):
        ret = super(CandidatesTermsSerializer, self).to_representation(instance)
        if len(ret['boards']) > 1:
            ret['boards'] = ret['boards'][0]
        return ret

class g0vCandidatesTermsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terms
        fields = ('uid', 'election_year', 'type', 'county', 'district', 'name', 'party', 'number', 'image')

