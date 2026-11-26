from django.contrib import admin

from .models import (
    Equipment,
    Usuario,
    Terreno,
    Vivienda,
    PuntoAcceso,
    Residente
)


admin.site.register(Equipment)
admin.site.register(Usuario)
admin.site.register(Terreno)
admin.site.register(Vivienda)
admin.site.register(PuntoAcceso)
admin.site.register(Residente)