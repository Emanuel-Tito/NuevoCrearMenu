from django import forms
from django.core.exceptions import ValidationError
from .models import (Categoria, Plato, DetalleNutricional, Ingrediente,
                     Receta, DetalleIngrediente, Chef, Ciudad, TipoMenu, Restaurante)

# --- FUNCIÓN DE VALIDACIÓN REUTILIZABLE ---


def validar_no_es_numero(valor, nombre_campo):
    """Lanza error si el texto son solo dígitos"""
    if str(valor).strip().isdigit():
        raise ValidationError(
            f"El {nombre_campo} no puede contener solo números.")
    return valor

# 1. INGREDIENTES


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sal, Tomate'}),
        }

    def clean_nombre(self):
        return validar_no_es_numero(self.cleaned_data['nombre'], "nombre del ingrediente")

# 2. RECETAS


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'proceso']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'proceso': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_nombre(self):
        return validar_no_es_numero(self.cleaned_data['nombre'], "nombre de la receta")

# 3. DETALLE INGREDIENTE (Evitar guardar vacío)


class DetalleIngredienteForm(forms.ModelForm):
    class Meta:
        model = DetalleIngrediente
        fields = ['ingrediente', 'cantidad']
        widgets = {
            'ingrediente': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_ingrediente(self):
        ingrediente = self.cleaned_data.get('ingrediente')
        if not ingrediente:
            raise ValidationError("Debes seleccionar un ingrediente válido.")
        return ingrediente

# 4. CHEFS


class ChefForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ['nombre', 'cedula', 'turno', 'telefono', 'sexo', 'ciudad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            # Cédula sí puede ser número
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'M/F'}),
            'ciudad': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_nombre(self):
        return validar_no_es_numero(self.cleaned_data['nombre'], "nombre del chef")

    def clean_turno(self):
        # El turno no debería ser "111", mejor "Matutino"
        return validar_no_es_numero(self.cleaned_data['turno'], "turno")

# 5. CIUDADES


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_descripcion(self):
        # Las ciudades pueden tener números (Ej: "Sector 7"), pero no ser SOLO números
        return validar_no_es_numero(self.cleaned_data['descripcion'], "nombre de la ciudad")

# --- OTROS FORMS (Sin cambios mayores, pero ya importados) ---


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_nombre(self):
        return validar_no_es_numero(self.cleaned_data['nombre'], "nombre de la categoría")

    def clean_descripcion(self):
        desc = self.cleaned_data.get('descripcion')
        if desc:  # Solo validamos si escribieron algo
            return validar_no_es_numero(desc, "descripción")
        return desc


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'categoria', 'receta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'receta': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_nombre(self):
        return validar_no_es_numero(self.cleaned_data['nombre'], "nombre del plato")


class DetalleNutricionalForm(forms.ModelForm):
    class Meta:
        model = DetalleNutricional
        fields = ['caloria', 'proteina', 'carbohidratos', 'grasa']
        widgets = {
            'caloria': forms.NumberInput(attrs={'class': 'form-control'}),
            'proteina': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbohidratos': forms.NumberInput(attrs={'class': 'form-control'}),
            'grasa': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TipoMenuForm(forms.ModelForm):
    class Meta:
        model = TipoMenu
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_descripcion(self):
        return validar_no_es_numero(self.cleaned_data['descripcion'], "tipo de menú")


class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nombre', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
