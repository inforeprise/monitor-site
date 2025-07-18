from flask import Flask, render_template, request, redirect, url_for, flash
import os, json

ARQUIVO_URLS = "urls.txt"
STATUS_ARQUIVO = "status.json"

app = Flask(__name__)
app.secret_key = 'minha_chave_simples'

def carregar_status():
    if os.path.exists(STATUS_ARQUIVO):
        with open(STATUS_ARQUIVO, "r") as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    urls = []
    if os.path.exists(ARQUIVO_URLS):
        with open(ARQUIVO_URLS, 'r') as f:
            urls = [linha.strip() for linha in f if linha.strip()]

    status = carregar_status()
    lista_urls = [{"url": u, "status": status.get(u, "Não verificado")} for u in urls]

    return render_template('index.html', lista_urls=lista_urls)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nova_url = request.form.get('url', '').strip()
    if nova_url:
        with open(ARQUIVO_URLS, 'a') as f:
            f.write(nova_url + '\n')
        flash('URL adicionada com sucesso!', 'success')
    else:
        flash('URL inválida.', 'danger')
    return redirect(url_for('index'))

@app.route('/remover', methods=['POST'])
def remover():
    url_para_remover = request.form.get('url', '').strip()
    if not os.path.exists(ARQUIVO_URLS): return redirect(url_for('index'))

    with open(ARQUIVO_URLS, 'r') as f:
        urls = [linha.strip() for linha in f if linha.strip() and linha.strip() != url_para_remover]

    with open(ARQUIVO_URLS, 'w') as f:
        for u in urls: f.write(u + '\n')

    flash(f'URL removida com sucesso: {url_para_remover}', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
