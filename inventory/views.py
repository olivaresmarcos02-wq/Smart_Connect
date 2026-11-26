from django.db import IntegrityError, transaction
from django.db.models import Q
from django.db.models.deletion import ProtectedError

from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import (
    Equipment,
    Usuario,
    Terreno,
    Vivienda,
    PuntoAcceso,
    Residente
)

from .serializers import (
    EquipmentSerializer,
    UsuarioSerializer,
    TerrenoSerializer,
    ViviendaSerializer,
    PuntoAccesoSerializer,
    ResidenteSerializer
)


def persona(request):
    return Usuario.objects.filter(
        cuenta=request.user,
        estado=True
    ).first()


def administrador(request):
    return request.user.is_staff


def viviendas_administradas(request):
    p = persona(request)

    if p is None:
        return Vivienda.objects.none()

    return Vivienda.objects.filter(
        estado=True,
        terreno__estado=True
    ).filter(
        Q(terreno__administradores=p) |
        Q(
            residente__usuario=p,
            residente__rol_residente=Residente.PROPIETARIO_ADMIN
        )
    ).distinct()


def viviendas_visibles(request):
    p = persona(request)

    if p is None:
        return Vivienda.objects.none()

    return Vivienda.objects.filter(
        estado=True,
        terreno__estado=True
    ).filter(
        Q(pk__in=viviendas_administradas(request)) |
        Q(residente__usuario=p)
    ).distinct()


class EquipmentViewSet(ModelViewSet):
    queryset = Equipment.objects.order_by("id")
    serializer_class = EquipmentSerializer


class MaestroViewSet(ModelViewSet):

    def get_queryset(self):
        qs = super().get_queryset()

        if administrador(self.request) or self.action != "list":
            return qs

        return qs.filter(
            pk__in=self.visibles()
        ).distinct()

    def get_object(self):
        obj = super().get_object()

        if not administrador(self.request):
            if self.action != "retrieve" or not self.visibles().filter(pk=obj.pk).exists():
                raise PermissionDenied(
                    "No tiene permiso sobre este recurso."
                )

        return obj

    def create(self, request, *args, **kwargs):
        if not administrador(request):
            raise PermissionDenied(
                "Solo el administrador general puede crear maestros."
            )

        return super().create(request, *args, **kwargs)

    def perform_destroy(self, instance):
        try:
            instance.delete()

        except ProtectedError:
            raise ValidationError(
                "No se puede eliminar: existen registros relacionados."
            )


class UsuarioViewSet(MaestroViewSet):
    queryset = Usuario.objects.order_by("id")
    serializer_class = UsuarioSerializer

    def visibles(self):
        p = persona(self.request)

        if p is None:
            return Usuario.objects.none()

        return Usuario.objects.filter(
            Q(pk=p.pk) |
            Q(
                residente__vivienda__in=viviendas_administradas(
                    self.request
                )
            )
        ).distinct()


class TerrenoViewSet(MaestroViewSet):
    queryset = Terreno.objects.order_by("id")
    serializer_class = TerrenoSerializer

    def visibles(self):
        p = persona(self.request)

        if p is None:
            return Terreno.objects.none()

        return Terreno.objects.filter(
            estado=True
        ).filter(
            Q(administradores=p) |
            Q(vivienda__in=viviendas_visibles(self.request))
        ).distinct()


class ViviendaViewSet(MaestroViewSet):
    queryset = Vivienda.objects.order_by("id")
    serializer_class = ViviendaSerializer

    def visibles(self):
        return viviendas_visibles(self.request)


class PuntoAccesoViewSet(MaestroViewSet):
    queryset = PuntoAcceso.objects.order_by("id")
    serializer_class = PuntoAccesoSerializer

    def visibles(self):
        p = persona(self.request)

        if p is None:
            return PuntoAcceso.objects.none()

        return PuntoAcceso.objects.filter(
            terreno__estado=True
        ).filter(
            Q(terreno__administradores=p) |
            Q(
                terreno__vivienda__in=viviendas_visibles(
                    self.request
                )
            )
        ).distinct()


class ResidenteViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Residente.objects.order_by("id")
    serializer_class = ResidenteSerializer

    def visibles(self):
        p = persona(self.request)

        if p is None:
            return Residente.objects.none()

        return Residente.objects.filter(
            Q(vivienda__in=viviendas_administradas(self.request)) |
            Q(
                usuario=p,
                vivienda__in=viviendas_visibles(self.request)
            )
        ).distinct()

    def get_queryset(self):
        if administrador(self.request) or self.action != "list":
            return self.queryset

        return self.visibles().order_by("id")

    def get_object(self):
        obj = super().get_object()

        if not administrador(self.request):
            if not self.visibles().filter(pk=obj.pk).exists():
                raise PermissionDenied(
                    "No tiene permiso sobre este residente."
                )

        return obj

    def create(self, request, *args, **kwargs):

        if not administrador(request):

            try:
                vivienda_id = int(request.data.get("vivienda"))

            except (TypeError, ValueError, OverflowError):
                raise ValidationError({
                    "vivienda": "Indique un identificador válido."
                })

            if not viviendas_administradas(request).filter(
                pk=vivienda_id
            ).exists():
                raise PermissionDenied(
                    "No administra esta vivienda."
                )

            if request.data.get("rol_residente") == Residente.PROPIETARIO_ADMIN:
                raise PermissionDenied(
                    "Solo el administrador general puede conceder este rol."
                )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()

        except IntegrityError:
            raise ValidationError(
                "No se pudo guardar la asignación: compruebe que no esté duplicada."
            )