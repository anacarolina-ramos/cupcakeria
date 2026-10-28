-- Projeto físico do banco (PostgreSQL). Gerado a partir dos models em app/models.py.

CREATE TABLE categorias (
	id SERIAL NOT NULL, 
	nome VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
);

CREATE TABLE clientes (
	id SERIAL NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	telefone VARCHAR(20), 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

CREATE TABLE cupcakes (
	id SERIAL NOT NULL, 
	nome VARCHAR(80) NOT NULL, 
	descricao VARCHAR(255) NOT NULL, 
	preco_centavos INTEGER NOT NULL, 
	cor VARCHAR(7) NOT NULL, 
	disponivel BOOLEAN NOT NULL, 
	categoria_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(categoria_id) REFERENCES categorias (id)
);

CREATE TABLE enderecos (
	id SERIAL NOT NULL, 
	cliente_id INTEGER NOT NULL, 
	cep VARCHAR(9) NOT NULL, 
	rua VARCHAR(120) NOT NULL, 
	numero VARCHAR(10) NOT NULL, 
	complemento VARCHAR(80), 
	bairro VARCHAR(80) NOT NULL, 
	cidade VARCHAR(80) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cliente_id) REFERENCES clientes (id)
);

CREATE TABLE pedidos (
	id SERIAL NOT NULL, 
	cliente_id INTEGER NOT NULL, 
	endereco_id INTEGER NOT NULL, 
	criado_em TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	total_centavos INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cliente_id) REFERENCES clientes (id), 
	FOREIGN KEY(endereco_id) REFERENCES enderecos (id)
);

CREATE TABLE itens_pedido (
	id SERIAL NOT NULL, 
	pedido_id INTEGER NOT NULL, 
	cupcake_id INTEGER NOT NULL, 
	quantidade INTEGER NOT NULL, 
	preco_unitario_centavos INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(pedido_id) REFERENCES pedidos (id), 
	FOREIGN KEY(cupcake_id) REFERENCES cupcakes (id)
);

CREATE TABLE pagamentos (
	id SERIAL NOT NULL, 
	pedido_id INTEGER NOT NULL, 
	metodo VARCHAR(10) NOT NULL, 
	status VARCHAR(10) NOT NULL, 
	valor_centavos INTEGER NOT NULL, 
	criado_em TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (pedido_id), 
	FOREIGN KEY(pedido_id) REFERENCES pedidos (id)
);
