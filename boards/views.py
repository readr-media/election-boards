from rest_framework import viewsets, mixins, views, response, status
from .models import Boards, Checks
from .serializers import BoardsGetSerializer, BoardsPostSerializer, CheckBoardDeserializer 

class BoardsList(views.APIView):
    permission_classes = []

    def get(self, request, format=None):
        boards = Boards.objects.all()
        serializer = BoardsGetSerializer(boards, many=True) 
        return response.Response(serializer.data)
    
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
    def get(self, request):
        user = request.query_params.get('user', None)
        board = Boards.objects.exclude(uploaded_by=user).order_by('verified_amount', 'uploaded_at')[0]
        serializer = BoardsGetSerializer(board)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = CheckBoardDeserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################### ViewSet implementation. Deprecated. ####################
# Create your views here.
class BoardsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsGetSerializer
    permission_classes = []

class SingleBoardViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Boards.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardsGetSerializer
        elif self.action == 'create':
            return BoardsPostSerializer
        return BoardsGetSerializer
