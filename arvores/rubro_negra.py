# Arvore Rubro-Negra
# Regras:
#   1. todo no e vermelho ou preto
#   2. a raiz e preta
#   3. no vermelho nao tem filho vermelho
#   4. todo caminho de um no ate suas folhas (NIL) tem a mesma quantidade de nos pretos
# Em vez de usar None, usamos um unico no "NIL" (sentinela, sempre preto) no lugar das folhas.
# Isso deixa o codigo da remocao bem mais simples.

from arvores.base import ArvoreBase, No, PRETO, VERMELHO


class RubroNegra(ArvoreBase):

    def __init__(self):
        ArvoreBase.__init__(self)
        self.NIL = No(None, None)
        self.NIL.cor = PRETO
        self.NIL.esq = self.NIL
        self.NIL.dir = self.NIL
        self.NIL.pai = self.NIL
        self.raiz = self.NIL

    # ---------- rotacoes ----------

    def rotacao_esquerda(self, x):
        y = x.dir
        x.dir = y.esq
        if y.esq is not self.NIL:
            y.esq.pai = x
        y.pai = x.pai
        if x.pai is self.NIL:
            self.raiz = y
        elif x is x.pai.esq:
            x.pai.esq = y
        else:
            x.pai.dir = y
        y.esq = x
        x.pai = y
        self.rotacoes += 1

    def rotacao_direita(self, y):
        x = y.esq
        y.esq = x.dir
        if x.dir is not self.NIL:
            x.dir.pai = y
        x.pai = y.pai
        if y.pai is self.NIL:
            self.raiz = x
        elif y is y.pai.esq:
            y.pai.esq = x
        else:
            y.pai.dir = x
        x.dir = y
        y.pai = x
        self.rotacoes += 1

    # ---------- inserir ----------

    def inserir(self, jogo):
        chave = jogo.id
        pai = self.NIL
        atual = self.raiz

        while atual is not self.NIL:
            self.comparacoes += 1
            if chave == atual.chave:
                return False  # id repetido
            pai = atual
            if chave < atual.chave:
                atual = atual.esq
            else:
                atual = atual.dir

        novo = No(chave, jogo)
        novo.esq = self.NIL
        novo.dir = self.NIL
        novo.pai = pai
        novo.cor = VERMELHO  # no novo sempre entra vermelho

        if pai is self.NIL:
            self.raiz = novo
        elif chave < pai.chave:
            pai.esq = novo
        else:
            pai.dir = novo

        self.tamanho += 1
        self.consertar_insercao(novo)
        return True

    def consertar_insercao(self, z):
        # o unico problema possivel e um no vermelho com pai vermelho
        while z.pai.cor == VERMELHO:
            if z.pai is z.pai.pai.esq:
                tio = z.pai.pai.dir
                if tio.cor == VERMELHO:
                    # caso 1: tio vermelho -> so troca as cores e sobe
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z is z.pai.dir:
                        # caso 2: vira o caso 3 com uma rotacao
                        z = z.pai
                        self.rotacao_esquerda(z)
                    # caso 3
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self.rotacao_direita(z.pai.pai)
            else:
                # mesma coisa, so que espelhado
                tio = z.pai.pai.esq
                if tio.cor == VERMELHO:
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z is z.pai.esq:
                        z = z.pai
                        self.rotacao_direita(z)
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self.rotacao_esquerda(z.pai.pai)

        self.raiz.cor = PRETO

    # ---------- remover ----------

    def transplantar(self, u, v):
        # coloca a subarvore v no lugar da subarvore u
        if u.pai is self.NIL:
            self.raiz = v
        elif u is u.pai.esq:
            u.pai.esq = v
        else:
            u.pai.dir = v
        v.pai = u.pai

    def remover(self, id_game):
        z = self.raiz
        while z is not self.NIL:
            self.comparacoes += 1
            if id_game == z.chave:
                break
            if id_game < z.chave:
                z = z.esq
            else:
                z = z.dir

        if z is self.NIL:
            return False  # nao achou

        y = z
        cor_original = y.cor

        if z.esq is self.NIL:
            x = z.dir
            self.transplantar(z, z.dir)
        elif z.dir is self.NIL:
            x = z.esq
            self.transplantar(z, z.esq)
        else:
            # dois filhos: y e o sucessor (menor da direita)
            y = z.dir
            while y.esq is not self.NIL:
                y = y.esq
            cor_original = y.cor
            x = y.dir
            if y.pai is z:
                x.pai = y
            else:
                self.transplantar(y, y.dir)
                y.dir = z.dir
                y.dir.pai = y
            self.transplantar(z, y)
            y.esq = z.esq
            y.esq.pai = y
            y.cor = z.cor

        self.tamanho -= 1

        # se saiu um no preto, sobrou um "preto a menos" nesse caminho e precisa consertar
        if cor_original == PRETO:
            self.consertar_remocao(x)
        return True

    def consertar_remocao(self, x):
        while x is not self.raiz and x.cor == PRETO:
            if x is x.pai.esq:
                irmao = x.pai.dir
                if irmao.cor == VERMELHO:
                    # caso 1: irmao vermelho
                    irmao.cor = PRETO
                    x.pai.cor = VERMELHO
                    self.rotacao_esquerda(x.pai)
                    irmao = x.pai.dir
                if irmao.esq.cor == PRETO and irmao.dir.cor == PRETO:
                    # caso 2: irmao preto com dois filhos pretos
                    irmao.cor = VERMELHO
                    x = x.pai
                else:
                    if irmao.dir.cor == PRETO:
                        # caso 3
                        irmao.esq.cor = PRETO
                        irmao.cor = VERMELHO
                        self.rotacao_direita(irmao)
                        irmao = x.pai.dir
                    # caso 4
                    irmao.cor = x.pai.cor
                    x.pai.cor = PRETO
                    irmao.dir.cor = PRETO
                    self.rotacao_esquerda(x.pai)
                    x = self.raiz
            else:
                # mesma coisa, so que espelhado
                irmao = x.pai.esq
                if irmao.cor == VERMELHO:
                    irmao.cor = PRETO
                    x.pai.cor = VERMELHO
                    self.rotacao_direita(x.pai)
                    irmao = x.pai.esq
                if irmao.dir.cor == PRETO and irmao.esq.cor == PRETO:
                    irmao.cor = VERMELHO
                    x = x.pai
                else:
                    if irmao.esq.cor == PRETO:
                        irmao.dir.cor = PRETO
                        irmao.cor = VERMELHO
                        self.rotacao_esquerda(irmao)
                        irmao = x.pai.esq
                    irmao.cor = x.pai.cor
                    x.pai.cor = PRETO
                    irmao.esq.cor = PRETO
                    self.rotacao_direita(x.pai)
                    x = self.raiz

        x.cor = PRETO
