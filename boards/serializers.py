from rest_framework import serializers
from .models import Boards, Checks
from candidates.models import Candidates, Terms
from datetime import datetime
from django.contrib.gis.geos import Point
import re

class TimestampField(serializers.DateTimeField): 
    
    def to_internal_value(self, value):
        converted_time = datetime.fromtimestamp(float(value))
        return super(TimestampField, self).to_internal_value(converted_time)
        
class CoordinatesField(serializers.Field):
    
    def to_internal_value(self, data):
        m = re.match(r'\((?P<lat>[0-9\.]+)\s+(?P<lon>[0-9\.]+)\)', data)
        return Point(float(m.group('lat')), float(m.group('lon')))

    def to_representation(self, obj):
        return '({} {})'.format(obj[0],obj[1])

class BoardsTermsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terms
        fields = ('uid', 'election_year', 'type', 'county', 'district', 'name', 'party', 'number', 'image')

class BoardsGetSerializer(serializers.ModelSerializer):
    candidates = BoardsTermsSerializer(many=True,read_only=True)
    coordinates = CoordinatesField()

    class Meta:
        model = Boards
        fields = '__all__'
    
class BoardsPostSerializer(serializers.ModelSerializer):
    candidates = serializers.PrimaryKeyRelatedField(many=True, queryset=Terms.objects.all())
    took_at = TimestampField()
    uploaded_by = serializers.UUIDField(format='hex_verbose')
    coordinates = CoordinatesField()

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

class CheckBoardDeserializer(serializers.ModelSerializer):

    board = serializers.PrimaryKeyRelatedField(queryset=Boards.objects.all())
    candidates = serializers.PrimaryKeyRelatedField(many=True, queryset=Terms.objects.all(), required=False)
    created_by = serializers.UUIDField(format='hex_verbose')
    is_board = serializers.BooleanField(required=True)
    
    class Meta:
        model = Checks
        fields = '__all__'

    def create(self, validated_data):
        check_candidates = [] 
        if 'candidates' in validated_data:
            check_candidates = validated_data.pop('candidates')
            # if len(check_candidates) <= 0:
            #     raise serializers.ValidationError("candidats field presented but its length is 0")
        validated_data['type'] = 1
        check = Checks.objects.create(**validated_data)

        # If there are denoted candidates, create relationship
        if check_candidates: 
            for candidate in check_candidates:
                check.candidates.add(candidate)
        
        # Update verified_amount in board table
        check.board.verified_amount += 1
        check.board.save() 
        return check

class CheckMultiBoardsDeserializer(serializers.Serializer):
    is_board = serializers.ListField(
        child = serializers.PrimaryKeyRelatedField(queryset=Boards.objects.all())
    )
    not_board = serializers.ListField(
        child = serializers.PrimaryKeyRelatedField(queryset=Boards.objects.all())
    )
    created_by = serializers.UUIDField(required=True)

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        valid_boards = validated_data.get('is_board', [])
        invalid_boards = validated_data.get('not_board', [])
        created_by = validated_data.get('created_by','')
        
        if valid_boards:
            for board in valid_boards:
                check = Checks(**{'board':board, 'is_board': True, 'created_by': created_by, 'type': 2})
                check.save()

        if invalid_boards:
            for board in invalid_boards:
                check = Checks(**{'board':board, 'is_board': False, 'created_by': created_by, 'type': 2})
                check.save()

        return validated_data

class GetSingleCheckBoardSerializer(serializers.ModelSerializer):

    slogan = serializers.CharField()
    candidates = BoardsTermsSerializer(many=True,read_only=True)

    class Meta:
        model = Boards
        fields = ('id', 'candidates', 'image', 'verified_amount', 'uploaded_by', 'slogan')
