from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .models import Menu, Chef, TipoMenu, Restaurante, Plato, DetalleMenu


class PaginaCrearMenu(CreateView):
    model = Menu
    template_name = 'crearMenu/home.html'
    fields = ['nombre', 'chef', 'tipo_menu', 'restaurante']

    def get_success_url(self):
        # self.object es el Menú que se acaba de crear
        # Redirigimos a la nueva URL pasándole el ID del menú
        return reverse('crearMenu:gestionar_detalle_menu', kwargs={'menu_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menus'] = Menu.objects.all()
        return context

# --- ¡NUEVA VISTA PARA LA PÁGINA 2! ---


def gestionar_detalle_menu(request, menu_id):
    # Obtenemos el Menú (maestro) con el que estamos trabajando
    try:
        menu = Menu.objects.get(pk=menu_id)
    except Menu.DoesNotExist:
        # Manejar error si el menú no existe
        return redirect('crearMenu:crear_menu')

    # Lógica para AÑADIR un nuevo plato (DetalleMenu)
    if request.method == 'POST':
        # Obtenemos los datos del formulario de "Añadir Plato"
        id_plato = request.POST.get('plato')
        precio = request.POST.get('precio')

        if id_plato and precio:
            plato = Plato.objects.get(pk=id_plato)

            # Creamos el registro de DETALLE
            DetalleMenu.objects.create(
                menu=menu,
                plato=plato,
                precio=precio
            )
            # Redirigimos a la misma página para que se actualice la tabla
            return redirect('crearMenu:gestionar_detalle_menu', menu_id=menu_id)

    # Lógica para MOSTRAR la página (GET)

    # 1. Traemos los platos ya añadidos a ESTE menú
    detalles_del_menu = DetalleMenu.objects.filter(menu=menu)

    # 2. Traemos TODOS los platos disponibles para el dropdown
    todos_los_platos = Plato.objects.all()

    context = {
        'menu': menu,  # El menú que estamos editando
        'detalles': detalles_del_menu,  # La tabla de platos ya añadidos
        'platos_disponibles': todos_los_platos,  # Para el dropdown
    }

    return render(request, 'crearMenu/detalle_menu.html', context)


def imprimir_menu_pdf(request, menu_id):
    """
    Toma un menu_id, renderiza una plantilla HTML con los detalles
    de ese menú y la devuelve como un PDF descargable.
    """

    # 1. Obtener los datos necesarios
    try:
        menu = Menu.objects.get(pk=menu_id)
        # Trae todos los platos y precios de ESE menú
        detalles = DetalleMenu.objects.filter(
            menu=menu).order_by('plato__nombre')
    except Menu.DoesNotExist:
        return HttpResponse("Menú no encontrado", status=404)

    # 2. Definir el contexto para la plantilla
    context = {
        'menu': menu,
        'detalles': detalles,  # La lista de objetos DetalleMenu
    }

    # 3. Cargar la plantilla HTML que crearemos a continuación
    template_path = 'crearMenu/menu_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    # 4. Crear la respuesta PDF
    response = HttpResponse(content_type='application/pdf')

    # 5. Configurar el nombre del archivo PDF
    # (reemplazamos espacios para evitar problemas en nombres de archivo)
    filename = f"Menu_{menu.nombre.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # 6. Generar el PDF usando xhtml2pdf
    pisa_status = pisa.CreatePDF(
        html,                # El string HTML renderizado
        dest=response)       # El objeto HttpResponse donde se escribirá el PDF

    # 7. Manejar errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err)

    # 8. Devolver el PDF
    return response
