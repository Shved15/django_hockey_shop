from django.urls import include, path
from rest_framework import routers

from api.views import BagModelViewSet, ProductModelViewSet

app_name = 'api'

# Initialize the router and register views
router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'bags', BagModelViewSet)

urlpatterns = [
    # Enable routes from the router
    path('', include(router.urls)),
]
