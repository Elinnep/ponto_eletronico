from django.contrib import admin
from .models import TimeRecord, DailyAttendance


@admin.register(TimeRecord)
class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'data', 'hora', 'tipo', 'created_at')
    list_filter = ('tipo', 'data', 'user')
    search_fields = ('user__cpf', 'user__first_name', 'user__last_name')
    date_hierarchy = 'data'
    readonly_fields = ('created_at',)


@admin.register(DailyAttendance)
class DailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'data', 'total_horas', 'status', 'updated_at')
    list_filter = ('status', 'data', 'user')
    search_fields = ('user__cpf', 'user__first_name', 'user__last_name')
    date_hierarchy = 'data'
    readonly_fields = ('updated_at',)
