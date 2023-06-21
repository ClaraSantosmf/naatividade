from ...svc.api_svc import confere_e_atualiza_preco_de_ativo_na_api
import djclick as click


@click.command()
def command():
    confere_e_atualiza_preco_de_ativo_na_api()
    return
