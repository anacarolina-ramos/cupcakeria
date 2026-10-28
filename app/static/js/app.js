// Máscara de CEP no formato 00000-000.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-mascara-cep]").forEach((campo) => {
    campo.addEventListener("input", () => {
      const d = campo.value.replace(/\D/g, "").slice(0, 8);
      campo.value = d.length > 5 ? d.slice(0, 5) + "-" + d.slice(5) : d;
    });
  });
});
