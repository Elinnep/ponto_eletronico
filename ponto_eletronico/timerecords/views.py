from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from .models import TimeRecord, DailyAttendance
import json


@login_required
def dashboard(request):
    """
    Exibe o dashboard do usuário com relógio em tempo real e registro de ponto
    """
    today = timezone.now().date()
    records_today = TimeRecord.objects.filter(user=request.user, data=today).order_by('hora')
    
    # Preparar dados dos registros de hoje
    records_data = {}
    for record in records_today:
        records_data[record.tipo] = record.hora.strftime('%H:%M')
    
    context = {
        'records_today': records_today,
        'records_data': records_data,
        'today': today,
    }
    return render(request, 'dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def register_time(request):
    """
    AJAX endpoint para registrar ponto
    """
    data = json.loads(request.body)
    record_type = data.get('type')
    
    # Validar tipo
    valid_types = ['ENTRADA', 'INICIO_INTERVALO', 'FIM_INTERVALO', 'SAIDA']
    if record_type not in valid_types:
        return JsonResponse({'success': False, 'error': 'Tipo de registro inválido'})
    
    today = timezone.now().date()
    now = timezone.now().time()
    
    # Verificar se já existe registro do mesmo tipo hoje
    if TimeRecord.objects.filter(user=request.user, data=today, tipo=record_type).exists():
        return JsonResponse({
            'success': False, 
            'error': f'Você já registrou {record_type.lower().replace("_", " ")} hoje'
        })
    
    # Validar sequência de registros
    records_today = TimeRecord.objects.filter(user=request.user, data=today)
    
    if record_type == 'INICIO_INTERVALO':
        if not records_today.filter(tipo='ENTRADA').exists():
            return JsonResponse({
                'success': False, 
                'error': 'Você precisa registrar entrada antes do intervalo'
            })
    
    elif record_type == 'FIM_INTERVALO':
        if not records_today.filter(tipo='INICIO_INTERVALO').exists():
            return JsonResponse({
                'success': False, 
                'error': 'Você precisa registrar início do intervalo antes do fim'
            })
    
    elif record_type == 'SAIDA':
        if not records_today.filter(tipo='ENTRADA').exists():
            return JsonResponse({
                'success': False, 
                'error': 'Você precisa registrar entrada antes da saída'
            })
    
    # Criar registro
    time_record = TimeRecord.objects.create(
        user=request.user,
        data=today,
        hora=now,
        tipo=record_type
    )
    
    # Atualizar ou criar DailyAttendance
    attendance, created = DailyAttendance.objects.get_or_create(
        user=request.user,
        data=today
    )
    attendance.calcular_horas()
    attendance.save()
    
    return JsonResponse({
        'success': True,
        'message': f'{record_type.lower().replace("_", " ")} registrada com sucesso',
        'time': now.strftime('%H:%M'),
        'type': record_type
    })


@login_required
def attendance_report(request):
    """
    Exibe o espelho de ponto mensal
    """
    # Pegar mês e ano da requisição
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))
    
    # Calcular primeiro e último dia do mês
    from calendar import monthrange
    _, days_in_month = monthrange(year, month)
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, days_in_month).date()
    
    # Se é o mês/ano atual, não ir além de hoje
    today = timezone.now().date()
    if year == today.year and month == today.month:
        last_day = today
    
    # Buscar todos os registros do período
    all_records = TimeRecord.objects.filter(
        user=request.user,
        data__gte=first_day,
        data__lte=last_day
    ).order_by('data')
    
    # Encontrar primeira entrada do funcionário
    first_entry = all_records.filter(tipo='ENTRADA').first()
    
    # Se não houver entrada, não mostrar nada
    if not first_entry:
        all_days = []
        total_hours = 0
        total_absences = 0
        total_inconsistencies = 0
    else:
        # Buscar apenas datas que têm registros
        dates_with_records = set(record.data for record in all_records)
        
        # Buscar DailyAttendance para essas datas
        daily_records = DailyAttendance.objects.filter(
            user=request.user,
            data__in=dates_with_records
        ).order_by('data')
        
        # Criar lista com apenas os dias que têm registros
        all_days = []
        for record in daily_records:
            date = record.data
            # Buscar detalhes dos registros deste dia
            day_records = TimeRecord.objects.filter(user=request.user, data=date).order_by('hora')
            records_dict = {}
            for day_record in day_records:
                records_dict[day_record.tipo] = day_record.hora.strftime('%H:%M')
            
            all_days.append({
                'attendance': record,
                'date': date,
                'records': records_dict,
            })
        
        # Calcular totais
        total_hours = daily_records.aggregate(total=models.Sum('total_horas'))['total'] or 0
        total_absences = daily_records.filter(status='AUSENTE').count()
        total_inconsistencies = daily_records.filter(status='INCONSISTENTE').count()
    
    # Gerar lista de anos disponíveis
    current_year = timezone.now().year
    years = list(range(current_year - 2, current_year + 2))
    
    # Dicionário de meses
    months_dict = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro',
    }
    
    context = {
        'all_days': all_days,
        'month': month,
        'year': year,
        'years': years,
        'months_dict': months_dict,
        'total_hours': total_hours,
        'total_absences': total_absences,
        'total_inconsistencies': total_inconsistencies,
    }
    return render(request, 'attendance_report.html', context)
