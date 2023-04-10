import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    department = django_filters.CharFilter(field_name='department__name')
    surname = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['department', 'surname']
