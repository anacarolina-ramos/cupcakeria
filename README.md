# Cupcakeria

Aplicação web responsiva para uma loja de cupcakes gourmet, com vitrine virtual, carrinho de compras, finalização de pedido com endereço e pagamento simulado, acompanhamento de status e área administrativa para o dono da loja e o entregador.

Projeto Integrador Transdisciplinar em Engenharia de Software II (PIT II), Cruzeiro do Sul Virtual.

**Autora:** Ana Carolina Cassiano Ramos
**RGM:** 31555462

## Endereços do projeto

| Item | Endereço |
|---|---|
| Repositório no GitHub | https://github.com/anacarolina-ramos/cupcakeria |
| Aplicação em funcionamento | https://cupcakeria.onrender.com |

Observação: a aplicação está hospedada no plano gratuito do Render, que suspende o serviço após um período de inatividade. O primeiro acesso pode levar cerca de um minuto para responder.

## 1. Contexto e objetivo

Na etapa anterior (PIT I), foi realizado o levantamento de requisitos de um aplicativo para uma loja de cupcakes gourmet, aplicando metodologias ágeis para evitar erros de interpretação ocorridos em projetos passados. O resultado foi um backlog de 15 histórias de usuário priorizadas, organizadas em três módulos: Vendas, Pagamento e Entrega, e Administração.

Nesta etapa (PIT II), o planejamento foi revisado segundo o princípio de melhoria contínua (Kaizen), implementado, testado e publicado. O objetivo é entregar uma solução funcional que cubra a jornada completa de compra, da visualização dos produtos até a entrega, mantendo documentação, código e testes versionados em um único repositório.

## 2. Funcionalidades

Situação de cada história de usuário do backlog:

| ID | História de usuário | Prioridade | Situação |
|---|---|---|---|
| US01 | Visualizar fotos e descrições dos cupcakes | Alta | Implementada |
| US02 | Adicionar itens ao carrinho | Alta | Implementada |
| US03 | Escolher a forma de pagamento (PIX ou cartão) | Alta | Implementada (pagamento simulado) |
| US04 | Cadastrar sabores e preços | Alta | Implementada |
| US05 | Informar endereço de entrega | Alta | Implementada |
| US06 | Acompanhar o status do pedido | Média | Implementada |
| US07 | Visualizar o endereço do cliente (entregador) | Alta | Implementada (área da loja) |
| US08 | Filtrar cupcakes por categoria | Média | Implementada |
| US09 | Receber alerta de novos pedidos | Alta | Implementada (aviso na tela) |
| US10 | Editar quantidades no carrinho | Média | Implementada |
| US11 | Desativar sabores esgotados | Alta | Implementada |
| US12 | Receber confirmação por e-mail | Média | Simulada (texto exibido na tela) |
| US13 | Consultar relatório de vendas | Baixa | Implementada (resumo) |
| US14 | Marcar pedido como entregue | Alta | Implementada (área da loja) |
| US15 | Consultar histórico de pedidos | Baixa | Não implementada |

### Decisões de projeto e limitações conhecidas

- Não há login de cliente. O cliente é identificado pelo e-mail informado na finalização do pedido e acompanha o pedido por meio do número do pedido e do e-mail. Por esse motivo, a US15 não foi implementada.
- O dono da loja e o entregador compartilham a mesma área administrativa, protegida por senha.
- O pagamento e o envio de e-mail são simulados, sem integração com operadora de pagamento ou servidor de e-mail.
- Os valores monetários são armazenados em centavos (números inteiros) para evitar erros de arredondamento.
- Sabores cadastrados pela área administrativa exibem uma ilustração padrão até que uma foto com o nome correspondente seja adicionada à pasta de imagens.

## 3. Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem do back-end | Python 3 |
| Framework web | Flask (padrão arquitetural MVC) |
| Acesso a dados | SQLAlchemy (Flask-SQLAlchemy) |
| Banco de dados | SQLite (desenvolvimento) e PostgreSQL (produção) |
| Front-end | HTML, CSS e JavaScript (templates Jinja2) |
| Testes automatizados | Pytest |
| Servidor de aplicação | Gunicorn |
| Hospedagem | Render |
| Versionamento | Git e GitHub |
| Modo de codificação | Tradicional |

