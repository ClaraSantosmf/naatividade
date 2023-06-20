from ..models import Monitoramento, Historico
from django.utils import timezone
from ..svc.mail_svc import send_mail_alerta_compra, send_mail_alerta_venda

def request_mock_improvisado_api(parametro):
    return {"AZUL4": {"preco": 2}}


def confere_e_atualiza_preco_de_ativo_na_api():
    horario_brasilia = timezone.now()
    monitoramentos = Monitoramento.objects.select_related('ativo', 'email').filter(next_view__lte=horario_brasilia)

    lista_symbols_ativos_monitorados = monitoramentos.values_list(
        "ativo__symbol", flat=True
    )
    historicos_relacionados = Historico.objects.filter(
        ativo__symbol__in=lista_symbols_ativos_monitorados
    )
    ativos_ids_compra =[]
    monitoramentos_validos_venda =[]
    for symbol in lista_symbols_ativos_monitorados:
        try:
            response = request_mock_improvisado_api(symbol)
            ativo_da_vez = historicos_relacionados.get(ativo__symbol=symbol)
            monitoramento_da_vez = monitoramentos.get(ativo=ativo_da_vez.ativo)
            preco_atual_ativo = response[symbol]['preco']
            parametro_compra = monitoramento_da_vez.min_value
            if preco_atual_ativo != ativo_da_vez.valor:
                if preco_atual_ativo <= parametro_compra:
                    ativos_ids_compra.append(monitoramento_da_vez)
                elif preco_atual_ativo >= monitoramento_da_vez.max_value:
                    monitoramentos_validos_venda.append(monitoramento_da_vez)
        except:
            pass
    if ativos_ids_compra:
        send_mail_alerta_compra(ativos_ids_compra)
    if monitoramentos_validos_venda:
        send_mail_alerta_venda(monitoramentos_validos_venda)
    return response
