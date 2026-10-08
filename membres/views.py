from django.shortcuts import render
from rest_framework import viewsets


# Create your views here.
from rest_framework import permissions
from bibliotheque.models import *
from bibliotheque.serializers import *

class IsEmprunteurOuReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # safe nethod corresponds to basic methods like get ,patch and options
            return True
        return obj.emprunteur.user == request.user

class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Emprunt.objects.select_related("emprunteur", "livre")
    serializer_class = EmpruntSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmprunteurOuReadOnly]