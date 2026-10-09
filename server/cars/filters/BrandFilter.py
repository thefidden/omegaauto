import django_filters

from cars.models import Brand


class BrandFilter(django_filters.FilterSet):
    only_available = django_filters.BooleanFilter(method = 'filter_only_available')

    def filter_only_available(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(cars__status__name__in = ('В продаже', 'Зарезервирован')).distinct()

    class Meta:
        model = Brand
        fields = ('only_available',)
