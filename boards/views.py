from rest_framework import viewsets, views, response, status, mixins
from .models import Boards, Checks
from .serializers import MultiBoardsSerializer, MultiBoardsDeserializer, SingleCheckDeserializer, MultiChecksDeserializer, SingleCheckSerializer
from .filters import BoardsFilter, SingleCheckFilter
from app.filters import MaxResults

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import Max

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

class MultiBoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    permission_classes = []
    pagination_class = MaxResults 
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
        """
        Order boards by verified_amount and uploaded_at, then get the first board to request

        If there is no board, just filter uploaded_by and skip_board id if there is any, 
        and present the first board
        """

        queryset = self.filter_queryset(self.get_queryset())
        # If nothing selected(reach the end), sql query again and start from beginning
        if not queryset.exists():
            # Manually apply board id and uploaded_by restrictions
            # for starting over query
            queryset = self.get_queryset()
            u_b = self.request.query_params.get('uploaded_by', None)
            if u_b is not None:
                queryset = queryset.exclude(uploaded_by=u_b)
            s_b = self.request.query_params.get('skip_board', None)
            if s_b is not None:
                queryset = queryset.exclude(id=s_b)
        
        # Only show first board to check by spec
        serializer = self.get_serializer(queryset[0])

        return response.Response(serializer.data)

    def get_queryset(self):
        return Boards.objects.order_by('verified_amount', 'uploaded_at')
 
    def get_serializer_class(self):
        if self.action == 'create':
            return SingleCheckDeserializer
        return SingleCheckSerializer

class MultiChecksViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = MultiChecksDeserializer

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def gongde_list(request, format=None):
    name_list = Boards.objects.exclude(uploader_name__exact='').values_list('uploader_name', flat=True).distinct().order_by()
    results = {'results': name_list}
    return response.Response(results)