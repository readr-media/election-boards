from django.urls import path, re_path
from .views import MultiBoardsViewSet, SingleCheckViewSet, MultiChecksViewSet

app_name = 'boards'

urlpatterns = [
    path('boards/', MultiBoardsViewSet.as_view({'get':'list', 'post':'create'})),
    path('verify/board', SingleCheckViewSet.as_view({'get':'list', 'post':'create'})),
    path('verify/board/<int:pk>', SingleCheckViewSet.as_view({'get':'retrieve'})),
    path('verify/boards', MultiChecksViewSet.as_view({'post':'create'})),
]