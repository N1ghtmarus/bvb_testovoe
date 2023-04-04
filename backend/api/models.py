from django.db import models
from django.db.models import Sum
from decimal import Decimal


class Department(models.Model):
    name = models.CharField(max_length=100)
    director = models.OneToOneField(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_director'
    )

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
        ordering = ['name']

    def __str__(self):
        return self.name

    def total_salary(self):
        """
        Метод для подсчета общей зарплаты всех сотрудников департамента.
        """
        return self.employees.aggregate(
            total_salary=Sum('salary')
        )['total_salary'] or Decimal('0.00')

    def num_employees(self):
        return self.employees.count()


class Employee(models.Model):
    full_name = models.CharField(max_length=100, db_index=True)
    photo = models.ImageField(
        upload_to='employee_photos/%Y/%m/%d/',
        null=True,
        blank=True
    )
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.IntegerField()
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']
        unique_together = ['department', 'full_name']

    def __str__(self):
        return self.full_name
