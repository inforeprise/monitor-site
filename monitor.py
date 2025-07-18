import requests, hashlib, time, os, json

ARQUIVO_URLS = "urls.txt"
PASTA_HASHES = "hashes"
STATUS_ARQUIVO = "status.json"
INTERVALO = 300  # 5 minutos

os.makedirs(PASTA_HASHES, exist_ok=True)

def get_hash_do_conteudo(html):
    return hashlib.sha256(html.encode('utf-8')).hexdigest()

def obter_conteudo_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception:
        return None

def carregar_urls():
    if os.path.exists(ARQUIVO_URLS):
        with open(ARQUIVO_URLS, "r") as f:
            return [linha.strip() for linha in f if linha.strip()]
    return []

def carregar_status():
    if os.path.exists(STATUS_ARQUIVO):
        with open(STATUS_ARQUIVO, "r") as f:
            return json.load(f)
    return {}

def salvar_status(status_dict):
    with open(STATUS_ARQUIVO, "w") as f:
        json.dump(status_dict, f, indent=2)

def gerar_nome_arquivo_hash(url):
    return os.path.join(PASTA_HASHES, hashlib.md5(url.encode()).hexdigest() + ".txt")

def verificar_url(url, status_dict):
    html = obter_conteudo_url(url)
    if html is None:
        status_dict[url] = "Erro ao acessar"
        return

    hash_atual = get_hash_do_conteudo(html)
    caminho_hash = gerar_nome_arquivo_hash(url)

    if os.path.exists(caminho_hash):
        with open(caminho_hash, "r") as f:
            hash_anterior = f.read().strip()
        if hash_atual != hash_anterior:
            status_dict[url] = "Mudou"
        else:
            status_dict[url] = "Sem mudanças"
    else:
        status_dict[url] = "Primeira verificação"

    with open(caminho_hash, "w") as f:
        f.write(hash_atual)

def verificar_todas():
    urls = carregar_urls()
    status_dict = carregar_status()
    for url in urls:
        verificar_url(url, status_dict)
    salvar_status(status_dict)

if __name__ == "__main__":
    print("Iniciando monitoramento...")
    while True:
        verificar_todas()
        time.sleep(INTERVALO)
