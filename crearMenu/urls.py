from django.urls import path
from . import views

app_name = 'crearMenu'

urlpatterns = [
    path('', views.PaginaCrearMenu.as_view(), name='crear_menu'),
    path('menu/<int:menu_id>/detalle/', views.gestionar_detalle_menu,
         name='gestionar_detalle_menu'),
    path('menu/<int:menu_id>/imprimir/',
         views.imprimir_menu_pdf, name='imprimir_menu_pdf'),
]
