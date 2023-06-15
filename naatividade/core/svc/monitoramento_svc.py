class InfoEmail:
    def __init__(
        self, ativo, destinatario, valor_atual_ativo, valor_alerta_parametro_usuario
    ):
        self.ativo = ativo
        self.destinatario = destinatario
        self.valor_atual_ativo = valor_atual_ativo
        self.valor_alerta_parametro_usuario = valor_alerta_parametro_usuario

    def lista_emails_venda(self):
        if self.valor_atual_ativo == self.valor_alerta_parametro_usuario:
            maior_ou_igual = "Exatamente"
        else:
            maior_ou_igual = "Está maior que"
        assunto = f"Está na hora de vender {self.ativo}"
        msg = f"O ativo {self.ativo} está custando {self.valor_atual_ativo}! {maior_ou_igual} o preço de venda estabelecido no seu alerta NaAtividade. Alerta -> {self.valor_alerta_parametro_usuario}"
        template_email = (
            f"{assunto}",
            f"{msg}",
            "naatividade@gmail.com",
            [self.destinatario],
        )
        return template_email

    def lista_emails_compra(self):
        if self.valor_atual_ativo == self.valor_alerta_parametro_usuario:
            maior_ou_igual = "Exatamente"
        else:
            maior_ou_igual = "Menor que"
        assunto = f"Está na hora de comprar {self.ativo}"
        msg = f"O ativo {self.ativo} está custando {self.valor_atual_ativo}! {maior_ou_igual} o preço de compra estabelecido no seu alerta NaAtividade. Alerta -> {self.valor_alerta_parametro_usuario}"
        template_email = (
            f"{assunto}",
            f"{msg}",
            "naatividade@gmail.com",
            [self.destinatario],
        )
        return template_email
