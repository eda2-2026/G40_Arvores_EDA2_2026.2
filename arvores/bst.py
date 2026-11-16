# BST - arvore binaria de busca comum (sem balanceamento)
# Se os ids chegarem em ordem, ela vira uma lista encadeada.

from arvores.base import ArvoreBase, No


class BST(ArvoreBase):

    def inserir(self, jogo):
        chave = jogo.id
        pai = None
        atual = self.raiz

        # desce ate achar o lugar do novo no
        while atual is not None:
            self.comparacoes += 1
            if chave == atual.chave:
                return False  # id repetido, nao insere
            pai = atual
            if chave < atual.chave:
                atual = atual.esq
            else:
                atual = atual.dir

        novo = No(chave, jogo)
        if pai is None:
            self.raiz = novo
        elif chave < pai.chave:
            pai.esq = novo
        else:
            pai.dir = novo

        self.tamanho += 1
        return True

    def remover(self, id_game):
        pai = None
        atual = self.raiz

        # procura o no que sera removido
        while atual is not None:
            self.comparacoes += 1
            if id_game == atual.chave:
                break
            pai = atual
            if id_game < atual.chave:
                atual = atual.esq
            else:
                atual = atual.dir

        if atual is None:
            return False  # nao achou

        # caso 3: no com dois filhos -> troca pelo sucessor (menor da direita)
        if atual.esq is not None and atual.dir is not None:
            pai_sucessor = atual
            sucessor = atual.dir
            while sucessor.esq is not None:
                pai_sucessor = sucessor
                sucessor = sucessor.esq
            atual.chave = sucessor.chave
            atual.jogo = sucessor.jogo
            # agora o no que realmente sai e o sucessor
            pai = pai_sucessor
            atual = sucessor

        # casos 1 e 2: no com zero ou um filho
        if atual.esq is not None:
            filho = atual.esq
        else:
            filho = atual.dir

        if pai is None:
            self.raiz = filho
        elif pai.esq is atual:
            pai.esq = filho
        else:
            pai.dir = filho

        self.tamanho -= 1
        return True
