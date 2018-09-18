from rest_framework import viewsets, views, response, status
from .models import Boards, Checks
from .serializers import BoardsGetSerializer, BoardsPostSerializer, CheckBoardDeserializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination

class BoardsPagination(PageNumberPagination):
    """
    BoardsPagination is used to override default pagination settings for boards.
    Included:
    max_results - url query paramteters to adjust return amounts of board results 
    page - default pagination query parameters
    """
    page_size = 20
    page_size_query_param = 'max_results'
    max_page_size = 30

class BoardsView(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    permission_classes = []
    pagination_class = BoardsPagination 

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardsGetSerializer
        elif self.action == 'create':
            return BoardsPostSerializer
        return BoardsGetSerializer

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
