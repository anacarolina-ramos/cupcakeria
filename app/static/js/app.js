// Máscara de CEP no formato 00000-000.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-mascara-cep]").forEach((campo) => {
    campo.addEventListener("input", () => {
      const d = campo.value.replace(/\D/g, "").slice(0, 8);
      campo.value = d.length > 5 ? d.slice(0, 5) + "-" + d.slice(5) : d;
    });
  });
});

// Pagamento: mostra o painel do método escolhido, copia o código PIX e aplica máscaras.
document.addEventListener("DOMContentLoaded", () => {
  const paineis = {
    pix: document.getElementById("painel-pix"),
    cartao: document.getElementById("painel-cartao"),
  };
  const atualizarPaineis = () => {
    const escolhido = document.querySelector('input[name="metodo"]:checked');
    Object.entries(paineis).forEach(([metodo, painel]) => {
      if (painel) painel.hidden = !escolhido || escolhido.value !== metodo;
    });
  };
  document.querySelectorAll('input[name="metodo"]').forEach((r) =>
    r.addEventListener("change", atualizarPaineis));
  atualizarPaineis();

  document.querySelectorAll("[data-copiar]").forEach((botao) => {
    botao.addEventListener("click", async () => {
      const origem = document.querySelector(botao.dataset.copiar);
      if (!origem) return;
      try {
        await navigator.clipboard.writeText(origem.value);
      } catch (erro) {
        origem.select();
        document.execCommand("copy");
      }
      const textoOriginal = botao.textContent;
      botao.textContent = "Copiado!";
      setTimeout(() => { botao.textContent = textoOriginal; }, 2000);
    });
  });

  const aplicar = (seletor, formatar) => {
    document.querySelectorAll(seletor).forEach((campo) =>
      campo.addEventListener("input", () => { campo.value = formatar(campo.value); }));
  };
  aplicar("[data-mascara-cartao]", (v) =>
    v.replace(/\D/g, "").slice(0, 19).replace(/(.{4})/g, "$1 ").trim());
  aplicar("[data-mascara-validade]", (v) => {
    const d = v.replace(/\D/g, "").slice(0, 4);
    return d.length > 2 ? d.slice(0, 2) + "/" + d.slice(2) : d;
  });
  aplicar("[data-mascara-cvv]", (v) => v.replace(/\D/g, "").slice(0, 4));
});
