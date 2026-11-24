# Login no GitHub pelo navegador

O menu principal de `github-tools-upload.sh` possui a opção **8 — Login no GitHub pelo navegador**.

Ao selecionar, o script:

1. verifica se o GitHub CLI (`gh`) está instalado;
2. executa `gh auth login --hostname github.com --git-protocol ssh --web`;
3. abre o fluxo oficial no navegador;
4. confirma a sessão com `gh auth status`.

O script não recebe, grava ou registra tokens nem senhas. As credenciais são gerenciadas pelo GitHub CLI.

Para login direto com uma conta Google, a conta precisa estar disponível pelo SSO da organização no GitHub. Uma conta Google pessoal não substitui a autenticação do GitHub.

Instalação no Linux:

```bash
sudo apt update
sudo apt install gh
chmod +x github-tools-upload.sh
./github-tools-upload.sh
```
