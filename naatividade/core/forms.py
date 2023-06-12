from django.forms import ModelForm
from .models import Monitoramento


class MonitoramentoForm(ModelForm):
    class Meta:
        model = Monitoramento
        fields = ("ativo", "schedule", "min_value", "max_value", "email")
