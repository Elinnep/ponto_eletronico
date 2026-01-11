from decimal import Decimal
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeRecord(models.Model):
    RECORD_TYPES = [
        ("ENTRADA", "Entrada"),
        ("INICIO_INTERVALO", "Início do Intervalo"),
        ("FIM_INTERVALO", "Fim do Intervalo"),
        ("SAIDA", "Saída"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="time_records"
    )
    data = models.DateField()
    hora = models.TimeField()
    tipo = models.CharField(max_length=20, choices=RECORD_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data", "hora"]
        indexes = [
            models.Index(fields=["user", "data"]),
        ]
        unique_together = [["user", "data", "tipo"]]

    def __str__(self):
        return f"{self.user.cpf} - {self.data} - {self.get_tipo_display()}"  # type: ignore

    def save(self, *args, **kwargs):
        if not self.hora:
            self.hora = datetime.now().time()
        if not self.data:
            self.data = datetime.now().date()
        super().save(*args, **kwargs)


class DailyAttendance(models.Model):
    STATUS_CHOICES = [
        ("NORMAL", "Normal"),
        ("AUSENTE", "Ausente"),
        ("INCONSISTENTE", "Inconsistente"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="daily_attendance"
    )
    data = models.DateField()
    total_horas = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00")
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AUSENTE")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data"]
        unique_together = [["user", "data"]]

    def __str__(self):
        return f"{self.user.cpf} - {self.data} - {self.total_horas}h"  # type: ignore

    def calcular_horas(self):
        """
        Calcula total de horas trabalhadas no dia
        Fórmula: (saída - entrada) - (fim_intervalo - início_intervalo)
        """
        records = TimeRecord.objects.filter(user=self.user, data=self.data).order_by(
            "hora"
        )
        records_dict = {}

        for record in records:
            records_dict[record.tipo] = record.hora

        entrada = records_dict.get("ENTRADA")
        saida = records_dict.get("SAIDA")
        inicio_intervalo = records_dict.get("INICIO_INTERVALO")
        fim_intervalo = records_dict.get("FIM_INTERVALO")

        # Se não há saída ou entrada, marcar como ausente
        if not saida or not entrada:
            self.status = "AUSENTE"
            self.total_horas = Decimal("0.00")
            return

        # Calcular tempo total
        from datetime import datetime as dt

        tempo_entrada_saida = dt.combine(self.data, saida) - dt.combine(
            self.data, entrada
        )
        total_minutos = tempo_entrada_saida.total_seconds() / 60

        # Subtrair intervalo se existir
        if inicio_intervalo and fim_intervalo:
            tempo_intervalo = dt.combine(self.data, fim_intervalo) - dt.combine(
                self.data, inicio_intervalo
            )
            total_minutos -= tempo_intervalo.total_seconds() / 60

        # Converter para horas
        total_horas = total_minutos / 60

        self.total_horas = Decimal(str(round(total_horas, 2)))
        self.status = "NORMAL"

        # Verificar inconsistências
        if (inicio_intervalo and not fim_intervalo) or (
            not inicio_intervalo and fim_intervalo
        ):
            self.status = "INCONSISTENTE"
