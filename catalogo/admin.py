from django.contrib import admin
from .models import Categoria, Producto
from django.utils.html import format_html
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "IATEC Administración"
admin.site.site_title = "Panel de IATEC"
admin.site.index_title = "Bienvenido al Panel de Administración de IATEC"

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    list_editable = ('nombre', 'descripcion')
    ordering = ('id',)
    list_display_links = ('id',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria', 'mostrar_imagen')
    search_fields = ('nombre', 'categoria__nombre')
    list_filter = ('categoria',)
    ordering = ('id',)
    list_editable = ('nombre', 'precio', 'categoria')
    list_display_links = ('id',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'precio', 'descripcion', 'imagen', 'categoria')
        }),
    )

    def mostrar_imagen(self, obj):
        
        if obj.imagen:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />',
                obj.imagen.url
            )
        return "-"
    mostrar_imagen.short_description = "Imagen"