from django import forms
from .models import Categoria, Chef, Ciudad, Plato, DetalleNutricional, Ingrediente, Receta, DetalleIngrediente, Restaurante, TipoMenu


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'categoria', 'receta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'receta': forms.Select(attrs={'class': 'form-select'}),
        }


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


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sal, Tomate, Pollo'}),
        }


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'proceso']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'proceso': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describa paso a paso la preparación...'}),
        }


class DetalleIngredienteForm(forms.ModelForm):
    class Meta:
        model = DetalleIngrediente
        fields = ['ingrediente', 'cantidad']
        widgets = {
            'ingrediente': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Cantidad'}),
        }


class ChefForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ['nombre', 'cedula', 'turno', 'telefono', 'sexo', 'ciudad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'M/F'}),
            'ciudad': forms.Select(attrs={'class': 'form-select'}),
        }


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Ciudad'}),
        }


class TipoMenuForm(forms.ModelForm):
    class Meta:
        model = TipoMenu
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ejecutivo, Infantil, Eventos'
            }),
        }


class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nombre', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del Restaurante'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección / Ubicación'
            }),
        }
