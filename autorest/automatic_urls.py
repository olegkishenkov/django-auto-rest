# Serializers define the API representation.
from django.conf.urls import url
from django.urls import include
from rest_framework import serializers, viewsets, routers

from django.contrib.auth.models import User
from polls.models import Question


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        id, order_by, limit = map(lambda _: self.request.query_params.get(_), ('id', 'order_by', 'limit'))
        try:
            limit = int(limit)
        except ValueError:
            limit = None
        if id:
            queryset = queryset.filter(id=id)
        if order_by:
            queryset = queryset.order_by(order_by)
        if limit:
            queryset = queryset[:limit]
        return queryset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
