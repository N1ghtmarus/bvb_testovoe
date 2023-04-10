from rest_framework import serializers
from .models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'surname',
            'name',
            'patronymic',
            'photo',
            'position',
            'salary',
            'age',
            'department'
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    director = EmployeeSerializer()
    employees = EmployeeSerializer(many=True, read_only=True)
    num_employees = serializers.ReadOnlyField()
    total_salary = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = ['id', 'num_employees', 'total_salary', 'director', 'employees']
