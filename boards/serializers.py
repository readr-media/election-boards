from rest_framework import serializers
from .models import Boards
from candidates.models import Candidates, Terms

class BoardsTermsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terms
        fields = ('uid', 'election_year', 'type', 'county', 'district', 'name', 'party', 'number', 'image')


class BoardsGetSerializer(serializers.ModelSerializer):
    candidates = BoardsTermsSerializer(many=True,read_only=True)
    
    class Meta:
        model = Boards
        fields = '__all__'
    
    def to_representation(self, instance):
        location = instance.coordinates
        ret = super(BoardsGetSerializer, self).to_representation(instance)
        del ret['coordinates']
        ret['coordinates'] = '({},{})'.format(location[0],location[1])
        return ret

class BoardsPostSerializer(serializers.ModelSerializer):
    candidates = serializers.PrimaryKeyRelatedField(many=True, queryset=Terms.objects.all())

    class Meta:
        model = Boards
        fields = '__all__'
    
    def create(self, validated_data):
        # Create uploader
        board_candidates = validated_data.pop('candidates')
        board = Boards.objects.create(**validated_data)

        # Create relationship
        for candidate in board_candidates:
            board.candidates.add(candidate)
        return board
    
    def to_internal_value(self, data):
        data['coordinates'] = "SRID=4326;POINT " + data['coordinates']
        return super(BoardsPostSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        location = instance.coordinates
        ret = super(BoardsPostSerializer, self).to_representation(instance)
        del ret['coordinates']
        ret['coordinates'] = '({},{})'.format(location[0],location[1])
        return ret