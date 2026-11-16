import random

# Ordens em que os jogos sao inseridos na arvore.
# O csv ja vem em ordem crescente de id, que e o pior caso da BST comum.

SEMENTE = 42  # semente fixa pra todo mundo gerar a mesma ordem embaralhada


def ordem_crescente(jogos):
    lista = jogos[:]
    lista.sort(key=lambda jogo: jogo.id)
    return lista


def ordem_decrescente(jogos):
    lista = ordem_crescente(jogos)
    lista.reverse()
    return lista


def ordem_embaralhada(jogos):
    lista = jogos[:]
    gerador = random.Random(SEMENTE)
    gerador.shuffle(lista)
    return lista


CENARIOS = {
    "crescente": ordem_crescente,
    "decrescente": ordem_decrescente,
    "embaralhada": ordem_embaralhada,
}
