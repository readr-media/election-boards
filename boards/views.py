from rest_framework import viewsets
from .models import Boards
from .serializers import BoardsGetSerializer, BoardsPostSerializer

# Create your views here.
class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    # serializer_class = BoardsSerializer
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardsGetSerializer
        elif self.action == 'create':
            return BoardsPostSerializer