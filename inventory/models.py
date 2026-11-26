from django.conf import settings
from django.db import models


class Equipment(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)


class Usuario(models.Model):
    cuenta = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Terreno(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)

    administradores = models.ManyToManyField(
        Usuario,
        blank=True,
        related_name="terrenos_administrados"
    )

    def __str__(self):
        return self.nombre


class Vivienda(models.Model):
    terreno = models.ForeignKey(
        Terreno,
        on_delete=models.PROTECT
    )
    numero = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["terreno", "numero"],
                name="vivienda_unica_terreno"
            )
        ]

    def __str__(self):
        return f"{self.terreno} - Vivienda {self.numero}"


class PuntoAcceso(models.Model):
    terreno = models.ForeignKey(
        Terreno,
        on_delete=models.PROTECT
    )
    nombre = models.CharField(max_length=100)
    hora_desde = models.TimeField()
    hora_hasta = models.TimeField()

    def __str__(self):
        return self.nombre


class Residente(models.Model):
    PROPIETARIO_ADMIN = "PROPIETARIO_ADMIN"
    PROPIETARIO = "PROPIETARIO"
    ARRENDATARIO = "ARRENDATARIO"

    TIPOS = [
        (PROPIETARIO_ADMIN, "Propietario administrador"),
        (PROPIETARIO, "Propietario"),
        (ARRENDATARIO, "Arrendatario"),
    ]

    vivienda = models.ForeignKey(
        Vivienda,
        on_delete=models.PROTECT
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT
    )
    rol_residente = models.CharField(
        max_length=30,
        choices=TIPOS
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "vivienda"],
                name="residente_unico_vivienda"
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.vivienda}"