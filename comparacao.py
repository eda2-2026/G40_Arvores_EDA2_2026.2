# Benchmark: compara BST, AVL e Rubro-Negra nos tres cenarios de entrada.
#
# Para cada combinacao (arvore, cenario) a gente mede:
#   - insercao de todos os jogos: tempo, comparacoes, rotacoes e altura final
#   - busca de todos os ids: media de comparacoes por busca e tempo
#   - remocao de metade dos jogos (500, em ordem aleatoria): tempo, rotacoes e altura final
#
# Como o tempo varia de uma execucao pra outra, o tempo e a MEDIANA de varias repeticoes.
# Comparacoes, rotacoes e altura nao mudam (sao sempre iguais).
#
# Rodar: python comparacao.py
# Gera: assets/resultados.csv

import csv
import random
import statistics
import time

from utils.carregador import carregar_dados
from utils.cenarios import CENARIOS
from arvores.bst import BST
from arvores.avl import AVL
from arvores.rubro_negra import RubroNegra

CAMINHO = "dados/csv de jogos.csv"
REPETICOES = 7

ARVORES = [("BST", BST), ("AVL", AVL), ("Rubro-Negra", RubroNegra)]


def medir_tempo(funcao):
    inicio = time.perf_counter()
    funcao()
    return (time.perf_counter() - inicio) * 1000  # em ms


def rodar(classe, ordem, ids_remover):
    """Faz uma rodada completa e devolve as medidas."""
    arvore = classe()

    def inserir_todos():
        for jogo in ordem:
            arvore.inserir(jogo)

    tempo_insercao = medir_tempo(inserir_todos)
    comparacoes_insercao = arvore.comparacoes
    rotacoes_insercao = arvore.rotacoes
    altura_insercao = arvore.altura()

    # busca de todos os ids
    total_comparacoes_busca = 0
    maximo_busca = 0

    def buscar_todos():
        nonlocal total_comparacoes_busca, maximo_busca
        for jogo in ordem:
            comparacoes = arvore.buscar(jogo.id)["comparacoes"]
            total_comparacoes_busca += comparacoes
            if comparacoes > maximo_busca:
                maximo_busca = comparacoes

    tempo_busca = medir_tempo(buscar_todos)

    # remocao de metade dos jogos
    rotacoes_antes = arvore.rotacoes
    comparacoes_antes = arvore.comparacoes

    def remover_metade():
        for id_game in ids_remover:
            arvore.remover(id_game)

    tempo_remocao = medir_tempo(remover_metade)

    return {
        "tempo_insercao_ms": tempo_insercao,
        "comparacoes_insercao": comparacoes_insercao,
        "rotacoes_insercao": rotacoes_insercao,
        "altura": altura_insercao,
        "comparacoes_por_busca": total_comparacoes_busca / len(ordem),
        "maximo_comparacoes_busca": maximo_busca,
        "tempo_busca_ms": tempo_busca,
        "tempo_remocao_ms": tempo_remocao,
        "comparacoes_remocao": arvore.comparacoes - comparacoes_antes,
        "rotacoes_remocao": arvore.rotacoes - rotacoes_antes,
        "altura_apos_remocao": arvore.altura(),
    }


def main():
    jogos = carregar_dados(CAMINHO)

    # os mesmos 500 ids sao removidos em todas as arvores, na mesma ordem
    ids = [jogo.id for jogo in jogos]
    random.Random(7).shuffle(ids)
    ids_remover = ids[:500]

    resultados = []

    for cenario, funcao in CENARIOS.items():
        ordem = funcao(jogos)
        for nome, classe in ARVORES:
            rodadas = [rodar(classe, ordem, ids_remover) for _ in range(REPETICOES)]

            linha = {"cenario": cenario, "arvore": nome}
            for campo in rodadas[0]:
                valores = [r[campo] for r in rodadas]
                if campo.startswith("tempo"):
                    linha[campo] = statistics.median(valores)
                else:
                    linha[campo] = valores[0]  # nao muda entre as repeticoes
            resultados.append(linha)

    # ---------- mostra no terminal ----------
    print(f"\nBenchmark com {len(jogos)} jogos (tempo = mediana de {REPETICOES} execuções)\n")

    for cenario in CENARIOS:
        print(f"=== Entrada {cenario} ===")
        print(f"{'Árvore':<13}{'Altura':>7}{'Rot.ins':>9}{'Comp.ins':>10}{'Comp/busca':>12}{'Máx.busca':>10}"
              f"{'Rot.rem':>9}{'Alt.rem':>9}{'T.ins(ms)':>11}{'T.busca(ms)':>13}{'T.rem(ms)':>11}")
        for r in resultados:
            if r["cenario"] != cenario:
                continue
            print(f"{r['arvore']:<13}{r['altura']:>7}{r['rotacoes_insercao']:>9}{r['comparacoes_insercao']:>10}"
                  f"{r['comparacoes_por_busca']:>12.2f}{r['maximo_comparacoes_busca']:>10}"
                  f"{r['rotacoes_remocao']:>9}{r['altura_apos_remocao']:>9}"
                  f"{r['tempo_insercao_ms']:>11.2f}{r['tempo_busca_ms']:>13.2f}{r['tempo_remocao_ms']:>11.2f}")
        print()

    # ---------- salva em csv (os graficos leem esse arquivo) ----------
    campos = list(resultados[0].keys())
    arquivo = open("assets/resultados.csv", "w", newline="", encoding="utf-8")
    escritor = csv.DictWriter(arquivo, fieldnames=campos)
    escritor.writeheader()
    for r in resultados:
        linha = {}
        for campo in campos:
            valor = r[campo]
            linha[campo] = round(valor, 4) if isinstance(valor, float) else valor
        escritor.writerow(linha)
    arquivo.close()
    print("Resultados salvos em assets/resultados.csv")


if __name__ == "__main__":
    main()
