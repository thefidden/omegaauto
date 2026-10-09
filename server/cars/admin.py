from django.utils.html import format_html

from cars.models import Brand, Color, Fuel, Gear, CarImage, Car

from django.contrib import admin


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ('image', 'public', 'image_preview', 'index')
    readonly_fields = ('image_preview',)
    ordering = ('index',)

    @admin.display(description = 'Предпросмотр')
    def image_preview(self, obj: CarImage):
        if not obj.image:
            return 'Нет изображений'

        return format_html('''
            <img src="{}" style="max-height: 120px; max-width: 180px; object-fit: contain;"/>
        ''', obj.image.url)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'brand', 'model', 'year', 'mileage', 'power', 'displacement', 'fuel', 'gear', 'color', 'status',
        'price', 'created_at'
    )
    list_filter = (
        'brand', 'model', 'year', 'mileage', 'power', 'displacement', 'fuel', 'gear', 'color', 'status',
        'price', 'created_at'
    )
    search_fields = ('brand', 'model')
    inlines = (CarImageInline,)
    ordering = ('-created_at', 'brand', 'year', 'mileage')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Gear)
class GearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
