# Gera os graficos comparativos a partir de assets/resultados.csv
# (o arquivo e criado pelo comparacao.py).
#
# Rodar:
#   python comparacao.py
#   python plot_results.py
#
# Gera em assets/: altura.png, comparacoes_busca.png, rotacoes.png, tempos.png

import csv

import matplotlib
matplotlib.use("Agg")  # nao precisa de janela, so salva as imagens
import matplotlib.pyplot as plt

ARQUIVO = "assets/resultados.csv"

CENARIOS = ["crescente", "decrescente", "embaralhada"]
ARVORES = ["BST", "AVL", "Rubro-Negra"]

# cada arvore tem sempre a mesma cor em todos os graficos
CORES = {"BST": "#2a78d6", "AVL": "#eb6834", "Rubro-Negra": "#1baf7a"}

SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_SECUNDARIO = "#52514e"
GRADE = "#e4e3df"


def ler_resultados():
    dados = {}
    arquivo = open(ARQUIVO, encoding="utf-8")
    for linha in csv.DictReader(arquivo):
        numeros = {}
        for campo, valor in linha.items():
            if campo not in ("cenario", "arvore"):
                numeros[campo] = float(valor)
        dados[(linha["cenario"], linha["arvore"])] = numeros
    arquivo.close()
    return dados


def valores(dados, campo, arvores):
    """Monta {arvore: [valor em cada cenario]} para o campo pedido."""
    resultado = {}
    for arvore in arvores:
        resultado[arvore] = [dados[(c, arvore)][campo] for c in CENARIOS]
    return resultado


def formatar(valor):
    if abs(valor - round(valor)) < 0.000001:
        return f"{round(valor):,}".replace(",", ".")  # numero inteiro: sem casas decimais
    if valor >= 100:
        return f"{valor:,.0f}".replace(",", ".")
    if valor >= 10:
        return f"{valor:.1f}".replace(".", ",")
    return f"{valor:.2f}".replace(".", ",")


def grafico_barras(nome_arquivo, titulo, rotulo_y, series, log=False, rodape=None):
    fig, ax = plt.subplots(figsize=(9, 5.2))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    quantidade = len(series)
    largura = 0.25
    maior = max(max(v) for v in series.values())

    for i, (arvore, lista) in enumerate(series.items()):
        deslocamento = (i - (quantidade - 1) / 2) * (largura + 0.03)
        posicoes = [p + deslocamento for p in range(len(CENARIOS))]
        barras = ax.bar(posicoes, lista, width=largura, color=CORES[arvore],
                        edgecolor=SUPERFICIE, linewidth=2, label=arvore, zorder=3)
        # o valor fica escrito em cima de cada barra (sao so 9 barras)
        for barra, valor in zip(barras, lista):
            ax.text(barra.get_x() + barra.get_width() / 2, valor * (1.08 if log else 1) + (0 if log else maior * 0.012),
                    formatar(valor), ha="center", va="bottom", fontsize=9, color=TEXTO)

    if log:
        ax.set_yscale("log")
        menor = min(min(v) for v in series.values())
        ax.set_ylim(bottom=min(menor, 1) * 0.5 if menor < 1 else 0.5, top=maior * 2.2)
        rotulo_y += " (escala logarítmica)"
    else:
        ax.set_ylim(0, maior * 1.12)

    ax.set_xticks(range(len(CENARIOS)))
    ax.set_xticklabels([f"Entrada {c}" for c in CENARIOS], fontsize=10, color=TEXTO)
    ax.set_ylabel(rotulo_y, fontsize=10, color=TEXTO_SECUNDARIO)
    ax.tick_params(axis="y", colors=TEXTO_SECUNDARIO, labelsize=9, length=0)
    ax.tick_params(axis="x", length=0)
    ax.yaxis.grid(True, color=GRADE, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color(GRADE)

    ax.set_title(titulo, loc="left", fontsize=13, color=TEXTO, pad=38, fontweight="bold")
    ax.legend(frameon=False, ncol=quantidade, loc="lower left", bbox_to_anchor=(0, 1.0),
              labelcolor=TEXTO, fontsize=10)

    if rodape:
        fig.text(0.01, 0.01, rodape, fontsize=8.5, color=TEXTO_SECUNDARIO)

    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig("assets/" + nome_arquivo, dpi=160, facecolor=SUPERFICIE)
    plt.close(fig)
    print("Gerado assets/" + nome_arquivo)


def main():
    dados = ler_resultados()
    n_cresc = dados[("crescente", "BST")]
    avl_c = dados[("crescente", "AVL")]
    rn_c = dados[("crescente", "Rubro-Negra")]

    # 1) altura final
    grafico_barras(
        "altura.png",
        f"Com ids em ordem a BST chega a {n_cresc['altura']:.0f} níveis; "
        f"AVL e rubro-negra ficam em {avl_c['altura']:.0f} e {rn_c['altura']:.0f}",
        "Altura da árvore (níveis)",
        valores(dados, "altura", ARVORES),
        log=True,
    )

    # 2) comparacoes por busca
    grafico_barras(
        "comparacoes_busca.png",
        f"Uma busca leva {n_cresc['comparacoes_por_busca']:.0f} comparações na BST "
        f"degenerada e {avl_c['comparacoes_por_busca']:.0f} nas balanceadas",
        "Comparações por busca (média)",
        valores(dados, "comparacoes_por_busca", ARVORES),
        log=True,
    )

    # 3) rotacoes (BST nunca rotaciona, entao so AVL e rubro-negra)
    rotacoes = {}
    for arvore in ["AVL", "Rubro-Negra"]:
        rotacoes[arvore] = [
            dados[(c, arvore)]["rotacoes_insercao"] + dados[(c, arvore)]["rotacoes_remocao"]
            for c in CENARIOS
        ]
    grafico_barras(
        "rotacoes.png",
        "Rotações para inserir 1000 jogos e remover 500 (a BST não faz rotações)",
        "Rotações (inserção + remoção)",
        rotacoes,
    )

    # 4) tempo total
    tempos = {}
    for arvore in ARVORES:
        tempos[arvore] = [
            dados[(c, arvore)]["tempo_insercao_ms"]
            + dados[(c, arvore)]["tempo_busca_ms"]
            + dados[(c, arvore)]["tempo_remocao_ms"]
            for c in CENARIOS
        ]
    grafico_barras(
        "tempos.png",
        "Tempo total: inserir 1000, buscar 1000 e remover 500 jogos",
        "Tempo (ms)",
        tempos,
        log=True,
        rodape="Mediana de 7 execuções. Os tempos dependem do computador; comparações e rotações não.",
    )


if __name__ == "__main__":
    main()
