from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Equipment
from .serializers import EquipmentSerializer
from rest_framework.permissions import IsAuthenticated

class EquipmentViewSet(ModelViewSet):
    queryset = Equipment.objects.order_by("id")
    serializer_class = EquipmentSerializer


class ViviendaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # Mantener queryset y serializer_class del proyecto.