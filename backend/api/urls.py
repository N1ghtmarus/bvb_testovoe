from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'employee', views.EmployeeViewSet)
router.register(r'department', views.DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
