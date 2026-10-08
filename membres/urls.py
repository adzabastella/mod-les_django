
from django.urls import path, register_converter
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r"membres", EmprunteurViewSet, basename="membre")

urlpatterns = [
    path("", include(router.urls)),
]

