import django_filters

from cars.models import Car, Brand, Fuel, Gear, Color, CarStatus


class CarFilter(django_filters.FilterSet):
    brand = django_filters.ModelChoiceFilter(field_name = 'brand', queryset = Brand.objects.all(),
        to_field_name = 'name', label = 'Марка')

    model = django_filters.CharFilter(field_name = 'model', lookup_expr = 'iexact', label = 'Модель')
    fuel = django_filters.ModelChoiceFilter(field_name = 'fuel', queryset = Fuel.objects.all(), label = 'Топливо')
    color = django_filters.ModelChoiceFilter(field_name = 'color', queryset = Color.objects.all(), label = 'Цвет')
    gear = django_filters.ModelChoiceFilter(field_name = 'gear', queryset = Gear.objects.all(), label = 'Трансмиссия')
    status = django_filters.ModelChoiceFilter(field_name = 'status', queryset = CarStatus.objects.all(),
        label = 'Статус')

    year_min = django_filters.NumberFilter(field_name = 'year', lookup_expr = 'gte', label = 'Год выпуска, мин')
    year_max = django_filters.NumberFilter(field_name = 'year', lookup_expr = 'lte', label = 'Год выпуска, макс')

    mileage_min = django_filters.NumberFilter(field_name = 'mileage', lookup_expr = 'gte', label = 'Пробег, мин')
    mileage_max = django_filters.NumberFilter(field_name = 'mileage', lookup_expr = 'lte', label = 'Пробег, макс')

    power_min = django_filters.NumberFilter(field_name = 'power', lookup_expr = 'gte', label = 'Мощность, л.с., мин')
    power_max = django_filters.NumberFilter(field_name = 'power', lookup_expr = 'lte', label = 'Мощность, л.с., макс')

    displacement_min = django_filters.NumberFilter(field_name = 'displacement', lookup_expr = 'gte',
        label = 'Объем двигателя, мин')
    displacement_max = django_filters.NumberFilter(field_name = 'displacement', lookup_expr = 'lte',
        label = 'Объем двигателя, макс')

    price_min = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'gte', label = 'Стоимость, мин')
    price_max = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'lte', label = 'Стоимость, макс')

    only_available = django_filters.BooleanFilter(method = 'filter_only_available', label = 'Только доступные')

    class Meta:
        model = Car
        fields = (
            'brand',
            'model',
            'fuel',
            'color',
            'gear',
            'year_min',
            'year_max',
            'mileage_min',
            'mileage_max',
            'power_min',
            'power_max',
            'displacement_min',
            'displacement_max',
            'price_min',
            'price_max',
        )

    def filter_only_available(self, queryset, name, value):
        if value is True:
            return queryset.filter(status__name__in = ('В продаже', 'Зарезервирован'))

        return queryset
