# Testes de corretude das tres arvores.
# Depois de CADA insercao e CADA remocao a gente confere se a arvore ainda
# respeita as regras dela (ordem da BST, balanceamento da AVL, cores da rubro-negra).
#
# Rodar: python testes.py

import math
import random

from utils.carregador import carregar_dados
from utils.cenarios import CENARIOS
from arvores.bst import BST
from arvores.avl import AVL
from arvores.rubro_negra import RubroNegra
from arvores.base import PRETO, VERMELHO

CAMINHO = "dados/csv de jogos.csv"

erros = []


def conferir(condicao, mensagem):
    if not condicao:
        erros.append(mensagem)


# ---------------------------------------------------------------------------
# Verificacoes das regras de cada arvore
# ---------------------------------------------------------------------------

def verificar_bst(arvore, nome):
    """Regras comuns: ids em ordem estritamente crescente e tamanho certo."""
    ids = [jogo.id for jogo in arvore.em_ordem()]
    for i in range(1, len(ids)):
        if ids[i - 1] >= ids[i]:
            erros.append(f"{nome}: ids fora de ordem ({ids[i - 1]} e {ids[i]})")
            return False
    if len(ids) != arvore.tamanho:
        erros.append(f"{nome}: tamanho {arvore.tamanho} mas tem {len(ids)} nos")
        return False
    return True


def verificar_avl(arvore, nome):
    def confere(no):
        # devolve a altura real do no, ou -1 se achou erro
        if no is None:
            return 0
        esq = confere(no.esq)
        dir = confere(no.dir)
        if esq == -1 or dir == -1:
            return -1
        altura_real = max(esq, dir) + 1
        if no.altura != altura_real:
            erros.append(f"{nome}: altura guardada errada no no {no.chave}")
            return -1
        if abs(esq - dir) > 1:
            erros.append(f"{nome}: no {no.chave} desbalanceado (fb = {esq - dir})")
            return -1
        return altura_real

    return confere(arvore.raiz) != -1


def verificar_rubro_negra(arvore, nome):
    nil = arvore.NIL

    if nil.cor != PRETO:
        erros.append(f"{nome}: o NIL nao e preto")
        return False
    if arvore.raiz is not nil and arvore.raiz.cor != PRETO:
        erros.append(f"{nome}: a raiz nao e preta")
        return False

    def confere(no):
        # devolve a quantidade de nos pretos ate o NIL, ou -1 se achou erro
        if no is nil:
            return 1
        if no.cor == VERMELHO:
            if no.esq.cor == VERMELHO or no.dir.cor == VERMELHO:
                erros.append(f"{nome}: no vermelho {no.chave} com filho vermelho")
                return -1
        # confere os ponteiros pro pai
        if no.esq is not nil and no.esq.pai is not no:
            erros.append(f"{nome}: pai errado no filho esquerdo de {no.chave}")
            return -1
        if no.dir is not nil and no.dir.pai is not no:
            erros.append(f"{nome}: pai errado no filho direito de {no.chave}")
            return -1
        esq = confere(no.esq)
        dir = confere(no.dir)
        if esq == -1 or dir == -1:
            return -1
        if esq != dir:
            erros.append(f"{nome}: alturas negras diferentes no no {no.chave}")
            return -1
        if no.cor == PRETO:
            return esq + 1
        return esq

    return confere(arvore.raiz) != -1


def validar(arvore, tipo, nome):
    if not verificar_bst(arvore, nome):
        return False
    if tipo == "AVL":
        return verificar_avl(arvore, nome)
    if tipo == "Rubro-Negra":
        return verificar_rubro_negra(arvore, nome)
    return True


ARVORES = [("BST", BST), ("AVL", AVL), ("Rubro-Negra", RubroNegra)]


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

def teste_insercao_e_remocao(jogos):
    """Insere tudo em cada cenario validando a cada passo, depois remove tudo."""
    for tipo, classe in ARVORES:
        for cenario, funcao in CENARIOS.items():
            nome = f"{tipo}/{cenario}"
            arvore = classe()
            ordem = funcao(jogos)

            ok = True
            for jogo in ordem:
                arvore.inserir(jogo)
                if not validar(arvore, tipo, nome + " (insercao)"):
                    ok = False
                    break
            conferir(arvore.tamanho == len(jogos), f"{nome}: tamanho final errado")

            if ok:
                # remove todos em ordem aleatoria, validando a cada passo
                ids = [jogo.id for jogo in jogos]
                random.Random(7).shuffle(ids)
                for id_game in ids:
                    removeu = arvore.remover(id_game)
                    conferir(removeu, f"{nome}: nao removeu o id {id_game}")
                    if not validar(arvore, tipo, nome + " (remocao)"):
                        break
                conferir(arvore.tamanho == 0, f"{nome}: nao ficou vazia no final")
                conferir(arvore.altura() == 0, f"{nome}: altura da arvore vazia deveria ser 0")

            print(f"  {nome:<26} {'OK' if not erros else 'ERRO'}")


