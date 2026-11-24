# Login do GitHub pelo navegador

Este repositório inclui `github-login-menu.sh`, um pequeno menu para iniciar o login oficial do GitHub CLI, conferir a sessão ou abrir o gerenciador de uploads.

## Uso

```bash
chmod +x github-login-menu.sh
./github-login-menu.sh
```

Escolha **1) Entrar no GitHub pelo navegador**. O script executa:

```bash
gh auth login --hostname github.com --git-protocol ssh --web
```

O GitHub CLI conduz a autenticação no navegador e guarda as credenciais usando o mecanismo de armazenamento disponível no sistema. O script não pede nem grava senha ou token. É necessário instalar o [GitHub CLI](https://cli.github.com/).

**Sobre Google:** o login é no GitHub, não um OAuth de Google. Se uma organização do GitHub exigir SSO e oferecer Google como provedor, você poderá escolher Google na página de autenticação da organização. Uma conta Google pessoal não substitui a autenticação do GitHub.

A opção **3** abre `github-tools-upload.sh` no mesmo diretório. A autenticação do `gh` fica separada do método de upload SSH/HTTPS configurado no gerenciador existente.
