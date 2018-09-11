from rest_framework import viewsets, mixins
from .models import Boards
from .serializers import BoardsGetSerializer, BoardsPostSerializer

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