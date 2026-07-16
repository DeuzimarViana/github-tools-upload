#!/usr/bin/env python3
import sys
import time
import os
import json
import requests
from fordev import generators

RECEITAWS_CNPJ = "https://www.receitaws.com.br/v1/cnpj/"
CONFIG_FILE = os.path.expanduser("~/.autocadastral_config.json")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.action_chains import ActionChains
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

UFS = {
    "1": "RO", "2": "AC", "3": "AM", "4": "RR", "5": "PA",
    "6": "AP", "7": "TO", "8": "MA", "9": "PI",
    "10": "CE", "11": "RN", "12": "PB", "13": "PE", "14": "AL",
    "15": "SE", "16": "BA",
    "17": "MG", "18": "ES", "19": "RJ", "20": "SP",
    "21": "PR", "22": "SC", "23": "RS",
    "24": "MS", "25": "MT", "26": "GO", "27": "DF",
}

R = "\033[0m"
BOLD = "\033[1m"
GRAY = "\033[37m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"

BANNER = f"""
{BOLD}{RED}   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄{R}
{BOLD}{RED}  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌{R}
{BOLD}{RED}  ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ {R}
{BOLD}{RED}  ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌         {R}
{BOLD}{YELLOW}  ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ {R}
{BOLD}{YELLOW}  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌{R}
{BOLD}{YELLOW}  ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌ ▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌ ▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ {R}
{BOLD}{YELLOW}  ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌          ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌         {R}
{BOLD}{GREEN}  ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ {R}
{BOLD}{GREEN}  ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌{R}
{BOLD}{GREEN}   ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀{R}
"""

SITUACAO_MAP = {
    "regular": "REGULAR", "ativa": "ATIVA", "suspensa": "SUSPENSA",
    "cancelada": "CANCELADA", "nula": "NULA", "pendente": "PENDENTE",
    "inexistente": "INEXISTENTE", "falecido": "FALECIDO", "baixada": "BAIXADA",
    "inapta": "INAPTA",
}


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def aguardar():
    input("\nPressione ENTER para voltar ao menu...")


def carregar_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"cpfhub_key": ""}


def salvar_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_cpfhub_key():
    return carregar_config().get("cpfhub_key", "")


def validar_cpf(cpf):
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    if len(cpf_limpo) != 11:
        return False
    if cpf_limpo == cpf_limpo[0] * 11:
        return False
    for j in range(9, 11):
        soma = sum(int(cpf_limpo[i]) * (j + 1 - i) for i in range(j))
        resto = (soma * 10) % 11
        if resto == 10:
            resto = 0
        if resto != int(cpf_limpo[j]):
            return False
    return True


def gerar_cpf(uf=""):
    return generators.cpf(uf_code=uf)


def gerar_cnpj():
    return generators.cnpj()


def gerar_empresa(uf="SP"):
    return generators.company(uf_code=uf, data_only=True)


def gerar_pessoa(uf="", sexo="R"):
    dados = generators.people(n=1, sex=sexo, uf_code=uf, data_only=True)[0]
    return {
        "nome": dados.get("nome"),
        "cpf": dados.get("cpf"),
        "rg": dados.get("rg"),
        "data_nasc": dados.get("data_nasc"),
        "sexo": dados.get("sexo"),
        "email": dados.get("email"),
        "celular": dados.get("celular"),
    }


