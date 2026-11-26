from rest_framework import serializers

from .models import (
    Equipment,
    Usuario,
    Terreno,
    Vivienda,
    PuntoAcceso,
    Residente
)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id", "code", "name", "is_available")


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
        read_only_fields = ("cuenta",)


class TerrenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terreno
        fields = "__all__"


class ViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vivienda
        fields = "__all__"


class PuntoAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoAcceso
        fields = "__all__"


class ResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residente
        fields = "__all__"
        validators = []

    def validate(self, attrs):
        usuario = attrs.get("usuario")
        vivienda = attrs.get("vivienda")

        if not usuario.estado or not vivienda.estado or not vivienda.terreno.estado:
            raise serializers.ValidationError(
                "La persona, vivienda y terreno deben estar activos."
            )

        if Residente.objects.filter(
            usuario=usuario,
            vivienda=vivienda
        ).exists():
            raise serializers.ValidationError(
                "La persona ya está asignada a esta vivienda."
            )

        return attrs