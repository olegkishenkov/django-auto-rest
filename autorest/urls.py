from django.urls import path

from autorest import views

urlpatterns = [
    path('<str:model_name_plural>/', views.pre_view),
    path('<str:model_name_plural>/<int:pk>', views.pre_view),
]