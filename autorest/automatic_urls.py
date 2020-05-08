# Serializers define the API representation.
import copy

from django.conf.urls import url
from django.core.exceptions import ValidationError
from django.urls import include
from rest_framework import serializers, viewsets, routers

from django.contrib.auth.models import User
from polls.models import Question


class GETparmasViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = copy.deepcopy(dict(self.request.query_params))
        try:
            order_by = query_params.pop('order_by')[0]
        except KeyError:
            order_by = None
        try:
            limit = int(query_params.pop('limit')[0])
            if limit < 0:
                limit = None
        except (KeyError, ValueError):
            limit = None
        for key in query_params.keys():
            query_params[key] = query_params[key][0]
        try:
            queryset = queryset.filter(**query_params)
        except ValidationError:
            pass
        if order_by:
            queryset = queryset.order_by(order_by)
        if limit:
            queryset = queryset[:limit]
        return queryset


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']


# ViewSets define the view behavior.
class UserViewSet(GETparmasViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QuestionViewSet(GETparmasViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
