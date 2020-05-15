import copy

import django.apps
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.serializers import HyperlinkedModelSerializer


def _single_from_plural(s):
    return s.rstrip('ies') + 'y' if s.endswith('ies') else s.rstrip('s')


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


def pre_view(request, model_name_plural, **kwargs):
    autorest_not_installed = getattr(django.conf.settings, 'AUTOREST_NOT_INSTALLED', None)
    if autorest_not_installed:
        return HttpResponse(
            'automatic REST API not implemented',
            status=501,
            reason='automatic REST API not implemented',
        )

    # TODO: allow for identical model names in different apps
    models = django.apps.apps.get_models()
    model, model_name, model_class_name = None, None, None
    for model_ in models:
        if model_._meta.model_name == _single_from_plural(model_name_plural):
            model, model_name, model_class_name = model_, model_._meta.model_name, model_.__name__
            break
    if not model:
        return HttpResponse('not found', status=404)
    meta_class = type('Meta', (), {
        'model': model,
        'fields': [field.name for field in model._meta.fields]
    })
    serializer_class = type(model_class_name + 'Serializer', (HyperlinkedModelSerializer,), {'Meta': meta_class})
    viewset_class = type(model_class_name + 'ViewSet', (GETparamsViewSet,), {
        'queryset': model.objects.all(),
        'serializer_class': serializer_class
    })
    if not kwargs.get('pk', None):
        view = viewset_class.as_view({'get': 'list', 'post': 'create'})
    else:
        view = viewset_class.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
    return_value = view(request, **kwargs)
    return return_value
