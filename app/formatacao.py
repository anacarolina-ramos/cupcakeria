"""Funções de formatação usadas nas views."""


def brl(centavos):
    """Converte centavos (int) em texto no formato R$ 1.234,50."""
    valor = f"{(centavos or 0) / 100:,.2f}"
    valor = valor.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {valor}"
