from django.db import models


class TipoMenu(models.Model):
    # En Django, el 'id' es automático, pero para mapear a 'IdTipoMenu'
    # lo definimos explícitamente como la llave primaria.
    id_tipo_menu = models.AutoField(primary_key=True, db_column='IdTipoMenu')
    descripcion = models.CharField(max_length=255, db_column='Descripcion')

    class Meta:
        db_table = 'SGR_P_TipoMenu'  # Nombre exacto de la tabla en SQL Server

    def __str__(self):
        return self.descripcion


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, db_column='IdCategoria')
    nombre = models.CharField(max_length=100, db_column='Nombre')
    descripcion = models.CharField(
        max_length=500, null=True, blank=True, db_column='Descripcion')

    class Meta:
        db_table = 'SGR_P_Categoria'

    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(
        primary_key=True, db_column='IdIngrediente')
    nombre = models.CharField(max_length=255, db_column='Nombre')

    class Meta:
        db_table = 'SGR_P_Ingrediente'

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True, db_column='IdCiudad')
    descripcion = models.CharField(max_length=100, db_column='Descripcion')

    class Meta:
        db_table = 'SGR_P_Ciudad'

    def __str__(self):
        return self.descripcion

# --- Tablas Maestras ---


class Restaurante(models.Model):
    id_restaurante = models.AutoField(
        primary_key=True, db_column='IdRestaurante')
    nombre = models.CharField(max_length=255, db_column='Nombre')
    ubicacion = models.CharField(
        max_length=255, null=True, blank=True, db_column='Ubicacion')

    class Meta:
        db_table = 'SGR_M_Restaurante'

    def __str__(self):
        return self.nombre


class Chef(models.Model):
    id_chef = models.AutoField(primary_key=True, db_column='IdChef')
    nombre = models.CharField(max_length=255, db_column='Nombre')
    cedula = models.CharField(max_length=20, db_column='Cedula')
    turno = models.CharField(max_length=20, null=True,
                             blank=True, db_column='Turno')
    telefono = models.CharField(
        max_length=20, null=True, blank=True, db_column='Telefono')
    sexo = models.CharField(max_length=1, null=True,
                            blank=True, db_column='Sexo')

    # Relación ForeignKey (FK)
    # on_delete=models.SET_NULL significa que si se borra la ciudad,
    # este campo 'ciudad' en Chef se pondrá en NULO.
    ciudad = models.ForeignKey(
        Ciudad, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdCiudad')

    class Meta:
        db_table = 'SGR_M_Chef'

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True, db_column='IdReceta')
    nombre = models.CharField(max_length=255, db_column='Nombre')
    # VARCHAR(MAX) en SQL Server se traduce como TextField en Django
    proceso = models.TextField(null=True, blank=True, db_column='Proceso')

    class Meta:
        db_table = 'SGR_M_Receta'

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    id_plato = models.AutoField(primary_key=True, db_column='IdPlato')
    nombre = models.CharField(max_length=255, db_column='Nombre')

    # Relaciones FK
    receta = models.ForeignKey(
        Receta, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdReceta')
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdCategoria')

    class Meta:
        db_table = 'SGR_M_Plato'

    def __str__(self):
        return self.nombre


class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True, db_column='IdMenu')
    nombre = models.CharField(max_length=255, db_column='Nombre')

    # Relaciones FK
    chef = models.ForeignKey(
        Chef, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdChef')
    tipo_menu = models.ForeignKey(
        TipoMenu, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdTipoMenu')

    # Esta FK es NOT NULL, por lo que si se borra el restaurante,
    # se borran en cascada todos los menús asociados.
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, db_column='IdRestaurante')

    class Meta:
        db_table = 'SGR_M_Menu'

    def __str__(self):
        return self.nombre

# --- Tablas Transaccionales (Detalles) ---


class DetalleIngrediente(models.Model):
    id_detalle_ingrediente = models.AutoField(
        primary_key=True, db_column='IdDetalleIngrediente')

    # Relaciones FK (Estas son NOT NULL)
    receta = models.ForeignKey(
        Receta, on_delete=models.CASCADE, db_column='IdReceta')
    ingrediente = models.ForeignKey(
        Ingrediente, on_delete=models.CASCADE, db_column='IdIngrediente')

    # DECIMAL(10,2) se traduce como DecimalField
    cantidad = models.DecimalField(
        max_digits=10, decimal_places=2, db_column='Cantidad')

    class Meta:
        db_table = 'SGR_T_DetalleIngrediente'

    def __str__(self):
        # Un __str__ más descriptivo para tablas de detalle
        return f"{self.receta.nombre} - {self.ingrediente.nombre}"


class DetalleMenu(models.Model):
    id_detalle_menu = models.AutoField(
        primary_key=True, db_column='IdDetalleMenu')

    # Relaciones FK (NOT NULL)
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, db_column='IdMenu')
    plato = models.ForeignKey(
        Plato, on_delete=models.CASCADE, db_column='IdPlato')
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, db_column='Precio')

    class Meta:
        db_table = 'SGR_T_DetalleMenu'

    def __str__(self):
        return f"{self.menu.nombre} - {self.plato.nombre}"


class DetalleNutricional(models.Model):
    id_detalle_nutricional = models.AutoField(
        primary_key=True, db_column='IdDetalleNutricional')

    # Esta es una relación 1 a 1. Un plato tiene UN solo detalle nutricional.
    plato = models.OneToOneField(
        Plato, on_delete=models.CASCADE, db_column='IdPlato')

    # Campos DECIMAL que pueden ser nulos
    carbohidratos = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, db_column='Carbohidratos')
    proteina = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, db_column='Proteina')
    caloria = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, db_column='Caloria')
    grasa = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, db_column='Grasa')

    class Meta:
        db_table = 'SGR_T_DetalleNutricional'

    def __str__(self):
        return f"Info Nutricional de: {self.plato.nombre}"
