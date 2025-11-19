from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .models import Ciudad, DetalleNutricional, Menu, Chef, TipoMenu, Restaurante, Plato, DetalleMenu, Ingrediente, Receta, DetalleIngrediente
from django.db.models import Sum, Count, Avg, F
from .forms import CategoriaForm, ChefForm, CiudadForm, PlatoForm, DetalleNutricionalForm, IngredienteForm, RecetaForm, DetalleIngredienteForm, RestauranteForm, TipoMenuForm


class PaginaCrearMenu(CreateView):
    model = Menu
    template_name = 'crearMenu/home.html'
    fields = ['nombre', 'chef', 'tipo_menu', 'restaurante']

    def get_success_url(self):
        return reverse('crearMenu:gestionar_detalle_menu', kwargs={'menu_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menus'] = Menu.objects.all()
        return context


def gestionar_detalle_menu(request, menu_id):
    try:
        menu = Menu.objects.get(pk=menu_id)
    except Menu.DoesNotExist:
        return redirect('crearMenu:crear_menu')

    if request.method == 'POST':
        id_plato = request.POST.get('plato')
        precio = request.POST.get('precio')

        if id_plato and precio:
            plato = Plato.objects.get(pk=id_plato)

            DetalleMenu.objects.create(
                menu=menu,
                plato=plato,
                precio=precio
            )
            return redirect('crearMenu:gestionar_detalle_menu', menu_id=menu_id)
    detalles_del_menu = DetalleMenu.objects.filter(menu=menu)
    todos_los_platos = Plato.objects.all()
    context = {
        'menu': menu,
        'detalles': detalles_del_menu,
        'platos_disponibles': todos_los_platos,
    }
    return render(request, 'crearMenu/detalle_menu.html', context)


def eliminar_menu(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    menu.delete()
    return redirect('crearMenu:crear_menu')


def imprimir_menu_pdf(request, menu_id):
    try:
        menu = Menu.objects.get(pk=menu_id)
        detalles = DetalleMenu.objects.filter(
            menu=menu).order_by('plato__nombre')
    except Menu.DoesNotExist:
        return HttpResponse("Menú no encontrado", status=404)
    context = {
        'menu': menu,
        'detalles': detalles,
    }
    template_path = 'crearMenu/menu_pdf.html'
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"Menu_{menu.nombre.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    pisa_status = pisa.CreatePDF(
        html,
        dest=response)
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err)
    return response


def dashboard_reportes(request):
    menus_con_costo = Menu.objects.annotate(
        costo_total=Sum('detallemenu__precio')
    )
    platos_caloricos = Plato.objects.select_related(
        'detallenutricional').order_by('-detallenutricional__caloria')[:5]
    rendimiento_chefs = Chef.objects.annotate(
        num_menus=Count('menu')
    ).order_by('-num_menus')
    context = {
        'menus_costo': menus_con_costo,
        'platos_caloricos': platos_caloricos,
        'rendimiento_chefs': rendimiento_chefs
    }
    return render(request, 'crearMenu/reportes.html', context)


def eliminar_detalle_menu(request, detalle_id):
    try:
        detalle = DetalleMenu.objects.get(pk=detalle_id)
        menu_id = detalle.menu.pk
        detalle.delete()
    except DetalleMenu.DoesNotExist:
        return redirect('crearMenu:crear_menu')
    return redirect('crearMenu:gestionar_detalle_menu', menu_id=menu_id)


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crearMenu:crear_plato')
    else:
        form = CategoriaForm()
    return render(request, 'crearMenu/crear_categoria.html', {'form': form})


def crear_plato(request):
    if request.method == 'POST':
        plato_form = PlatoForm(request.POST)
        nutri_form = DetalleNutricionalForm(request.POST)

        if plato_form.is_valid() and nutri_form.is_valid():
            plato = plato_form.save()
            nutricion = nutri_form.save(commit=False)
            nutricion.plato = plato
            nutricion.save()
            return redirect('crearMenu:crear_menu')
    else:
        plato_form = PlatoForm()
        nutri_form = DetalleNutricionalForm()
    return render(request, 'crearMenu/crear_plato.html', {
        'plato_form': plato_form,
        'nutri_form': nutri_form
    })


def lista_platos(request):
    platos = Plato.objects.all().order_by('nombre')
    return render(request, 'crearMenu/lista_platos.html', {'platos': platos})