def teste_busca_sucessor_intervalo(jogos):
    """Compara busca, sucessor e intervalo com o resultado feito 'na forca bruta'."""
    ids = sorted(jogo.id for jogo in jogos)
    for tipo, classe in ARVORES:
        arvore = classe()
        for jogo in CENARIOS["embaralhada"](jogos):
            arvore.inserir(jogo)

        for id_game in ids:
            resultado = arvore.buscar(id_game)
            conferir(resultado["jogo"] is not None and resultado["jogo"].id == id_game,
                     f"{tipo}: busca nao achou o id {id_game}")

        conferir(arvore.buscar(0)["jogo"] is None, f"{tipo}: achou o id 0 que nao existe")
        conferir(arvore.buscar(5000)["jogo"] is None, f"{tipo}: achou o id 5000 que nao existe")

        # sucessor
        for id_game in [0, 1, 2, 500, 999, 1000, 1001]:
            esperado = None
            for i in ids:
                if i > id_game:
                    esperado = i
                    break
            obtido = arvore.sucessor(id_game)
            obtido = None if obtido is None else obtido.id
            conferir(obtido == esperado, f"{tipo}: sucessor de {id_game} deu {obtido}, esperado {esperado}")

        # intervalo
        gerador = random.Random(3)
        for _ in range(50):
            a = gerador.randint(-5, 1005)
            b = gerador.randint(-5, 1005)
            esperado = [i for i in ids if a <= i <= b]
            obtido = [jogo.id for jogo in arvore.intervalo(a, b)]
            conferir(obtido == esperado, f"{tipo}: intervalo [{a}, {b}] errado")

        print(f"  {tipo:<26} {'OK' if not erros else 'ERRO'}")


def teste_repetidos_e_inexistentes(jogos):
    for tipo, classe in ARVORES:
        arvore = classe()
        arvore.inserir(jogos[0])
        conferir(arvore.inserir(jogos[0]) is False, f"{tipo}: aceitou id repetido")
        conferir(arvore.tamanho == 1, f"{tipo}: tamanho errado depois do repetido")
        conferir(arvore.remover(99999) is False, f"{tipo}: removeu id que nao existe")
        conferir(arvore.tamanho == 1, f"{tipo}: tamanho errado depois de remover id inexistente")
        vazia = classe()
        conferir(vazia.buscar(1)["jogo"] is None, f"{tipo}: busca na arvore vazia")
        conferir(vazia.sucessor(1) is None, f"{tipo}: sucessor na arvore vazia")
        conferir(vazia.intervalo(1, 10) == [], f"{tipo}: intervalo na arvore vazia")
        print(f"  {tipo:<26} {'OK' if not erros else 'ERRO'}")


def teste_mistura_aleatoria(jogos):
    """Varias insercoes e remocoes misturadas, comparando com um conjunto (set) do Python."""
    for tipo, classe in ARVORES:
        arvore = classe()
        presentes = set()
        gerador = random.Random(11)
        por_id = {jogo.id: jogo for jogo in jogos}

        for _ in range(3000):
            id_game = gerador.randint(1, 1000)
            if gerador.random() < 0.55:
                inseriu = arvore.inserir(por_id[id_game])
                conferir(inseriu == (id_game not in presentes), f"{tipo}: retorno do inserir errado")
                presentes.add(id_game)
            else:
                removeu = arvore.remover(id_game)
                conferir(removeu == (id_game in presentes), f"{tipo}: retorno do remover errado")
                presentes.discard(id_game)
            if not validar(arvore, tipo, tipo + " (mistura)"):
                break

        ids = [jogo.id for jogo in arvore.em_ordem()]
        conferir(ids == sorted(presentes), f"{tipo}: conteudo final diferente do esperado")
        print(f"  {tipo:<26} {'OK' if not erros else 'ERRO'}")


def teste_altura(jogos):
    """AVL e rubro-negra tem que respeitar o limite teorico de altura."""
    n = len(jogos)
    limite_avl = 1.4405 * math.log2(n + 2)
    limite_rn = 2 * math.log2(n + 1)

    for cenario, funcao in CENARIOS.items():
        ordem = funcao(jogos)
        bst, avl, rn = BST(), AVL(), RubroNegra()
        for jogo in ordem:
            bst.inserir(jogo)
            avl.inserir(jogo)
            rn.inserir(jogo)
        conferir(avl.altura() <= limite_avl, f"AVL/{cenario}: altura {avl.altura()} acima do limite")
        conferir(rn.altura() <= limite_rn, f"Rubro-Negra/{cenario}: altura {rn.altura()} acima do limite")
        print(f"  {cenario:<12} alturas -> BST: {bst.altura():>4} | AVL: {avl.altura():>2} | Rubro-Negra: {rn.altura():>2}")

    # a BST comum tem que degenerar com ids em ordem
    bst = BST()
    for jogo in CENARIOS["crescente"](jogos):
        bst.inserir(jogo)
    conferir(bst.altura() == n, "BST/crescente deveria ter altura igual ao numero de jogos")


def main():
    jogos = carregar_dados(CAMINHO)
    print(f"{len(jogos)} jogos carregados\n")

    testes = [
        ("Insercao e remocao validando a cada passo", teste_insercao_e_remocao),
        ("Busca, sucessor e intervalo", teste_busca_sucessor_intervalo),
        ("Repetidos, inexistentes e arvore vazia", teste_repetidos_e_inexistentes),
        ("Mistura aleatoria de insercoes e remocoes", teste_mistura_aleatoria),
        ("Altura das arvores", teste_altura),
    ]
    for titulo, funcao in testes:
        print(titulo)
        funcao(jogos)
        print()

    if len(erros) == 0:
        print("TODOS OS TESTES PASSARAM")
    else:
        print(f"{len(erros)} ERRO(S) ENCONTRADO(S):")
        for erro in erros[:20]:
            print(" -", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
