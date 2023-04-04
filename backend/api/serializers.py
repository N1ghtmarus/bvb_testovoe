from rest_framework import serializers
from .models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'full_name',
            'photo',
            'position',
            'salary',
            'age',
            'department'
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    director = EmployeeSerializer()
    num_employees = serializers.ReadOnlyField()
    total_salary = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = '__all__'
