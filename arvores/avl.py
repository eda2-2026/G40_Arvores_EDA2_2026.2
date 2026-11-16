# AVL - arvore binaria de busca balanceada pela altura
# Regra: em todo no, a diferenca de altura entre a subarvore esquerda e a direita
# (fator de balanceamento) e no maximo 1. Quando passa disso, faz rotacao.

from arvores.base import ArvoreBase, No


def altura_do_no(no):
    if no is None:
        return 0
    return no.altura


def atualizar_altura(no):
    esq = altura_do_no(no.esq)
    dir = altura_do_no(no.dir)
    if esq > dir:
        no.altura = esq + 1
    else:
        no.altura = dir + 1


def fator_balanceamento(no):
    if no is None:
        return 0
    return altura_do_no(no.esq) - altura_do_no(no.dir)


class AVL(ArvoreBase):

    def rotacao_direita(self, y):
        x = y.esq
        y.esq = x.dir
        x.dir = y
        atualizar_altura(y)
        atualizar_altura(x)
        self.rotacoes += 1
        return x  # x passa a ser a raiz dessa subarvore

    def rotacao_esquerda(self, x):
        y = x.dir
        x.dir = y.esq
        y.esq = x
        atualizar_altura(x)
        atualizar_altura(y)
        self.rotacoes += 1
        return y

    def balancear(self, no):
        atualizar_altura(no)
        fb = fator_balanceamento(no)

        if fb > 1:
            # lado esquerdo pesado
            if fator_balanceamento(no.esq) < 0:
                no.esq = self.rotacao_esquerda(no.esq)  # caso esquerda-direita
            return self.rotacao_direita(no)

        if fb < -1:
            # lado direito pesado
            if fator_balanceamento(no.dir) > 0:
                no.dir = self.rotacao_direita(no.dir)  # caso direita-esquerda
            return self.rotacao_esquerda(no)

        return no

    # ---------- inserir ----------

    def inserir(self, jogo):
        self.inseriu = False
        self.raiz = self.inserir_no(self.raiz, jogo)
        if self.inseriu:
            self.tamanho += 1
        return self.inseriu

    def inserir_no(self, no, jogo):
        if no is None:
            self.inseriu = True
            return No(jogo.id, jogo)

        self.comparacoes += 1
        if jogo.id == no.chave:
            return no  # id repetido
        if jogo.id < no.chave:
            no.esq = self.inserir_no(no.esq, jogo)
        else:
            no.dir = self.inserir_no(no.dir, jogo)

        return self.balancear(no)

    # ---------- remover ----------

    def remover(self, id_game):
        self.removeu = False
        self.raiz = self.remover_no(self.raiz, id_game)
        if self.removeu:
            self.tamanho -= 1
        return self.removeu

    def remover_no(self, no, id_game):
        if no is None:
            return None

        self.comparacoes += 1
        if id_game < no.chave:
            no.esq = self.remover_no(no.esq, id_game)
        elif id_game > no.chave:
            no.dir = self.remover_no(no.dir, id_game)
        else:
            self.removeu = True
            # zero ou um filho
            if no.esq is None:
                return no.dir
            if no.dir is None:
                return no.esq
            # dois filhos: copia o sucessor (menor da direita) e remove ele la da direita
            sucessor = no.dir
            while sucessor.esq is not None:
                sucessor = sucessor.esq
            no.chave = sucessor.chave
            no.jogo = sucessor.jogo
            no.dir = self.remover_no(no.dir, sucessor.chave)

        return self.balancear(no)
