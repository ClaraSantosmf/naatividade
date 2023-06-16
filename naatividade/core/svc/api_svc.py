def request_mock_improvisado_api(parametro):
    return {"PETR3": {"preco": 2}}


def confere_e_atualiza_preco_de_ativo_na_api(
    lista_symbols_ativos_monitorados, historicos_relacionados
):
    for symbol in lista_symbols_ativos_monitorados:
        try:
            response = request_mock_improvisado_api(symbol)
            if response.symbol.preco != historicos_relacionados:
                pass
        except:
            pass
    return response
