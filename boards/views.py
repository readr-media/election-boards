from rest_framework import viewsets, mixins, views, response, status
from .models import Boards, Checks
from .serializers import BoardsGetSerializer, BoardsPostSerializer, CheckBoardDeserializer
from drf_yasg.utils import swagger_auto_schema

class BoardsList(views.APIView):
    permission_classes = []

    @swagger_auto_schema(responses={200: BoardsGetSerializer(many=True)})
    def get(self, request, format=None):
        boards = Boards.objects.all()
        serializer = BoardsGetSerializer(boards, many=True) 
        return response.Response(serializer.data)

    @swagger_auto_schema(query_serializer=BoardsPostSerializer, responses={201:BoardsPostSerializer})
    def post(self, request, format=None):
        serializer = BoardsPostSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckBoardView(views.APIView):
    permission_classes = []

    # Return single board with minimum verified_amount, uploaded earliest
    # And rule out specific user by using ?user=[UUID]
    @swagger_auto_schema(responses={200: BoardsGetSerializer})
    def get(self, request):
        user = request.query_params.get('user', None)
        board = Boards.objects.exclude(uploaded_by=user).order_by('verified_amount', 'uploaded_at')[0]
        serializer = BoardsGetSerializer(board)
        return response.Response(serializer.data)
    
    @swagger_auto_schema(query_serializer=CheckBoardDeserializer, responses={201:CheckBoardDeserializer})
    def post(self, request):
        serializer = CheckBoardDeserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
