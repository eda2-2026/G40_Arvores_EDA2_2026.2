import csv
from modelos.jogos import Jogo

# valores que aparecem no arquivo quando o dado esta faltando
VALORES_VAZIOS = ["NULL", "N/A", "tbd", ""]


def converter_int(valor):
    if valor in VALORES_VAZIOS:
        return None
    return int(valor)


def converter_float(valor):
    if valor in VALORES_VAZIOS:
        return None
    return float(valor)


def carregar_dados(caminho_arquivo):
    jogos = []

    arquivo = open(caminho_arquivo, encoding="utf-8")
    leitor = csv.DictReader(arquivo)

    for linha in leitor:  # Percorre cada linha do csv e cria um objeto Jogo com os dados da linha
        developer = linha["developer"]
        if developer in VALORES_VAZIOS:
            developer = None

        jogo = Jogo(
            id_game=int(linha["id_game"]),
            name=linha["name"],
            year_of_release=converter_int(linha["year_of_release"]),
            developer=developer,
            platform=linha["platform"],
            critic_score=converter_int(linha["critic_score"]),
            user_score=converter_float(linha["user_score"])
        )
        jogos.append(jogo)  # adiciona o objeto Jogo à lista que vamos utilizar

    arquivo.close()
    return jogos
