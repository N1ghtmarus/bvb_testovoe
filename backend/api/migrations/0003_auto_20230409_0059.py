from django.db import migrations


def split_full_name(apps, schema_editor):
    Employee = apps.get_model('api', 'Employee')
    for employee in Employee.objects.all():
        full_name = employee.full_name.split()
        if len(full_name) == 3:
            employee.name = full_name[0]
            employee.surname = full_name[1]
            employee.patronymic = full_name[2]
        elif len(full_name) == 2:
            employee.name = full_name[0]
            employee.surname = full_name[1]
        elif len(full_name) == 1:
            employee.name = full_name[0]
        employee.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_employee_options_and_more'),
    ]

    operations = [
        migrations.RunPython(split_full_name),
    ]
