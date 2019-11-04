from rest_framework import serializers
from .models import Boards, Checks
from candidates.models import Candidates, Terms
from datetime import datetime
from django.contrib.gis.geos import Point
from django.db.models import Max, Count
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
        fields = ('id', 'uid', 'election_year', 'type', 'county', 'district', 'name', 'party', 'number', 'image')

class MultiBoardsSerializer(serializers.ModelSerializer):
    candidates = BoardsTermsSerializer(many=True, read_only=True)
    coordinates = CoordinatesField()

    class Meta:
        model = Boards
        fields = '__all__'

class MultiBoardsDeserializer(serializers.ModelSerializer):
    candidates = serializers.PrimaryKeyRelatedField(many=True, queryset=Terms.objects.all())
    took_at = TimestampField()
    uploaded_by = serializers.UUIDField(format='hex_verbose')
    coordinates = CoordinatesField()

    class Meta:
        model = Boards
        fields = '__all__'

    def create(self, validated_data):
        # Create a board
        board_candidates = validated_data.pop('candidates')
        board = Boards.objects.create(**validated_data)

        check = Checks(board=board, is_board=True, is_original=True, headcount=len(board_candidates), created_at = board.uploaded_at, created_by=board.uploaded_by)
        check.save()

        # Create relationship
        for candidate in board_candidates:
            board.candidates.add(candidate)
            check.candidates.add(candidate)

        return board

class SingleCheckDeserializer(serializers.ModelSerializer):

    board = serializers.PrimaryKeyRelatedField(queryset=Boards.objects.all())
    candidates = serializers.PrimaryKeyRelatedField(many=True, queryset=Terms.objects.all(), required=False)
    created_by = serializers.UUIDField(format='hex_verbose')
    is_board = serializers.BooleanField(required=True)
    is_original = serializers.NullBooleanField(required=False)
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
        # Invalidate is_original field
        if 'is_original' in validated_data and validated_data['is_original'] == True:
            validated_data['is_original'] = False
        check = Checks.objects.create(**validated_data)

        # If there are denoted candidates, create relationship
        if check_candidates:
            for candidate in check_candidates:
                check.candidates.add(candidate)

        # Update verified_amount in board table
        check.board.verified_amount += 1
        check.board.save()

        # Select most headcount number 'headcount_max'
        # If headcount_max is None, then choose the original length
        headcount_max = Checks.objects.filter(board=validated_data['board'], is_original=False).aggregate(Max('headcount'))
        headcount_max = headcount_max['headcount__max']

        if headcount_max is None:
            headcount_max = Checks.objects.filter(board=validated_data['board'], is_original=True).only('headcount')[0].headcount
        # Count how many times a board is identified belonging to a candidates.
        # If the counts equals, sort them with created_at
        # The original answer is counted as a verification
        most_candidates = [p['candidates__id'] for p in Checks.objects.filter(board=validated_data['board']) \
            .values('candidates__id').annotate(verify_frequency=Count('candidates__id'), last_update=Max('created_at')).order_by('-verify_frequency','-last_update') \
            if p['candidates__id'] is not None and p['verify_frequency'] != 0]

        if headcount_max > 0:
            if len(most_candidates) > headcount_max:
                most_candidates = most_candidates[:headcount_max]
            # Update boards_boards_candidates to connect this boards with only most
            # frequent candidates
            validated_data['board'].candidates.clear()
            for candidate in most_candidates:
                validated_data['board'].candidates.add(candidate)
        return check

class MultiChecksDeserializer(serializers.Serializer):
    """Convert input when validate multiple boards"""
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
                check = Checks(**{'board':board, 'is_board': True, 'created_by': created_by, 'type': 2, 'is_original': False})
                check.save()

        if invalid_boards:
            for board in invalid_boards:
                check = Checks(**{'board':board, 'is_board': False, 'created_by': created_by, 'type': 2, 'is_original': False})
                check.save()

                # ib = Boards.objects.get(pk=board)
                board.not_board_amount += 1
                board.save()
                
        return validated_data

class SingleCheckSerializer(serializers.ModelSerializer):

    slogan = serializers.CharField()
    candidates = BoardsTermsSerializer(many=True,read_only=True)

    class Meta:
        model = Boards
        fields = ('id', 'candidates', 'image', 'verified_amount',
                  'uploaded_by', 'slogan', 'party_icon', 'board_type')
