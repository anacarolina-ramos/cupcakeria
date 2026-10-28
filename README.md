# Cupcakeria

Aplicativo web (responsivo) de uma loja de cupcakes gourmet: vitrine virtual, carrinho, pedido com endereço e pagamento (simulado), e área do dono da loja. Projeto Integrador Transdisciplinar em Engenharia de Software II.

**Autora:** Ana Carolina Cassiano Ramos · RGM 31555462

## Tecnologias
Python 3 · Flask (padrão MVC) · SQLAlchemy · SQLite (local) / PostgreSQL (produção) · HTML/CSS/JS · Pytest · Render (hospedagem)

## Como rodar no seu computador
```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate        Mac/Linux:  source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```
Abra http://127.0.0.1:5000. Na primeira execução o banco é criado e recebe cupcakes de exemplo.
Área da loja: http://127.0.0.1:5000/admin/login (senha local: `admin123`).

## Testes
```bash
python -m pytest -v
```

## Estrutura (MVC)
```
app/models.py        MODEL      entidades e banco
app/controllers/     CONTROLLER rotas e regras de fluxo
app/templates/       VIEW       páginas HTML (Jinja2)
app/static/          CSS e JS
tests/               testes automatizados (Pytest)
sql/schema.sql       projeto físico do banco (PostgreSQL)
docs/                documentação (escopo, UML, IHC, banco, testes)
```

## Histórias de usuário implementadas
US01 vitrine · US02 carrinho · US03 pagamento (simulado) · US04 cadastro de sabores · US05 endereço · US06 acompanhar status · US07 endereço visível ao entregador · US08 filtro por categoria · US09 alerta de novos pedidos · US10 editar quantidades · US11 marcar sabor esgotado · US13 relatório de vendas · US14 marcar como entregue · US12 e-mail de confirmação (simulado, exibido na tela).
**Não implementadas:** US15 histórico de pedidos por conta (não há login de cliente nesta versão).

## Publicar no Render
1. Suba o projeto no GitHub.
2. Em render.com: **New → Blueprint** e escolha o repositório (usa o `render.yaml`).
3. Quando pedir, defina `ADMIN_SENHA` com uma senha sua.
4. Aguarde o deploy e copie o link `https://....onrender.com`.
O plano gratuito "dorme" após inatividade: o primeiro acesso pode demorar. Confira no site as condições atuais do plano gratuito do banco.
