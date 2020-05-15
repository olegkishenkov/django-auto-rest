from django.urls import path

from . import views

urlpatterns = [
    path('<str:model_name_plural>/', views.pre_view, name='model-list'),
    path('<str:model_name_plural>/<int:pk>', views.pre_view, name='model-detail'),
]