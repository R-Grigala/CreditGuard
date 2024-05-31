from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CardViewSet

# Create a router and register the CardViewSet with it
router = DefaultRouter()
router.register(r'cards', CardViewSet, basename='card')

# Wire up our API using automatic URL routing
# Additionally, we include login URLs for the browsable API
urlpatterns = [
    path('', include(router.urls)),
]
