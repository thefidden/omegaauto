import django_filters

from cars.models import Model, Brand


class ModelFilter(django_filters.FilterSet):
    brand = django_filters.ModelChoiceFilter(
        field_name = 'brand', queryset = Brand.objects.all(), to_field_name = 'name', label = 'Модель'
    )

    class Meta:
        model = Model
        fields = ('brand',)
