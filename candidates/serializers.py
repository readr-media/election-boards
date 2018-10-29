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
    not_board_amount = serializers.IntegerField()
    class Meta:
        model = Boards
        fields = ('image','coordinates','county','district','road','took_at','uploaded_at','uploaded_by','verified_amount', 'not_board_amount')

    def to_representation(self, instance):
        location = instance.coordinates
        ret = super(SingleBoardSerializer, self).to_representation(instance)
        del ret['coordinates']
        ret['coordinates'] = '({},{})'.format(location[0],location[1])
        return ret

class CandidatesTermsSerializer(serializers.HyperlinkedModelSerializer):
    boards = SingleBoardSerializer(many=True)
    verified_board_amount = serializers.IntegerField()
    unverified_board_amount = serializers.IntegerField(default=0) # Set default=0 to avoid empty models field problem

    class Meta:
        model = Terms
        fields = ('id','uid', 'election_year', 'type', 'county', 'district', 'name', 'party', 'number', 'image', 'boards', 'constituency', 'verified_board_amount', 'unverified_board_amount')
 
    def to_representation(self, instance):
        ret = super(CandidatesTermsSerializer, self).to_representation(instance)
        # Calculate unverified_board_amount from correct boards length and verified_board_amount
        ret['unverified_board_amount'] = len(ret['boards']) - ret['verified_board_amount']

        if len(ret['boards']) > 1:
            ret['boards'] = ret['boards'][:1]
        return ret

