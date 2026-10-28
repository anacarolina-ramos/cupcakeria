"""MODEL: entidades do domínio e mapeamento para o banco de dados."""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

STATUS_PEDIDO = {
    "recebido": "Pedido recebido",
    "em_preparo": "Em preparo",
    "saiu_para_entrega": "Saiu para entrega",
    "entregue": "Entregue",
    "cancelado": "Cancelado",
}

METODOS_PAGAMENTO = {"pix": "PIX", "cartao": "Cartão"}


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    cupcakes = db.relationship("Cupcake", back_populates="categoria")


class Cupcake(db.Model):
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    preco_centavos = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(7), nullable=False, default="#C2185B")  # cor da cobertura
    disponivel = db.Column(db.Boolean, nullable=False, default=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)

    categoria = db.relationship("Categoria", back_populates="cupcakes")

    @property
    def preco(self):
        return self.preco_centavos / 100


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefone = db.Column(db.String(20))

    enderecos = db.relationship("Endereco", back_populates="cliente")
    pedidos = db.relationship("Pedido", back_populates="cliente")


class Endereco(db.Model):
    __tablename__ = "enderecos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    rua = db.Column(db.String(120), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(80))
    bairro = db.Column(db.String(80), nullable=False)
    cidade = db.Column(db.String(80), nullable=False)

    cliente = db.relationship("Cliente", back_populates="enderecos")

    @property
    def completo(self):
        comp = f", {self.complemento}" if self.complemento else ""
        return f"{self.rua}, {self.numero}{comp} - {self.bairro}, {self.cidade} - CEP {self.cep}"


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    endereco_id = db.Column(db.Integer, db.ForeignKey("enderecos.id"), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), nullable=False, default="recebido")
    total_centavos = db.Column(db.Integer, nullable=False)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    endereco = db.relationship("Endereco")
    itens = db.relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    pagamento = db.relationship("Pagamento", back_populates="pedido", uselist=False,
                                cascade="all, delete-orphan")

    @property
    def status_texto(self):
        return STATUS_PEDIDO.get(self.status, self.status)


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    cupcake_id = db.Column(db.Integer, db.ForeignKey("cupcakes.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario_centavos = db.Column(db.Integer, nullable=False)  # preço no momento da compra

    pedido = db.relationship("Pedido", back_populates="itens")
    cupcake = db.relationship("Cupcake")

    @property
    def subtotal_centavos(self):
        return self.quantidade * self.preco_unitario_centavos


class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False, unique=True)
    metodo = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="aprovado")
    valor_centavos = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)

    pedido = db.relationship("Pedido", back_populates="pagamento")

    @property
    def metodo_texto(self):
        return METODOS_PAGAMENTO.get(self.metodo, self.metodo)
