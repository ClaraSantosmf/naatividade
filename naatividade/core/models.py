from django.db import models


class Ativo(models.Model):
    nome = models.CharField(max_length=130)
    symbol = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

class Email(models.Model):
    email = models.EmailField()

class Monitoramento(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.PROTECT)
    schedule = models.IntegerField(default = 60, null=True, blank=True, verbose_name="Monitoramento em minutos")
    min_value = models.DecimalField(max_digits=12, decimal_places=2)
    max_value = models.DecimalField(max_digits=12, decimal_places=2)
    email = models.ForeignKey(Email, on_delete=models.PROTECT)

class Historico(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
