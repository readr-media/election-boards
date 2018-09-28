from rest_framework import viewsets, views, response, status, mixins
from .models import Boards, Checks
from .serializers import BoardsGetSerializer, BoardsPostSerializer, CheckBoardDeserializer, CheckMultiBoardsDeserializer, GetSingleCheckBoardSerializer
from rest_framework.pagination import PageNumberPagination
from .filters import BoardsFilter, SingleCheckFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BoardsPagination(PageNumberPagination):
    permission_classes = []
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
    filter_class = BoardsFilter 

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('coordinates', openapi.IN_QUERY, description="Coordinates format in (latitude lontitude)", type=openapi.TYPE_STRING),
        openapi.Parameter('radius', openapi.IN_QUERY, description="Radius from coordinates, default to 100m", type=openapi.TYPE_INTEGER),
        openapi.Parameter('uploaded_by', openapi.IN_QUERY, description="exclude boards uploaded by this user", type=openapi.TYPE_STRING)])
    def list(self, request):
        return super(BoardsView, self).list(request)

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardsGetSerializer
        elif self.action == 'create':
            return BoardsPostSerializer
        return BoardsGetSerializer

# class CheckView(viewsets.ModelViewSet):
class CheckView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Boards.objects.order_by('verified_amount', 'uploaded_at')
    permission_classes = []
    pagination_class = None
    filterset_class = SingleCheckFilter

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('uploaded_by', openapi.IN_QUERY, description="exclude boards uploaded by user[uuid]", type=openapi.TYPE_STRING)])
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        # If nothing selected(reach the end), sql query again and start from beginning
        if queryset.count() == 0:
            serializer = self.get_serializer(self.get_queryset()[0])
        else:
            # only return the first one
            serializer = self.get_serializer(queryset[0])
        return response.Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return GetSingleCheckBoardSerializer
        elif self.action == 'create':
            return CheckBoardDeserializer
        return BoardsGetSerializer

class CheckBoardsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = CheckMultiBoardsDeserializer