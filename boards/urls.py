from django.urls import path, re_path
from .views import BoardsList, CheckBoardView

app_name = 'boards'

urlpatterns = [
    path('boards/', BoardsList.as_view()),
    path('verify/board', CheckBoardView.as_view()),
]