from django.core.mail import send_mass_mail

from naatividade.core.models import Monitoramento, Historico, Ativo
from naatividade.core.svc.monitoramento_svc import InfoEmail


def send_mail_alerta_venda(ativo_id):
    infos_emails_para_vender = []
    ativo = Ativo.objects.get(id=ativo_id)
    historico = Historico.objects.filter(ativo=ativo_id).order_by("-timestamp").first()
    monitoramentos_validos_venda = Monitoramento.objects.filter(
        ativo=ativo_id, max_value__gte=historico.valor
    ).select_related("email")
    for monitoramento in monitoramentos_validos_venda:
        destinatario = monitoramento.email.__str__()  # qual melhor forma disso?
        infoemail = InfoEmail(
            ativo.nome, destinatario, historico.valor, monitoramento.max_value
        )
        infos_emails_para_vender.append(infoemail.lista_emails_venda())
        try:
            if infos_emails_para_vender:
                send_mass_mail(infos_emails_para_vender, fail_silently=False)
        except:
            return


def send_mail_alerta_compra(ativo_id):
    infos_emails_para_comprar = []
    ativo = Ativo.objects.get(id=ativo_id)
    historico = Historico.objects.filter(ativo=ativo_id).order_by("-timestamp").first()
    monitoramentos_validos_compra = Monitoramento.objects.filter(
        ativo=ativo_id, min_value__lte=historico.valor
    ).select_related("email")
    for monitoramento in monitoramentos_validos_compra:
        destinatario = monitoramento.email.__str__()
        infoemail = InfoEmail(
            ativo.nome, destinatario, historico.valor, monitoramento.min_value
        )
        infos_emails_para_comprar.append(infoemail.lista_emails_compra())
    if infos_emails_para_comprar:
        try:
            send_mass_mail(infos_emails_para_comprar, fail_silently=False)
        except:
            return
