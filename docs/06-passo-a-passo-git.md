# 6. Colocando no GitHub
1. No github.com: **New repository** → nome `cupcakeria` → público → **sem** README → Create.
2. Na pasta do projeto, no terminal:
```bash
git init
git add .
git commit -m "Projeto Cupcakeria: código, testes e documentação"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/cupcakeria.git
git push -u origin main
```
3. Faça commits pequenos a cada melhoria (ex.: `git commit -m "Corrige validação de CEP"`) e `git push`.
