from rest_framework import viewsets, views, response, status, mixins
from .models import Boards, Checks
from .serializers import MultiBoardsSerializer, MultiBoardsDeserializer, SingleCheckDeserializer, MultiChecksDeserializer, SingleCheckSerializer
from rest_framework.pagination import PageNumberPagination
from .filters import BoardsFilter, SingleCheckFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import Max

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

class MultiBoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    permission_classes = []
    pagination_class = BoardsPagination 
    filter_class = BoardsFilter 

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('coordinates', openapi.IN_QUERY, description="Coordinates format in (latitude lontitude)", type=openapi.TYPE_STRING),
        openapi.Parameter('radius', openapi.IN_QUERY, description="Radius from coordinates, default to 100m", type=openapi.TYPE_INTEGER),
        openapi.Parameter('uploaded_by', openapi.IN_QUERY, description="Exclude boards uploaded by this user", type=openapi.TYPE_STRING),
        openapi.Parameter('verified_amount', openapi.IN_QUERY, description="Return boards with verified_amount >= [verified_amount]", type=openapi.TYPE_INTEGER),
        openapi.Parameter('not_board_amount', openapi.IN_QUERY, description="Return boards which is evaluated as not board <= [not_board_amount]", type=openapi.TYPE_INTEGER)])
    def list(self, request):
        return super(MultiBoardsViewSet, self).list(request)

    def get_serializer_class(self):
        if self.action == 'list':
            return MultiBoardsSerializer
        elif self.action == 'create':
            return MultiBoardsDeserializer
        return MultiBoardsSerializer

# class SingleCheckViewSet(viewsets.ModelViewSet):
class SingleCheckViewSet(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    queryset = Boards.objects.order_by('verified_amount', 'uploaded_at')
    permission_classes = []
    pagination_class = None
    filterset_class = SingleCheckFilter

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('uploaded_by', openapi.IN_QUERY, description="exclude boards uploaded by [uploaded_by]", type=openapi.TYPE_STRING),
        openapi.Parameter('skip_board', openapi.IN_QUERY, description="Skip board with id prior to [skip_board]", type=openapi.TYPE_INTEGER)])
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        # If nothing selected(reach the end), sql query again and start from beginning
        if queryset.count() == 0:
            serializer = self.get_serializer(self.get_queryset()[0])
        else:
            # only return the first one
            serializer = self.get_serializer(queryset[0])
        return response.Response(serializer.data)

    def get_queryset(self):
        qs = Boards.objects.order_by('verified_amount', 'uploaded_at')
        if self.action == 'list' or self.action == 'retrieve':
            qs = Boards.objects.annotate(slogan=Max('board_checks__slogan')).order_by('verified_amount', 'uploaded_at')
        return qs
            
    def get_serializer_class(self):
        if self.action == 'create':
            return SingleCheckDeserializer
        return SingleCheckSerializer

class MultiChecksViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = MultiChecksDeserializer
