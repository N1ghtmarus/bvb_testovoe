from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Subquery
from django.db.models.query import QuerySet, Prefetch

from .filters import EmployeeFilter
from .models import Employee, Department
from .pagination import CustomPagination
from .serializers import EmployeeSerializer, DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления сотрудниками.
    """
    queryset = Employee.objects.select_related('department')
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeFilter

    def get_permissions(self) -> list:
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        """
        При создании сотрудника, если передан параметр `department`,
        то производит привязку к департаменту.
        """
        department_id = self.request.data.get('department')
        if department_id:
            department = get_object_or_404(Department, id=department_id)
            serializer.save(department=department)
        else:
            serializer.save()


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления департаментами.
    """
    queryset = Department.objects.select_related('director')
    serializer_class = DepartmentSerializer

    def get_permissions(self) -> list:
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self) -> QuerySet:
        """
        Возвращает QuerySet департаментов с
        дополнительными полями "num_employees" и "total_salary".
        При обращении через 'GET' метод достает всех сотрудников,
        привязанных к департаменту
        """
        if self.request.method == 'GET':
            queryset = super().get_queryset().annotate(
                num_employees=Count('employees'),
                total_salary=Sum('employees__salary')
            )

            director_ids = Department.objects.exclude(
                director_id=None
                ).values('director_id')

            return queryset.prefetch_related(
                Prefetch(
                    'employees',
                    Employee.objects.exclude(id__in=Subquery(director_ids))
                )
            )
        return queryset
