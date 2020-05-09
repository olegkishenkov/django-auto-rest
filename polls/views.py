import copy

from django.core.exceptions import ValidationError
from rest_framework import viewsets

from polls.models import Question
from polls.serializers import QuestionSerializer


class GETparamsViewSet(viewsets.ModelViewSet):
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


class QuestionViewSet(GETparamsViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
