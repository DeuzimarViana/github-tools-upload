1. Instalação e Configuração
bash
# Dar permissão de execução
chmod +x github-tools-upload.sh

# Primeira execução (modo interativo)
./github-tools-upload.sh

# Login diretamente pelo navegador
./github-tools-upload.sh login

2. Uso Diário - Modos Disponíveis
Modo Interativo (Menu)

bash
./github-tools-upload.sh
Opção 1: Configurar repositório
Opção 2: Upload de ferramentas
Opção 3: Configurar SSH
Opção 8: Login no GitHub pelo navegador

Modo Rápido (Linha de Comando)

bash
./github-tools-upload.sh quick
./github-tools-upload.sh login

3. Login com GitHub CLI

Instale o GitHub CLI no Linux:

```bash
sudo apt update
sudo apt install gh
```

Selecione a opção 8 no menu ou execute:

```bash
./github-tools-upload.sh login
```

O script usa `gh auth login --hostname github.com --git-protocol ssh --web`. Isso abre o GitHub no navegador e permite usar SSO Google quando configurado pela organização. Login Google pessoal não autentica diretamente no GitHub.

4. Configuração de Token para HTTPS
Para usar HTTPS com token (mais seguro que senha):

Acesse: https://github.com/settings/tokens
Clique em "Generate new token"
Selecione a permissão necessária, normalmente `repo`
Use o token apenas quando o script solicitar

🔧 Solução de Problemas
Erro: "Permission denied (publickey)"

bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com

Erro: "Repository not found"
Verifique se o repositório existe no GitHub.
Confirme permissões de acesso.
Para HTTPS: use token em vez de senha.

💡 Dicas de Organização
Estrutura recomendada:

text
~/tools/
├── recon/
├── exploitation/
├── post-exploit/
├── scripts/
└── README.md

Agendar uploads automáticos (crontab):

bash
0 2 * * * /caminho/para/quick-github.sh "Backup automático diário"
