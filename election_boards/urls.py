"""election_boards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include

from rest_framework import routers
from candidates.views import CandidatesTermsViewSet
from councilors.views import CouncilorsDetailViewSet
from elections.views import ElectionsViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'candidates_terms', CandidatesTermsViewSet)
router.register(r'councilors_terms', CouncilorsDetailViewSet)
router.register(r'elections', ElectionsViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Election Boards API",
      default_version='v2',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(),
)


urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api/', include('boards.urls')),
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]