## 4. Arquitetura

O projeto adota o padrão MVC (Model, View, Controller), que separa a responsabilidade de armazenamento e validação (Model), de apresentação (View) e de fluxo de requisições (Controller).

```
cupcakeria/
├── app/
│   ├── models.py          Model: entidades e mapeamento para o banco
│   ├── controllers/       Controller: rotas e regras de fluxo
│   ├── templates/         View: páginas HTML (Jinja2)
│   ├── static/            CSS, JavaScript e imagens
│   ├── validadores.py     Validação das entradas do usuário
│   ├── carrinho.py        Regras do carrinho de compras
│   ├── pedidos.py         Regras de criação de pedidos
│   ├── config.py          Configurações e variáveis de ambiente
│   └── seed.py            Dados iniciais (sabores de exemplo)
├── tests/                 Testes automatizados (Pytest)
├── sql/schema.sql         Projeto físico do banco de dados
├── docs/                  Documentação do projeto
├── render.yaml            Configuração de implantação no Render
└── requirements.txt       Dependências
```

## 5. Modelo de dados

O banco é composto pelas tabelas `categorias`, `clientes`, `cupcakes`, `enderecos`, `pedidos`, `itens_pedido` e `pagamentos`. O modelo lógico está normalizado até a Terceira Forma Normal. O script de criação encontra-se em `sql/schema.sql`, e o dicionário de dados em `docs/04-banco-de-dados.md`.

## 6. Documentação

| Arquivo | Conteúdo |
|---|---|
| `docs/01-escopo.md` | Escopo revisado, histórias de usuário e decisões de simplificação |
| `docs/02-uml.md` | Diagramas de classes, casos de uso, sequência e atividades |
| `docs/03-ihc.md` | Telas, wireframe, mensagens de erro e princípios de interface aplicados |
| `docs/04-banco-de-dados.md` | Projeto conceitual, lógico e físico, e dicionário de dados |
| `docs/05-modelo-de-teste.md` | Formulário de teste com usuários e modelo do laudo de qualidade |
| `docs/06-passo-a-passo-git.md` | Roteiro de versionamento |

## 7. Como executar localmente

Pré-requisitos: Python 3 e Git instalados.

```bash
git clone https://github.com/anacarolina-ramos/cupcakeria.git
cd cupcakeria

python -m venv .venv
# Windows:    .venv\Scripts\activate
# Linux/Mac:  source .venv/bin/activate

pip install -r requirements.txt
flask --app app run --debug
```

## 8. Testes

### Testes automatizados (verificação)

```bash
python -m pytest -v
```

A suíte contém 55 casos de teste, que cobrem validação de entradas, vitrine e carrinho, finalização e acompanhamento de pedidos e área administrativa.

### Testes com usuários (validação)

A aplicação foi disponibilizada a colegas de curso para teste, conforme o roteiro e o formulário de `docs/05-modelo-de-teste.md`. Os registros individuais e o laudo de qualidade, com erros encontrados, correções e evidências, estão na pasta `docs/`.

## 9. Implantação

A aplicação é implantada no Render por meio do arquivo `render.yaml`, que define o serviço web e o banco PostgreSQL.

1. Enviar o código ao GitHub.
2. No Render, selecionar New, depois Blueprint, e escolher o repositório.
3. Definir o valor da variável `ADMIN_SENHA`.
4. Aguardar a conclusão da implantação e acessar o endereço gerado.

Variáveis de ambiente utilizadas: `DATABASE_URL`, `SECRET_KEY` e `ADMIN_SENHA`.

## 10. Créditos das imagens

As fotografias dos cupcakes, armazenadas em `app/static/img/cupcakes/`, foram obtidas no banco de imagens Pexels (https://www.pexels.com), cuja licença permite o uso gratuito, inclusive em projetos publicados.
