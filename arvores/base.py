# Contrato comum das tres arvores (BST, AVL e Rubro-Negra).
# Tudo que e igual nas tres (busca, altura, sucessor, intervalo...) fica aqui.
# Cada arvore so implementa o que muda: inserir e remover.
#
# Obs: as funcoes daqui nao usam recursao, porque a BST comum com ids em ordem
# crescente vira uma lista de 1000 nos e estouraria o limite de recursao do Python.

PRETO = "preto"
VERMELHO = "vermelho"


class No:
    def __init__(self, chave, jogo):
        self.chave = chave   # id do jogo
        self.jogo = jogo     # objeto Jogo guardado no no
        self.esq = None
        self.dir = None
        self.pai = None            # so a rubro-negra usa
        self.altura = 1            # so a AVL usa (altura do no)
        self.cor = VERMELHO        # so a rubro-negra usa


class ArvoreBase:

    def __init__(self):
        self.NIL = None   # o que representa "sem no" (a rubro-negra troca por um no sentinela)
        self.raiz = None
        self.tamanho = 0
        self.rotacoes = 0     # total de rotacoes feitas
        self.comparacoes = 0  # comparacoes feitas em inserir e remover

    # ---------- metodos que cada arvore implementa ----------

    def inserir(self, jogo):
        raise NotImplementedError

    def remover(self, id_game):
        raise NotImplementedError

    # ---------- metodos iguais nas tres ----------

    def buscar(self, id_desejado):
        comparacoes = 0  # Contador de comparações
        no = self.raiz
        while no is not self.NIL:
            comparacoes += 1  # Incrementa o contador a cada comparação
            if id_desejado == no.chave:
                return {
                    "jogo": no.jogo,
                    "comparacoes": comparacoes
                }
            if id_desejado < no.chave:
                no = no.esq
            else:
                no = no.dir
        return {
            "jogo": None,
            "comparacoes": comparacoes
        }

    def altura(self):
        # altura = quantidade de niveis (arvore vazia = 0)
        if self.raiz is self.NIL:
            return 0
        maior = 0
        pilha = [(self.raiz, 1)]
        while len(pilha) > 0:
            no, nivel = pilha.pop()
            if nivel > maior:
                maior = nivel
            if no.esq is not self.NIL:
                pilha.append((no.esq, nivel + 1))
            if no.dir is not self.NIL:
                pilha.append((no.dir, nivel + 1))
        return maior

    def em_ordem(self):
        # devolve os jogos ordenados pelo id
        resultado = []
        pilha = []
        no = self.raiz
        while no is not self.NIL or len(pilha) > 0:
            if no is not self.NIL:
                pilha.append(no)
                no = no.esq
            else:
                no = pilha.pop()
                resultado.append(no.jogo)
                no = no.dir
        return resultado

    def sucessor(self, id_game):
        # proximo jogo cadastrado: o menor id que e maior que id_game
        candidato = None
        no = self.raiz
        while no is not self.NIL:
            if no.chave > id_game:
                candidato = no
                no = no.esq
            else:
                no = no.dir
        if candidato is None:
            return None
        return candidato.jogo

    def intervalo(self, id_inicio, id_fim):
        # todos os jogos com id entre id_inicio e id_fim (inclusive)
        resultado = []
        pilha = []
        no = self.raiz
        while no is not self.NIL or len(pilha) > 0:
            if no is not self.NIL:
                pilha.append(no)
                # so vale a pena descer pra esquerda se ainda pode ter id maior que o inicio
                if no.chave > id_inicio:
                    no = no.esq
                else:
                    no = self.NIL
            else:
                no = pilha.pop()
                if no.chave > id_fim:
                    break  # a partir daqui so tem ids maiores
                if no.chave >= id_inicio:
                    resultado.append(no.jogo)
                no = no.dir
        return resultado

    def niveis(self, max_niveis):
        # usado no main pra desenhar o comeco da arvore no terminal
        # devolve uma lista de niveis, cada um com texto tipo "5" ou "5(V)"
        resultado = []
        if self.raiz is self.NIL:
            return resultado
        atual = [self.raiz]
        for _ in range(max_niveis):
            if len(atual) == 0:
                break
            textos = []
            proximo = []
            for no in atual:
                if no is self.NIL:
                    textos.append("-")
                    continue
                texto = str(no.chave)
                if no.cor == VERMELHO and self.NIL is not None:
                    texto += "(V)"
                textos.append(texto)
                proximo.append(no.esq)
                proximo.append(no.dir)
            resultado.append(textos)
            atual = proximo
            # se so sobrou "sem no" nao precisa desenhar o proximo nivel
            if all(n is self.NIL for n in atual):
                break
        return resultado