def editar_plato(request, plato_id):
    plato = get_object_or_404(Plato, pk=plato_id)
    try:
        nutricion = plato.detallenutricional
    except DetalleNutricional.DoesNotExist:
        nutricion = None
    if request.method == 'POST':
        plato_form = PlatoForm(request.POST, instance=plato)
        if nutricion:
            nutri_form = DetalleNutricionalForm(
                request.POST, instance=nutricion)
        else:
            nutri_form = DetalleNutricionalForm(request.POST)

        if plato_form.is_valid() and nutri_form.is_valid():
            plato_guardado = plato_form.save()

            nutricion_guardada = nutri_form.save(commit=False)
            nutricion_guardada.plato = plato_guardado
            nutricion_guardada.save()
            return redirect('crearMenu:lista_platos')
    else:
        plato_form = PlatoForm(instance=plato)
        if nutricion:
            nutri_form = DetalleNutricionalForm(instance=nutricion)
        else:
            nutri_form = DetalleNutricionalForm()
    return render(request, 'crearMenu/editar_plato.html', {
        'plato_form': plato_form,
        'nutri_form': nutri_form,
        'plato': plato
    })


def lista_ingredientes(request):
    ingredientes = Ingrediente.objects.all().order_by('nombre')
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crearMenu:lista_ingredientes')
    else:
        form = IngredienteForm()
    return render(request, 'crearMenu/lista_ingredientes.html', {
        'ingredientes': ingredientes,
        'form': form
    })


def eliminar_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, pk=ingrediente_id)
    ingrediente.delete()
    return redirect('crearMenu:lista_ingredientes')


def lista_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'crearMenu/lista_recetas.html', {'recetas': recetas})


def crear_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save()
            # Redirigir a gestionar sus ingredientes inmediatamente
            return redirect('crearMenu:gestionar_receta', receta_id=receta.pk)
    else:
        form = RecetaForm()
    return render(request, 'crearMenu/crear_receta.html', {'form': form})


def gestionar_receta(request, receta_id):
    receta = get_object_or_404(Receta, pk=receta_id)
    if request.method == 'POST':
        form = DetalleIngredienteForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.receta = receta
            detalle.save()
            return redirect('crearMenu:gestionar_receta', receta_id=receta.id_receta)
    else:
        form = DetalleIngredienteForm()
    detalles = DetalleIngrediente.objects.filter(receta=receta)
    return render(request, 'crearMenu/detalle_receta.html', {
        'receta': receta,
        'detalles': detalles,
        'form': form
    })


def eliminar_detalle_ingrediente(request, detalle_id):
    detalle = get_object_or_404(DetalleIngrediente, pk=detalle_id)
    receta_id = detalle.receta.pk
    detalle.delete()
    return redirect('crearMenu:gestionar_receta', receta_id=receta_id)


def lista_chefs(request):
    chefs = Chef.objects.all().order_by('nombre')
    return render(request, 'crearMenu/lista_chefs.html', {'chefs': chefs})


def crear_chef(request):
    if request.method == 'POST':
        form = ChefForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crearMenu:lista_chefs')
    else:
        form = ChefForm()

    return render(request, 'crearMenu/crear_chef.html', {'form': form})


def eliminar_chef(request, chef_id):
    chef = get_object_or_404(Chef, pk=chef_id)
    chef.delete()
    return redirect('crearMenu:lista_chefs')


def lista_ciudades(request):
    ciudades = Ciudad.objects.all().order_by('descripcion')

    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crearMenu:lista_ciudades')
    else:
        form = CiudadForm()

    return render(request, 'crearMenu/lista_ciudades.html', {
        'ciudades': ciudades,
        'form': form
    })


def eliminar_ciudad(request, ciudad_id):
    ciudad = get_object_or_404(Ciudad, pk=ciudad_id)
    ciudad.delete()
    return redirect('crearMenu:lista_ciudades')


def lista_tipos_menu(request):
    tipos = TipoMenu.objects.all().order_by('descripcion')

    if request.method == 'POST':
        form = TipoMenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crearMenu:lista_tipos_menu')
    else:
        form = TipoMenuForm()

    return render(request, 'crearMenu/lista_tipos_menu.html', {
        'tipos': tipos,
        'form': form
    })


def eliminar_tipo_menu(request, tipo_id):
    tipo = get_object_or_404(TipoMenu, pk=tipo_id)
    tipo.delete()
    return redirect('crearMenu:lista_tipos_menu')


def lista_restaurantes(request):
    restaurantes = Restaurante.objects.all().order_by('nombre')

    if request.method == 'POST':
        form = RestauranteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crearMenu:lista_restaurantes')
    else:
        form = RestauranteForm()

    return render(request, 'crearMenu/lista_restaurantes.html', {
        'restaurantes': restaurantes,
        'form': form
    })


def eliminar_restaurante(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, pk=restaurante_id)
    restaurante.delete()
    return redirect('crearMenu:lista_restaurantes')
