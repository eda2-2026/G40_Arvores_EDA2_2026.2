import time

from utils.carregador import carregar_dados
from utils.cenarios import CENARIOS
from modelos.jogos import Jogo
from arvores.bst import BST
from arvores.avl import AVL
from arvores.rubro_negra import RubroNegra

caminho_arquivo = 'dados/csv de jogos.csv'

jogos_listados = carregar_dados(caminho_arquivo)
print(f"Total de jogos carregados: {len(jogos_listados)}")

TIPOS = {
    "1": ("BST", BST),
    "2": ("AVL", AVL),
    "3": ("Rubro-Negra", RubroNegra),
}


def montar_arvore():
    print("\nQual árvore você quer usar?")
    print("1 - BST (sem balanceamento)")
    print("2 - AVL")
    print("3 - Rubro-Negra")
    opcao = input("Escolha: ")
    while opcao not in TIPOS:
        opcao = input("Opção inválida. Escolha 1, 2 ou 3: ")

    print("\nEm que ordem os jogos serão inseridos?")
    print("1 - Crescente (a ordem do arquivo)")
    print("2 - Decrescente")
    print("3 - Embaralhada")
    ordem = input("Escolha: ")
    nomes_cenarios = {"1": "crescente", "2": "decrescente", "3": "embaralhada"}
    while ordem not in nomes_cenarios:
        ordem = input("Opção inválida. Escolha 1, 2 ou 3: ")
    cenario = nomes_cenarios[ordem]

    nome, classe = TIPOS[opcao]
    arvore = classe()

    inicio = time.time()
    for jogo in CENARIOS[cenario](jogos_listados):
        arvore.inserir(jogo)
    fim = time.time()

    print(f"\n{nome} montada com {arvore.tamanho} jogos (ordem {cenario})")
    print(f"Altura: {arvore.altura()}")
    print(f"Rotações: {arvore.rotacoes}")
    print(f"Comparações nas inserções: {arvore.comparacoes}")
    print(f"Tempo: {(fim - inicio) * 1000:.3f} ms")
    return nome, arvore


def ler_inteiro(texto):
    valor = input(texto)
    while not valor.strip().lstrip("-").isdigit():
        valor = input("Digite um número inteiro: ")
    return int(valor)


nome_arvore, arvore = montar_arvore()

while True:
    print(f"\n===== CATÁLOGO DE JOGOS ({nome_arvore}) =====")
    print("1 - Buscar jogo por ID")
    print("2 - Cadastrar um jogo")
    print("3 - Descontinuar um jogo")
    print("4 - Próximo ID cadastrado")
    print("5 - Jogos em um intervalo de IDs")
    print("6 - Estatísticas da árvore")
    print("7 - Desenhar o começo da árvore")
    print("8 - Trocar de árvore")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "0":
        break

    elif opcao == "1":
        id_desejado = ler_inteiro("Digite o ID do jogo que deseja buscar: ")
        resultado = arvore.buscar(id_desejado)
        if resultado["jogo"] is not None:
            print("\nJogo encontrado!")
            print(resultado["jogo"])
        else:
            print("\nJogo não encontrado.")
        print(f"Total de comparações realizadas: {resultado['comparacoes']}")

    elif opcao == "2":
        novo_id = ler_inteiro("ID do novo jogo: ")
        nome = input("Nome do jogo: ")
        plataforma = input("Plataforma: ")
        ano = ler_inteiro("Ano de lançamento: ")
        novo_jogo = Jogo(novo_id, nome, ano, None, plataforma, None, None)

        rotacoes_antes = arvore.rotacoes
        if arvore.inserir(novo_jogo):
            print("\nJogo cadastrado!")
            print(f"Rotações nessa inserção: {arvore.rotacoes - rotacoes_antes}")
        else:
            print("\nJá existe um jogo com esse ID.")

    elif opcao == "3":
        id_remover = ler_inteiro("ID do jogo que será descontinuado: ")
        rotacoes_antes = arvore.rotacoes
        if arvore.remover(id_remover):
            print("\nJogo descontinuado!")
            print(f"Rotações nessa remoção: {arvore.rotacoes - rotacoes_antes}")
        else:
            print("\nJogo não encontrado.")

    elif opcao == "4":
        id_atual = ler_inteiro("A partir de qual ID? ")
        proximo = arvore.sucessor(id_atual)
        if proximo is not None:
            print("\nPróximo jogo cadastrado:")
            print(proximo)
        else:
            print("\nNão existe jogo com ID maior que esse.")

    elif opcao == "5":
        inicio_id = ler_inteiro("ID inicial: ")
        fim_id = ler_inteiro("ID final: ")
        encontrados = arvore.intervalo(inicio_id, fim_id)
        print(f"\n{len(encontrados)} jogo(s) no intervalo. Mostrando até 10:")
        for jogo in encontrados[:10]:
            print(jogo)

    elif opcao == "6":
        print(f"\nTamanho: {arvore.tamanho} jogos")
        print(f"Altura: {arvore.altura()}")
        print(f"Rotações até agora: {arvore.rotacoes}")
        print(f"Comparações em inserções e remoções: {arvore.comparacoes}")

    elif opcao == "7":
        # (V) = no vermelho, so aparece na rubro-negra
        linhas = arvore.niveis(5)
        print("\nPrimeiros níveis (\"-\" = sem filho):")
        for i in range(len(linhas)):
            print(f"Nível {i + 1}: " + "  ".join(linhas[i]))
        if arvore.altura() > len(linhas):
            print(f"... a árvore tem {arvore.altura()} níveis no total")

    elif opcao == "8":
        nome_arvore, arvore = montar_arvore()

    else:
        print("Opção inválida.")
