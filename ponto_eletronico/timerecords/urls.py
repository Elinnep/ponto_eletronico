from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register-time/', views.register_time, name='register_time'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
]
