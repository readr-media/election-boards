from django.urls import path, re_path
from .views import BoardsView, CheckBoardView

app_name = 'boards'

urlpatterns = [
    path('boards/', BoardsView.as_view({'get':'list', 'post':'create'})),
    path('verify/board', CheckBoardView.as_view()),
]