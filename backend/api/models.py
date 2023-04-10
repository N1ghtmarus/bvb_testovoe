from django.db import models


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


class Employee(models.Model):
    name = models.CharField(
        max_length=50, blank=True, null=True, db_index=True
        )
    surname = models.CharField(
        max_length=50, blank=True, null=True, db_index=True
        )
    patronymic = models.CharField(
        max_length=50, blank=True, null=True
        )
    photo = models.ImageField(
        upload_to='employee_photos/%Y/%m/%d/',
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
        ordering = ['surname']
        unique_together = ['department', 'name', 'surname', 'patronymic']

    def __str__(self):
        return f'{self.name}, {self.patronymic}, {self.surname}'
