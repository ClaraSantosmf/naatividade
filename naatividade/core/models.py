from django.db import models


class Ativo(models.Model):
    nome = models.CharField(max_length=130)
    symbol = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Email(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Monitoramento(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.PROTECT)
    schedule = models.IntegerField(
        default=60, null=True, blank=True, verbose_name="Monitoramento em minutos"
    )
    min_value = models.DecimalField(max_digits=12, decimal_places=2)
    max_value = models.DecimalField(max_digits=12, decimal_places=2)
    email = models.ForeignKey(Email, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    last_view = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    next_view = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.ativo.nome


class Historico(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
