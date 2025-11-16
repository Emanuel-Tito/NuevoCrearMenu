# crearMenu/admin.py
from django.contrib import admin
from . import models

admin.site.register(models.TipoMenu)
admin.site.register(models.Categoria)
admin.site.register(models.Ingrediente)
admin.site.register(models.Ciudad)
admin.site.register(models.Restaurante)
admin.site.register(models.Chef)
admin.site.register(models.Receta)
admin.site.register(models.Plato)
admin.site.register(models.Menu)
admin.site.register(models.DetalleIngrediente)
admin.site.register(models.DetalleMenu)
admin.site.register(models.DetalleNutricional)
