from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from polls.views import QuestionViewSet

router = routers.DefaultRouter()
router.register(r'question', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]