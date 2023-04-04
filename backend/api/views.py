from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

from .models import Employee, Department
from .pagination import CustomPagination
from .serializers import EmployeeSerializer, DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления сотрудниками.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination

    def get_permissions(self) -> list:
        """
        Возвращает список разрешений для действия.

        При запросе методом GET требуется аутентификация пользователя,
        при других запросах требуется проверка на администратора.

        :return: список разрешений.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self) -> QuerySet:
        """
        Возвращает QuerySet сотрудников.

        Если передан параметр `department`, то фильтрует сотрудников по департаменту,
        если передан параметр `full_name`, то фильтрует сотрудников по ФИО.

        :return: QuerySet сотрудников.
        """
        queryset = Employee.objects.select_related('department').all()

        department = self.request.query_params.get('department', None)
        if department is not None:
            return queryset.filter(department__name=department)

        full_name = self.request.query_params.get('full_name', None)
        if full_name is not None:
            return queryset.filter(full_name=full_name)

        return queryset

    def create(self, request, *args, **kwargs) -> Response:
        """
        Создает нового сотрудника.

        При создании сотрудника, если передан параметр `department`,
        то производит привязку к департаменту.

        :param request: объект запроса.
        :param args: неименованные аргументы.
        :param kwargs: именованные аргументы.
        :return: объект ответа.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Определяем нужно ли привязать пользователя к департаменту
        department_id = request.data.get('department', None)
        if department_id is not None:
            department = get_object_or_404(Department, id=department_id)
        else:
            department = None

        employee = serializer.save(department=department)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(employee).data,
            status=status.HTTP_201_CREATED, headers=headers
        )


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self) -> list:
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self) -> QuerySet:
        queryset = Department.objects.all()
        for department in queryset:
            department.num_employees = department.num_employees()
            department.total_salary = department.total_salary()
        return queryset
