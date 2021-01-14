from django.contrib import admin
from .models import Marca, Producto, Contacto #import de tablas en  model
from .forms import ProductoForm #import del formulario
# Register your models here.


class ProdcutoAdmin(admin.ModelAdmin):
    #mostrar más columnas en el admin.
    list_display = ["nombre", "precio", "nuevo", "marca"]

    #columnas editables.
    list_editable = ["precio"]

    #texto de búsqueda.
    search_fields = ["nombre"]

    #filtro por marcas y si es nuevo
    list_filter = ["marca", "nuevo"]

    list_per_page = 5

    form = ProductoForm

    #registros por página
    #list_per_page = 1


admin.site.register(Marca)
admin.site.register(Producto, ProdcutoAdmin)
admin.site.register(Contacto)
