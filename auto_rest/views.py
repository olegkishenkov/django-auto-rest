from copy import copy

import django.apps
from django.db.models import ForeignKey
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer


def _single_from_plural(s):
    return s.rstrip('ies') + 'y' if s.endswith('ies') else s.rstrip('s')

def _plural_from_singular(s):
    return s.rstrip('y') + 'ies' if s.endswith('y') else s + 's'


class GETparamsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()

        # order_by = self.request.query_params.get('order_by', None)
        #
        # limit = self.request.query_params.get('limit', None)
        # if (limit is not None) and (not limit.isnumeric() or int(limit) < 0):
        #     limit = None
        # else:
        #     limit = int(limit)
        #
        # query_params = {key: value for key, value in dict(self.request.query_params).items() if key not in ('order_by', 'limit')}

        query_params = copy(dict(self.request.query_params))
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


def make_serializer_class(model):
    fk_related_models = [field.related_model for field in model._meta.fields if isinstance(field, ForeignKey)]

    fields = {}
    fields_for_meta = [field.name for field in model._meta.fields]
    for model_ in fk_related_models:
        fields.update({model_._meta.model_name: AutoHyperlinkedRelatedField(
            read_only=True,
            view_name='model-detail',
        )})

    meta_class = type('Meta', (), {
        'model': model,
        'fields': fields_for_meta,
    })
    serializer_class = type(
        model.__name__ + 'Serializer',
        (HyperlinkedModelSerializer, ),
        {'Meta': meta_class, **fields},
    )

    return serializer_class


def make_viewset_class(model):
    serializer_class = make_serializer_class(model)

    viewset_class = type(model.__name__ + 'ViewSet', (GETparamsViewSet,), {
        'queryset': model.objects.all(),
        'serializer_class': serializer_class
    })

    return viewset_class


class AutoHyperlinkedRelatedField(HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {
            'model_name_plural': _plural_from_singular(self.field_name),
            self.lookup_url_kwarg: lookup_value,
        }
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)

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

    viewset_class = make_viewset_class(model)

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
