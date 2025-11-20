from django.urls import path
from . import views

app_name = 'crearMenu'

urlpatterns = [
    # --- PÁGINA DE INICIO Y MENÚS ---
    path('', views.PaginaCrearMenu.as_view(), name='crear_menu'),
    path('menu/<int:menu_id>/detalle/', views.gestionar_detalle_menu,
         name='gestionar_detalle_menu'),
    path('menu/eliminar/<int:menu_id>/',
         views.eliminar_menu, name='eliminar_menu'),
    path('menu/<int:menu_id>/imprimir/',
         views.imprimir_menu_pdf, name='imprimir_menu_pdf'),
    path('detalle/eliminar/<int:detalle_id>/',
         views.eliminar_detalle_menu, name='eliminar_detalle'),

    # --- GESTIÓN DE PLATOS ---
    path('crear-plato/', views.crear_plato, name='crear_plato'),
    path('platos/', views.lista_platos, name='lista_platos'),
    path('platos/editar/<int:plato_id>/',
         views.editar_plato, name='editar_plato'),
    path('platos/eliminar/<int:plato_id>/', views.eliminar_plato,
         name='eliminar_plato'),  # Faltaba esta

    # --- GESTIÓN DE CATEGORÍAS
    path('crear-categoria/', views.lista_categorias, name='crear_categoria'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/editar/<int:categoria_id>/',
         views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/',
         views.eliminar_categoria, name='eliminar_categoria'),

    # --- GESTIÓN DE INGREDIENTES ---
    path('ingredientes/', views.lista_ingredientes, name='lista_ingredientes'),
    path('ingredientes/eliminar/<int:ingrediente_id>/',
         views.eliminar_ingrediente, name='eliminar_ingrediente'),

    # --- GESTIÓN DE RECETAS ---
    path('recetas/', views.lista_recetas, name='lista_recetas'),
    path('recetas/crear/', views.crear_receta, name='crear_receta'),
    path('recetas/<int:receta_id>/gestionar/',
         views.gestionar_receta, name='gestionar_receta'),
    path('recetas/eliminar/<int:receta_id>/',
         views.eliminar_receta, name='eliminar_receta'),
    path('recetas/detalle/eliminar/<int:detalle_id>/',
         views.eliminar_detalle_ingrediente, name='eliminar_detalle_ingrediente'),

    # --- GESTIÓN DE CHEFS ---
    path('chefs/', views.lista_chefs, name='lista_chefs'),
    path('chefs/crear/', views.crear_chef, name='crear_chef'),
    path('chefs/editar/<int:chef_id>/', views.editar_chef, name='editar_chef'),
    path('chefs/eliminar/<int:chef_id>/',
         views.eliminar_chef, name='eliminar_chef'),

    # --- GESTIÓN DE CIUDADES ---
    path('ciudades/', views.lista_ciudades, name='lista_ciudades'),
    path('ciudades/eliminar/<int:ciudad_id>/',
         views.eliminar_ciudad, name='eliminar_ciudad'),

    # --- GESTIÓN DE TIPOS DE MENÚ ---
    path('tipos-menu/', views.lista_tipos_menu, name='lista_tipos_menu'),
    path('tipos-menu/eliminar/<int:tipo_id>/',
         views.eliminar_tipo_menu, name='eliminar_tipo_menu'),

    # --- GESTIÓN DE RESTAURANTES ---
    path('restaurantes/', views.lista_restaurantes, name='lista_restaurantes'),
    path('restaurantes/eliminar/<int:restaurante_id>/',
         views.eliminar_restaurante, name='eliminar_restaurante'),
]
