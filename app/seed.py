"""Dados de exemplo para a vitrine."""
from .models import Categoria, Cupcake, db

CATALOGO = {
    "Clássicos": [
        ("Baunilha com Morango", "Massa de baunilha e cobertura de buttercream de morango.", 900, "#F4A6B8"),
        ("Brigadeiro Belga", "Massa de chocolate e brigadeiro de chocolate belga.", 1100, "#5B3A29"),
        ("Limão Siciliano", "Massa cítrica com cobertura de limão e raspas.", 1000, "#F2E05B"),
    ],
    "Sem açúcar": [
        ("Cacau Zero", "Chocolate 70% adoçado com xilitol, sem açúcar adicionado.", 1300, "#7A4B3A"),
        ("Coco Fit", "Massa de coco com cobertura de cream cheese sem açúcar.", 1250, "#EFE7D8"),
    ],
    "Veganos": [
        ("Red Velvet Vegano", "Sem ovos e sem leite, com creme de coco e beterraba.", 1400, "#B3243B"),
        ("Pistache Vegano", "Massa de pistache com cobertura de castanhas.", 1500, "#A8C686"),
    ],
    "Especiais": [
        ("Doce de Leite com Flor de Sal", "Recheio de doce de leite e flor de sal.", 1450, "#C98B3C"),
        ("Maracujá com Chocolate Branco", "Mousse de maracujá e chocolate branco.", 1350, "#F7C948"),
    ],
}


def seed_se_vazio():
    if Categoria.query.first() is not None:
        return False
    for nome_cat, cupcakes in CATALOGO.items():
        cat = Categoria(nome=nome_cat)
        db.session.add(cat)
        for nome, desc, preco, cor in cupcakes:
            db.session.add(Cupcake(nome=nome, descricao=desc, preco_centavos=preco,
                                   cor=cor, categoria=cat))
    db.session.commit()
    return True
