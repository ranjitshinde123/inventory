import django_filters

from .models import Stock, NonStock


class StockFilter(django_filters.FilterSet):                            # Stockfilter used to filter based on name
    name = django_filters.CharFilter(lookup_expr='-icontains')           # allows filtering without entering the full name
    class Meta:
        Model = Stock
        fields = ['name','category','subcategory']


class NonStockFilter(django_filters.FilterSet):                            # Stockfilter used to filter based on name
    name = django_filters.CharFilter(lookup_expr='-icontains')           # allows filtering without entering the full name
    class Meta:
        Model = NonStock
        fields = ['name','category','subcategory']