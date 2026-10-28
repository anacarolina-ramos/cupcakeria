# 4. Projeto de banco de dados

## Conceitual (entidades e cardinalidades)
Categoria 1:N Cupcake · Cliente 1:N Endereço · Cliente 1:N Pedido · Endereço 1:N Pedido · Pedido 1:N ItemPedido · Cupcake 1:N ItemPedido · Pedido 1:1 Pagamento.

## Lógico (3ª Forma Normal)
- categorias(**id**, nome)
- cupcakes(**id**, nome, descricao, preco_centavos, cor, disponivel, *categoria_id*)
- clientes(**id**, nome, email, telefone)
- enderecos(**id**, *cliente_id*, cep, rua, numero, complemento, bairro, cidade)
- pedidos(**id**, *cliente_id*, *endereco_id*, criado_em, status, total_centavos)
- itens_pedido(**id**, *pedido_id*, *cupcake_id*, quantidade, preco_unitario_centavos)
- pagamentos(**id**, *pedido_id*, metodo, status, valor_centavos, criado_em)

Negrito = chave primária; itálico = chave estrangeira. `preco_unitario_centavos` guarda o preço da época da compra (histórico), por isso não fere a 3FN. Nenhum atributo é multivalorado e não há dependência transitiva entre atributos não-chave.

## Físico
Veja `sql/schema.sql` (PostgreSQL). Em desenvolvimento usa-se SQLite com as mesmas tabelas.

## Dicionário de dados
| Tabela | Campo | Tipo | Nulo? | Restrição / domínio |
|---|---|---|---|---|
| categorias | id | SERIAL | Não | PK |
| categorias | nome | VARCHAR(50) | Não | Único |
| cupcakes | id | SERIAL | Não | PK |
| cupcakes | nome | VARCHAR(80) | Não | |
| cupcakes | descricao | VARCHAR(255) | Não | |
| cupcakes | preco_centavos | INTEGER | Não | 1 a 100000 (validado na aplicação) |
| cupcakes | cor | VARCHAR(7) | Não | Hexadecimal `#RRGGBB` |
| cupcakes | disponivel | BOOLEAN | Não | Verdadeiro = aparece na vitrine |
| cupcakes | categoria_id | INTEGER | Não | FK → categorias.id |
| clientes | id | SERIAL | Não | PK |
| clientes | nome | VARCHAR(100) | Não | Mínimo 3 caracteres |
| clientes | email | VARCHAR(120) | Não | Único, formato de e-mail |
| clientes | telefone | VARCHAR(20) | Sim | 10 ou 11 dígitos |
| enderecos | id | SERIAL | Não | PK |
| enderecos | cliente_id | INTEGER | Não | FK → clientes.id |
| enderecos | cep | VARCHAR(9) | Não | `00000-000` |
| enderecos | rua / numero / bairro / cidade | VARCHAR | Não | Obrigatórios |
| enderecos | complemento | VARCHAR(80) | Sim | |
| pedidos | id | SERIAL | Não | PK |
| pedidos | cliente_id / endereco_id | INTEGER | Não | FKs |
| pedidos | criado_em | TIMESTAMP | Não | Data e hora do pedido |
| pedidos | status | VARCHAR(20) | Não | recebido, em_preparo, saiu_para_entrega, entregue, cancelado |
| pedidos | total_centavos | INTEGER | Não | Soma dos itens |
| itens_pedido | id | SERIAL | Não | PK |
| itens_pedido | pedido_id / cupcake_id | INTEGER | Não | FKs |
| itens_pedido | quantidade | INTEGER | Não | 1 a 20 |
| itens_pedido | preco_unitario_centavos | INTEGER | Não | Preço no momento da compra |
| pagamentos | id | SERIAL | Não | PK |
| pagamentos | pedido_id | INTEGER | Não | FK, único (1:1) |
| pagamentos | metodo | VARCHAR(10) | Não | pix ou cartao |
| pagamentos | status | VARCHAR(10) | Não | aprovado (simulado) |
| pagamentos | valor_centavos | INTEGER | Não | Igual ao total do pedido |
| pagamentos | criado_em | TIMESTAMP | Não | |