def consultar_cnpj(cnpj):
    cnpj_limpo = "".join(filter(str.isdigit, cnpj))
    if len(cnpj_limpo) != 14:
        return None, "CNPJ deve ter 14 dígitos"
    try:
        resp = requests.get(RECEITAWS_CNPJ + cnpj_limpo, timeout=10)
        if resp.status_code != 200:
            return None, f"Erro HTTP {resp.status_code}"
        dados = resp.json()
        if dados.get("status") == "ERROR":
            return None, dados.get("message", "CNPJ inválido")
        return dados, None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def consultar_cpf_api(cpf):
    api_key = get_cpfhub_key()
    if not api_key:
        return None, (
            "API key não configurada.\n"
            "Cadastre-se grátis em https://app.cpfhub.io/auth/register\n"
            "(50 consultas grátis/mês) e configure a chave no menu."
        )
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    if len(cpf_limpo) != 11:
        return None, "CPF deve ter 11 dígitos"
    try:
        resp = requests.get(
            f"https://api.cpfhub.io/cpf/{cpf_limpo}",
            headers={"x-api-key": api_key, "Accept": "application/json"},
            timeout=10,
        )
        if resp.status_code == 401 or resp.status_code == 403:
            return None, "API key inválida. Verifique a configuração."
        if resp.status_code == 429:
            return None, "Limite de consultas excedido."
        if resp.status_code == 404:
            return None, "CPF não encontrado na base da Receita Federal."
        if resp.status_code != 200:
            return None, f"Erro HTTP {resp.status_code}"
        dados = resp.json().get("data", {})
        return {
            "cpf": dados.get("cpf"),
            "nome": dados.get("name"),
            "situacao": "REGULAR" if dados.get("name") else "DESCONHECIDO",
        }, None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def criar_driver_selenium():
    if not SELENIUM_AVAILABLE:
        return None
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--window-size=1366,768")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=opts)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            window.chrome = {runtime: {}};
        """
    })
    return driver


def consultar_cpf_selenium(cpf, driver):
    driver.get("https://www.situacao-cadastral.com/")
    time.sleep(1.5)
    ActionChains(driver).move_by_offset(100, 150).perform()
    doc_input = driver.find_element(By.ID, "doc")
    doc_input.clear()
    doc_input.send_keys(cpf)
    ActionChains(driver).move_by_offset(10, 10).perform()
    driver.find_element(By.ID, "consultar").click()
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "resultado"))
        )
    except Exception:
        return None, "Timeout ou site bloqueou a consulta"
    html = driver.page_source
    situacao_raw = ""
    nome = ""
    for cls in ("vrd", "vrm", "amr", "cnz"):
        els = driver.find_elements(By.CSS_SELECTOR, f"span.dados.situacao span.{cls}")
        if els:
            situacao_raw = els[0].text.strip()
            break
    if not situacao_raw:
        els = driver.find_elements(By.CSS_SELECTOR, "span.dados.situacao")
        if els:
            situacao_raw = els[0].text.strip()
    sit_key = situacao_raw.lower().replace("situação:", "").strip()
    situacao = SITUACAO_MAP.get(sit_key, situacao_raw or "DESCONHECIDO")
    try:
        nome = driver.find_element(By.CSS_SELECTOR, "span.dados.nome").text.strip()
    except Exception:
        pass
    return {"situacao": situacao, "nome": nome, "raw": situacao_raw}, None


def consultar_cpf(cpf, usar_selenium=False):
    if usar_selenium:
        if not SELENIUM_AVAILABLE:
            return None, "Selenium não disponível. Instale com: pip install selenium"
        driver = criar_driver_selenium()
        if not driver:
            return None, "Falha ao criar driver Selenium"
        try:
            return consultar_cpf_selenium(cpf, driver)
        finally:
            driver.quit()
    return consultar_cpf_api(cpf)


def filtrar_cnpjs():
    entrada = input("Arquivo de entrada (padrão: cnpjs.txt): ").strip() or "cnpjs.txt"
    saida = input("Arquivo de saída (padrão: cnpjs_ativos.txt): ").strip() or "cnpjs_ativos.txt"
    try:
        with open(entrada) as f:
            cnpjs = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo {entrada} não encontrado!")
        aguardar()
        return
    if not cnpjs:
        print("Nenhum CNPJ encontrado no arquivo.")
        aguardar()
        return
    ativos = []
    total = len(cnpjs)
    for i, cnpj in enumerate(cnpjs, 1):
        print(f"[{i}/{total}] Consultando {cnpj}...", end=" ")
        dados, erro = consultar_cnpj(cnpj)
        if dados and dados.get("situacao") == "ATIVA":
            ativos.append(cnpj)
            print("ATIVO")
        elif dados:
            print(dados.get("situacao"))
        else:
            print(f"Erro: {erro}")
        if i < total:
            time.sleep(20)
    with open(saida, "w") as f:
        for cnpj in ativos:
            f.write(cnpj + "\n")
    print(f"\nTotal: {total} | Ativos salvos: {len(ativos)} -> {saida}")
    aguardar()


def filtrar_cpfs_situacao():
    api_key = get_cpfhub_key()
    if not api_key:
        print("\nAPI key não configurada!")
        print("Cadastre-se grátis em https://app.cpfhub.io/auth/register")
        print("Depois configure a chave no menu.")
        aguardar()
        return

    entrada = input("Arquivo de entrada (padrão: cpfs_gerados.txt): ").strip() or "cpfs_gerados.txt"
    saida = input("Arquivo de saída (padrão: cpfs_regular.txt): ").strip() or "cpfs_regular.txt"
    try:
        with open(entrada) as f:
            cpfs = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo {entrada} não encontrado!")
        aguardar()
        return
    if not cpfs:
        print("Nenhum CPF encontrado no arquivo.")
        aguardar()
        return
    regulares = []
    total = len(cpfs)
    for i, cpf in enumerate(cpfs, 1):
        print(f"[{i}/{total}] Consultando {cpf}...", end=" ")
        dados, erro = consultar_cpf(cpf, usar_selenium=False)
        if dados and dados.get("situacao") == "REGULAR":
            regulares.append(cpf)
            print("REGULAR")
        elif dados:
            print(dados.get("situacao", "DESCONHECIDO"))
        else:
            print(f"Erro: {erro}")
        if i < total:
            time.sleep(2)
    with open(saida, "w") as f:
        for cpf in regulares:
            f.write(cpf + "\n")
    print(f"\nTotal: {total} | Regulares salvos: {len(regulares)} -> {saida}")
    aguardar()


def configurar_api_key():
    limpar()
    print(BANNER)
    atual = get_cpfhub_key()
    if atual:
        print(f"Chave atual: {atual[:8]}...{atual[-4:]}")
    else:
        print("Nenhuma chave configurada.")
    print("\nPara obter uma chave grátis:")
    print("1. Acesse https://app.cpfhub.io/auth/register")
    print("2. Crie sua conta (50 consultas grátis/mês)")
    print("3. Copie sua API Key no dashboard")
    nova = input("\nDigite a nova API Key (ou ENTER para cancelar): ").strip()
    if nova:
        config = carregar_config()
        config["cpfhub_key"] = nova
        salvar_config(config)
        print("Chave salva com sucesso!")
    else:
        print("Operação cancelada.")
    aguardar()


def escolher_uf():
    print("\nEstados:")
    for cod, sigla in sorted(UFS.items(), key=lambda x: int(x[0])):
        print(f"  [{cod:>2}] {sigla}")
    print("  [0] Aleatório")
    op = input("\nCódigo do estado: ").strip()
    return UFS.get(op, "")


def menu_gerar():
    limpar()
    print(BANNER)
    print("  [1] Gerar CPF")
    print("  [2] Gerar CNPJ")
    print("  [3] Gerar Pessoa")
    print("  [4] Gerar Empresa")
    op = input("\nEscolha: ").strip()
    if op == "1":
        uf = escolher_uf()
        print(f"\nCPF: {gerar_cpf(uf)}")
    elif op == "2":
        print(f"\nCNPJ: {gerar_cnpj()}")
    elif op == "3":
        print("\nSexo: [M]asc, [F]em, [R]andom")
        sexo = input("Escolha: ").strip().upper() or "R"
        if sexo not in ("M", "F", "R"):
            sexo = "R"
        uf = escolher_uf()
        dados = gerar_pessoa(uf, sexo)
        print(f"\n  Nome: {dados['nome']}")
        print(f"  CPF: {dados['cpf']}")
        print(f"  RG: {dados['rg']}")
        print(f"  Data Nasc.: {dados['data_nasc']}")
        print(f"  Sexo: {dados['sexo']}")
        print(f"  Email: {dados['email']}")
        print(f"  Celular: {dados['celular']}")
    elif op == "4":
        uf = escolher_uf()
        if not uf:
            uf = "SP"
        dados = gerar_empresa(uf)
        print(f"\n  Razão Social: {dados.get('Nome')}")
        print(f"  CNPJ: {dados.get('CNPJ')}")
        print(f"  Inscrição Estadual: {dados.get('Inscrição Estadual')}")
        print(f"  Endereço: {dados.get('Endereço', '')}, {dados.get('Número', '')} - "
              f"{dados.get('Bairro', '')}, {dados.get('Cidade', '')}/{dados.get('Estado', uf)}")
        print(f"  CEP: {dados.get('CEP', '')}")
        print(f"  Telefone: {dados.get('Telefone', '')}")
        print(f"  Email: {dados.get('E-Mail', '')}")
    else:
        print("Opção inválida.")
    aguardar()


def menu_consultar():
    limpar()
    print(BANNER)
    tipo = input("Consultar [1] CNPJ ou [2] CPF? ").strip()
    if tipo == "2":
        doc = input("Digite o CPF (com ou sem pontuação): ").strip()
        print("\nMétodo: [1] API CPFHub (requer key) ou [2] Selenium (experimental)")
        metodo = input("Escolha: ").strip()
        usar_selenium = metodo == "2"
        dados, erro = consultar_cpf(doc, usar_selenium)
        if erro:
            print(f"\nErro: {erro}")
            aguardar()
            return
        print("\n" + "=" * 42)
        print("  CPF: " + doc)
        print("  Nome: " + (dados.get("nome", "") or "---"))
        print("  Situação: " + dados.get("situacao", ""))
        print("=" * 42)
    else:
        doc = input("Digite o CNPJ (com ou sem pontuação): ").strip()
        dados, erro = consultar_cnpj(doc)
        if erro:
            print(f"\nErro: {erro}")
            aguardar()
            return
        print("\n" + "=" * 42)
        print("  CNPJ: " + dados.get("cnpj", ""))
        print("  Razão Social: " + dados.get("nome", ""))
        print("  Situação: " + dados.get("situacao", ""))
        print("  Data Situação: " + dados.get("data_situacao", ""))
        print("  Abertura: " + dados.get("abertura", ""))
        print("  Município/UF: " + dados.get("municipio", "") + " - " + dados.get("uf", ""))
        if dados.get("atividade_principal"):
            print("  Atividade: " + dados["atividade_principal"][0].get("text", ""))
        print("=" * 42)
    aguardar()


def validar_lote_cpf():
    entrada = input("Arquivo de entrada (padrão: cpfs_gerados.txt): ").strip() or "cpfs_gerados.txt"
    saida = input("Arquivo de saída (padrão: cpfs_validos.txt): ").strip() or "cpfs_validos.txt"
    try:
        with open(entrada) as f:
            cpfs = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo {entrada} não encontrado!")
        aguardar()
        return
    if not cpfs:
        print("Nenhum CPF encontrado no arquivo.")
        aguardar()
        return
    validos = []
    invalidos = []
    for cpf in cpfs:
        if validar_cpf(cpf):
            validos.append(cpf)
        else:
            invalidos.append(cpf)
    with open(saida, "w") as f:
        for cpf in validos:
            f.write(cpf + "\n")
    print(f"\nResultado: {len(validos)} válidos | {len(invalidos)} inválidos")
    print(f"Válidos salvos em: {saida}")
    aguardar()


def gerar_lote_cpf(uf=""):
    try:
        qtd = int(input("Quantos CPFs gerar? ").strip())
    except ValueError:
        print("Número inválido.")
        aguardar()
        return
    saida = input("Arquivo de saída (padrão: cpfs_gerados.txt): ").strip() or "cpfs_gerados.txt"
    with open(saida, "w") as f:
        for _ in range(qtd):
            f.write(gerar_cpf(uf) + "\n")
    print(f"\n{qtd} CPFs gerados em {saida}")
    aguardar()


def consultar_lote_cpf():
    api_key = get_cpfhub_key()
    if not api_key:
        print("\nAPI key não configurada!")
        print("Cadastre-se grátis em https://app.cpfhub.io/auth/register")
        print("Depois configure a chave no menu.")
        aguardar()
        return

    entrada = input("Arquivo de entrada (padrão: cpfs_validos.txt): ").strip() or "cpfs_validos.txt"
    saida = input("Arquivo de saída (padrão: cpfs_regular.txt): ").strip() or "cpfs_regular.txt"
    try:
        with open(entrada) as f:
            cpfs = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo {entrada} não encontrado!")
        aguardar()
        return
    if not cpfs:
        print("Nenhum CPF encontrado no arquivo.")
        aguardar()
        return
    regulares = []
    total = len(cpfs)
    print(f"\nConsultando {total} CPFs na Receita Federal...\n")
    for i, cpf in enumerate(cpfs, 1):
        print(f"[{i}/{total}] {cpf} -> ", end="", flush=True)
        dados, erro = consultar_cpf_api(cpf)
        if dados and dados.get("situacao") == "REGULAR":
            regulares.append(cpf)
            nome = dados.get("nome", "---")
            print(f"REGULAR ({nome})")
        elif dados:
            print(dados.get("situacao", "DESCONHECIDO"))
        else:
            print(f"{erro}")
        if i < total:
            time.sleep(2)
    with open(saida, "w") as f:
        for cpf in regulares:
            f.write(cpf + "\n")
    print(f"\nTotal: {total} | Regulares: {len(regulares)} | Salvos em: {saida}")
    aguardar()


def main():
    while True:
        limpar()
        print(BANNER)
        print(f"  {GREEN}[1]{R} {GRAY}Gerar CPF / CNPJ / Pessoa{R}")
        print(f"  {CYAN}[2]{R} {GRAY}Consultar situação cadastral{R}")
        print(f"  {YELLOW}[3]{R} {GRAY}Filtrar CNPJs ativos (lote){R}")
        print(f"  {MAGENTA}[4]{R} {GRAY}Filtrar CPFs válidos (lote){R}")
        print(f"  {BLUE}[5]{R} {GRAY}Filtrar CPFs regulares (situação cadastral){R}")
        print(f"  {RED}[6]{R} {GRAY}Gerar lote de CPFs{R}")
        print(f"  {GREEN}[7]{R} {GRAY}Configurar API Key (CPFHub){R}")
        print(f"  {CYAN}[8]{R} {GRAY}Consultar CPFs do arquivo (lote){R}")
        print(f"  {RED}[0]{R} {GRAY}Sair{R}")
        op = input(f"\n{BOLD}{YELLOW}Escolha: {R}").strip()
        if op == "1":
            menu_gerar()
        elif op == "2":
            menu_consultar()
        elif op == "3":
            limpar()
            print(BANNER)
            filtrar_cnpjs()
        elif op == "4":
            limpar()
            print(BANNER)
            validar_lote_cpf()
        elif op == "5":
            limpar()
            print(BANNER)
            filtrar_cpfs_situacao()
        elif op == "6":
            limpar()
            print(BANNER)
            uf = escolher_uf()
            gerar_lote_cpf(uf)
        elif op == "7":
            configurar_api_key()
        elif op == "8":
            limpar()
            print(BANNER)
            consultar_lote_cpf()
        elif op == "0":
            print("\nEncerrando...")
            sys.exit(0)
        else:
            print("Opção inválida.")
            aguardar()


if __name__ == "__main__":
    main()
