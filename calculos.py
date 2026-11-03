def calcular_media(n1, n2, n3):
    return n1 + n2 + n3 / 3


def situacao(media, frequencia):
    if media >= 6:
        return "APROVADO"
    if frequencia < 75:
        return "REPROVADO POR FALTA"
    return "REPROVADO"


def valor_hora_aula(titulacao):
    if titulacao == "especialista":
        return 45
    if titulacao == "mestre":
        return 60
    if titulacao == "doutor":
        return 80


def gerar_ra(ano, sequencia):
    return str(ano) + str(sequencia)


def juros_atraso(valor, dias):
    return valor + valor * 0.1 * dias
