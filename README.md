# G40_Arvores_EDA2_2026.2
Repositório dedicado ao Trabalho 3 de Estruturas de Dados 2 do 2º semestre de 2026.

O projeto tem como objetivo implementar e comparar **árvores binárias de busca** (comum e balanceadas), utilizando como base uma tabela contendo informações sobre jogos.

## Alunos

| Matrícula | Nome |
| --- | --- |
| 202023805 | João Paulo Barros de Cristo |

**Disciplina:** Estrutura de Dados 2  
**Professor:** Mauricio Serrano  
**Semestre:** 2026.2

---

## 🎯 Objetivo

Implementar três estruturas estudadas na disciplina e compará-las na prática:

- **BST** (árvore binária de busca comum);
- **AVL**;
- **Árvore Rubro-Negra**.

Todas suportam inserção, busca e remoção, e são comparadas considerando:

- Altura final da árvore;
- Número de rotações;
- Quantidade de comparações por busca;
- Tempo de execução.

---

## 🎮 Cenário

A aplicação é um **catálogo de jogos**. Cada jogo é identificado por um `id_game`, que é a **chave da árvore**, e dois jogos nunca têm o mesmo ID.

### Por que esse contexto?

Os jogos do arquivo estão cadastrados com IDs de 1 a 1000, em ordem crescente. Chaves que chegam ordenadas são o pior caso de uma BST comum: cada novo ID vai para a direita do anterior e a árvore vira uma lista encadeada, com altura próxima de 1000. A AVL e a Rubro-Negra existem justamente para evitar isso, então a base permite mostrar a diferença entre as três estruturas com dados reais.

### Operações que o catálogo precisa suportar

| Operação do catálogo | Operação na árvore |
| --- | --- |
| Existe o jogo com esse ID? | busca |
| Cadastrar um jogo | inserção |
| Descontinuar um jogo | remoção (com rebalanceamento) |
| Qual o próximo ID cadastrado? | sucessor |
| Quais jogos têm ID entre X e Y? | busca por intervalo |

---

## 📋 Escopo

### MVP

- Implementar BST, AVL e Rubro-Negra (inserção, busca e remoção);
- Medir altura final, número de rotações, comparações por busca e tempo de execução;
- Aplicar a estrutura no catálogo (busca por ID, próximo ID, jogos em um intervalo de IDs).

### Extras (planejados)

- Testes automáticos que validam as regras de cada árvore após cada operação;
- Comparação entre três ordens de entrada: crescente, decrescente e embaralhada;
- Gráficos comparativos dos resultados.

---

## 🗃️ Base de Dados

A aplicação utiliza o arquivo `dados/csv de jogos.csv`, com **1000 jogos** reais, e não precisa de nenhum gerador.

| Característica | Valor |
| --- | --- |
| Jogos | 1000 |
| Chave da árvore | `id_game` (único, de 1 a 1000) |
| Anos de lançamento | 1980 a 2016 |
| Plataformas | 24 |
| Ordem das linhas | crescente por `id_game` |

Principais campos usados:

| Campo | Descrição |
| --- | --- |
| `id_game` | identificador do jogo (chave da árvore) |
| `name` | nome do jogo |
| `platform` | plataforma |
| `year_of_release` | ano de lançamento |
| `developer` | desenvolvedora |
| `critic_score` | nota da crítica |
| `user_score` | nota dos usuários |

Alguns registros têm dados faltando (`NULL`, `N/A` ou `tbd`). Esses valores são tratados no carregamento e ficam vazios, sem atrapalhar a árvore, já que a chave (`id_game`) sempre existe.

---

## 🗂️ Estrutura do Projeto

Seguindo o padrão dos trabalhos anteriores:

```text
G40_Arvores_EDA2_2026.2/
│
├── README.md
├── main.py                  # demonstração (menu)
├── comparacao.py            # benchmark entre as três árvores
├── testes.py                # testes de corretude
├── requirements.txt
├── assets/                  # gráficos e dados do benchmark
├── dados/
│   └── csv de jogos.csv
├── modelos/
│   └── jogos.py             # classe Jogo
├── utils/
│   ├── carregador.py        # leitura do CSV
│   └── cenarios.py          # ordens de entrada (crescente, decrescente, embaralhada)
│
└── arvores/
    ├── base.py              # contrato comum das árvores
    ├── bst.py
    ├── avl.py
    └── rubro_negra.py
```

---

## 🛠️ Tecnologias

- Python 3.10+
- matplotlib (para os gráficos, nas etapas finais)

---

## ▶️ Como Executar

As instruções serão atualizadas conforme as etapas forem entregues. Quando o projeto estiver completo:

```bash
pip install -r requirements.txt
python main.py          # demonstração
python testes.py        # testes de corretude
python comparacao.py    # benchmark
```

---

## 🚧 Status do Projeto

- [x] Escolher o contexto (catálogo de jogos) e justificar a escolha
- [x] Definir o modelo de dados e as operações do catálogo
- [ ] Implementar a BST
- [ ] Implementar a AVL
- [ ] Implementar a Rubro-Negra
- [ ] Catálogo de jogos e demonstração (`main.py`)
- [ ] Testes de corretude
- [ ] Benchmark, gráficos e análise experimental
- [ ] Vídeo de apresentação

## Apresentação

(link do vídeo)
