#!/usr/bin/env bash

# Small launcher for GitHub CLI browser authentication and the upload manager.
set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
UPLOAD_SCRIPT="$SCRIPT_DIR/github-tools-upload.sh"

print_header() {
    printf '\n%s\n' 'GitHub Tools Upload — autenticação'
    printf '%s\n\n' '────────────────────────────────────'
}

login_github() {
    if ! command -v gh >/dev/null 2>&1; then
        printf '%s\n' "GitHub CLI (gh) não está instalado. Instale-o: https://cli.github.com/" >&2
        return 1
    fi

    printf '%s\n' 'O login será feito pelo fluxo oficial do GitHub CLI no navegador.'
    printf '%s\n' 'Se sua organização usa Google como SSO, você poderá selecionar Google na página de login.'
    printf '%s\n\n' 'Isso não vincula uma conta Google pessoal ao GitHub; a autenticação é gerenciada pelo GitHub CLI.'

    gh auth login --hostname github.com --git-protocol ssh --web || {
        printf '%s\n' 'Não foi possível concluir o login.' >&2
        return 1
    }

    if gh auth status --hostname github.com; then
        local login
        login="$(gh api user --hostname github.com --jq .login 2>/dev/null || true)"
        if [[ -n "$login" ]]; then
            printf '\nLogin concluído como: %s\n' "$login"
        else
            printf '\nLogin concluído.\n'
        fi
        return 0
    fi

    printf '%s\n' 'O GitHub CLI não confirmou uma sessão autenticada.' >&2
    return 1
}

check_login() {
    if ! command -v gh >/dev/null 2>&1; then
        printf '%s\n' "GitHub CLI (gh) não está instalado. Instale-o: https://cli.github.com/" >&2
        return 1
    fi
    gh auth status --hostname github.com
}

while true; do
    print_header
    printf '%s\n' '1) Entrar no GitHub pelo navegador'
    printf '%s\n' '2) Verificar sessão do GitHub'
    printf '%s\n' '3) Abrir o gerenciador de uploads'
    printf '%s\n' '0) Sair'
    printf '\n%s' 'Escolha uma opção: '
    IFS= read -r choice || exit 0

    case "$choice" in
        1) login_github ;;
        2) check_login ;;
        3)
            if [[ -x "$UPLOAD_SCRIPT" ]]; then
                exec "$UPLOAD_SCRIPT"
            elif [[ -f "$UPLOAD_SCRIPT" ]]; then
                exec bash "$UPLOAD_SCRIPT"
            else
                printf 'Não encontrei %s\n' "$UPLOAD_SCRIPT" >&2
            fi
            ;;
        0) exit 0 ;;
        *) printf '%s\n' 'Opção inválida.' ;;
    esac

    printf '\n%s' 'Pressione Enter para continuar...'
    IFS= read -r _ || exit 0
done
