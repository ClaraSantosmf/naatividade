from django.core.mail import send_mass_mail

from naatividade.core.models import Monitoramento, Historico, Ativo
from naatividade.core.svc.monitoramento_svc import InfoEmail


def send_mail_alerta_venda(monitoramentos_validos_venda):
    infos_emails_para_vender = []
    for monitoramento in monitoramentos_validos_venda:
        valor_no_historico = monitoramento.ativo.historico_set.order_by("-timestamp").first().valor
        destinatario = str(monitoramento.email)
        infoemail = InfoEmail(
         monitoramento.ativo.nome, destinatario, valor_no_historico, monitoramento.max_value
        )
        infos_emails_para_vender.append(infoemail.lista_emails_venda())
        try:
            if infos_emails_para_vender:
                send_mass_mail(infos_emails_para_vender, fail_silently=False)
        except:
            return


def send_mail_alerta_compra(monitoramentos_validos_venda):
    infos_emails_para_comprar = []
    for monitoramento in monitoramentos_validos_venda:
        valor_no_historico = monitoramento.ativo.historico_set.order_by("-timestamp").first().valor
        destinatario = str(monitoramento.email)
        infoemail = InfoEmail(
         monitoramento.ativo.nome, destinatario, valor_no_historico, monitoramento.min_value
        )
        infos_emails_para_comprar.append(infoemail.lista_emails_compra())
    if infos_emails_para_comprar:
        try:
            send_mass_mail(infos_emails_para_comprar, fail_silently=False)
        except:
            return
