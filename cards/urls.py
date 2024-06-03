from django.urls import path
from .views import CardViewSet

urlpatterns = [
    path('', CardViewSet.as_view())
]