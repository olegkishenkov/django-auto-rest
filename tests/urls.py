from django.urls import path, include

urlpatterns = [
    path('', include('auto_rest.urls')),
]
