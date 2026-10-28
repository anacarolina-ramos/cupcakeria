# 1. Escopo revisado (Kaizen sobre a PIT I)

**Problema:** o app anterior não atendeu o cliente por erros de interpretação dos requisitos.
**Solução:** web app responsivo da Cupcakeria, construído a partir de User Stories priorizadas.

| ID | História | Prioridade | Situação |
|---|---|---|---|
| US01 | Ver fotos e descrições dos cupcakes | Alta | Implementada |
| US02 | Adicionar itens ao carrinho | Alta | Implementada |
| US03 | Escolher PIX/Cartão para pagar | Alta | Implementada (simulado) |
| US04 | Dono cadastra sabores e preços | Alta | Implementada |
| US05 | Cliente informa endereço | Alta | Implementada |
| US06 | Acompanhar status do pedido | Média | Implementada |
| US07 | Entregador vê endereço | Alta | Implementada (área da loja) |
| US08 | Filtrar por categoria | Média | Implementada |
| US09 | Dono recebe alerta de novos pedidos | Alta | Implementada (aviso na tela) |
| US10 | Editar quantidades no carrinho | Média | Implementada |
| US11 | Dono desativa sabores esgotados | Alta | Implementada |
| US12 | Confirmação por e-mail | Média | Simulada (texto na tela) |
| US13 | Relatórios de vendas | Baixa | Implementada (resumo) |
| US14 | Entregador marca "Entregue" | Alta | Implementada (área da loja) |
| US15 | Histórico de pedidos | Baixa | Não implementada |

**Decisões de simplificação (a registrar no vídeo):**
- Não há login de cliente: o cliente é identificado pelo e-mail no checkout e acompanha o pedido com número + e-mail.
- Dono e entregador usam a mesma área protegida por senha.
- Pagamento e e-mail são simulados (sem operadora real nem servidor de e-mail).
- Valores guardados em centavos (inteiros) para evitar erro de arredondamento.

**Requisitos não funcionais:** responsivo (celular), validação de entradas, proteção CSRF, senha do admin em variável de ambiente, testes automatizados.
