"""Regra de negócio: criação do pedido a partir do carrinho."""
from .models import Cliente, Endereco, ItemPedido, Pagamento, Pedido, db


def criar_pedido(dados, itens):
    """Grava cliente, endereço, pedido, itens e pagamento (simulado) em uma transação."""
    cliente = Cliente.query.filter_by(email=dados["email"]).first()
    if cliente is None:
        cliente = Cliente(email=dados["email"], nome=dados["nome"])
        db.session.add(cliente)
    cliente.nome = dados["nome"]
    cliente.telefone = dados["telefone"] or None

    endereco = Endereco(
        cliente=cliente, cep=dados["cep"], rua=dados["rua"], numero=dados["numero"],
        complemento=dados["complemento"] or None, bairro=dados["bairro"], cidade=dados["cidade"],
    )
    total = sum(i["subtotal_centavos"] for i in itens)
    pedido = Pedido(cliente=cliente, endereco=endereco, total_centavos=total)
    for i in itens:
        pedido.itens.append(ItemPedido(
            cupcake_id=i["cupcake"].id,
            quantidade=i["quantidade"],
            preco_unitario_centavos=i["cupcake"].preco_centavos,
        ))
    # Pagamento simulado: sempre aprovado (não há integração com operadora real)
    pedido.pagamento = Pagamento(metodo=dados["metodo"], valor_centavos=total, status="aprovado")
    db.session.add(pedido)
    db.session.commit()
    return pedido
