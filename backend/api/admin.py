from django.contrib import admin
from .models import Department, Employee


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'director', 'employee_count']
    inlines = [EmployeeInline]

    def employee_count(self, obj):
        return obj.employees.count()

    employee_count.short_description = 'Количество сотрудников'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'full_name', 'position', 'salary', 'age', 'department']
    list_filter = ['department']
    search_fields = ['full_name']
