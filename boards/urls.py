from django.urls import path, re_path
from .views import BoardsView, CheckView, CheckBoardsViewSet

app_name = 'boards'

urlpatterns = [
    path('boards/', BoardsView.as_view({'get':'list', 'post':'create'})),
    path('verify/board', CheckView.as_view({'get':'list', 'post':'create'})),
    path('verify/board/<int:pk>', CheckView.as_view({'get':'retrieve'})),
    path('verify/boards', CheckBoardsViewSet.as_view({'post':'create'})),
]