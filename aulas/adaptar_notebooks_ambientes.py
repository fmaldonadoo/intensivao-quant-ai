#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adapta todos os notebooks do Intensivão Quant AI para rodar tanto no
VS Code (Jupyter local) quanto no Google Colab, sem modificação manual.

O que faz:
  1. Insere célula de setup logo após o título de cada notebook
  2. Normaliza todos os caminhos de parquet para usar a variável DADOS_DIR
     - 'arquivo.parquet'            → os.path.join(DADOS_DIR, 'arquivo.parquet')
     - '../../dados/arquivo.parquet' → os.path.join(DADOS_DIR, 'arquivo.parquet')
"""
import json, re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Célula de setup que será inserida em cada notebook ───────────────────────

SETUP_CELL_SOURCE = """\
# ── CONFIGURAÇÃO DO AMBIENTE ─────────────────────────────────────────────────
# Este notebook roda no VS Code (Jupyter local) E no Google Colab.
# Execute esta célula primeiro — ela detecta o ambiente e configura os caminhos.

import os, sys

try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    # ── Google Colab ──────────────────────────────────────────────────────────
    print("Ambiente detectado: Google Colab")

    # Montar Google Drive para persistir os dados entre sessões
    from google.colab import drive
    drive.mount('/content/drive')

    # Instalar dependências não incluídas no Colab por padrão
    import subprocess
    subprocess.run(['pip', 'install', '-q', 'yfinance', 'pyarrow'], check=False)

    # Clonar o repositório do curso (pula automaticamente se já existir)
    REPO_DIR = '/content/intensivao-quant-ai'
    if not os.path.exists(REPO_DIR):
        print("Clonando repositório do curso...")
        subprocess.run([
            'git', 'clone',
            'https://github.com/fmaldonadoo/intensivao-quant-ai.git',
            REPO_DIR
        ])
        print("Repositório clonado com sucesso.")

    # Pasta de dados no Google Drive — persiste entre sessões do Colab
    DADOS_DIR = '/content/drive/MyDrive/intensivao_quant/dados'
    os.makedirs(DADOS_DIR, exist_ok=True)
    print(f"Dados serão salvos em: {DADOS_DIR}")

else:
    # ── VS Code / Jupyter local ───────────────────────────────────────────────
    print("Ambiente detectado: VS Code / Jupyter local")

    # Sobe a árvore de diretórios até encontrar a raiz do repositório (.git)
    _p = os.path.abspath(os.getcwd())
    while _p != os.path.dirname(_p):
        if os.path.exists(os.path.join(_p, '.git')):
            break
        _p = os.path.dirname(_p)

    DADOS_DIR = os.path.join(_p, 'dados')
    os.makedirs(DADOS_DIR, exist_ok=True)
    print(f"Dados serão salvos em: {DADOS_DIR}")
"""

SETUP_MARKER = "IN_COLAB"   # string que indica se o setup já foi inserido


def cell_source_str(cell):
    """Retorna o source de uma célula como string."""
    src = cell.get("source", [])
    return "".join(src) if isinstance(src, list) else src


def make_code_cell(source):
    """Cria um dict de célula de código no formato nbformat 4."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }


def update_parquet_paths(source: str) -> str:
    """
    Normaliza referências a arquivos .parquet para usar DADOS_DIR.

    Padrões tratados:
      '../../dados/arquivo.parquet'  →  os.path.join(DADOS_DIR, 'arquivo.parquet')
      '../dados/arquivo.parquet'     →  os.path.join(DADOS_DIR, 'arquivo.parquet')
      'arquivo.parquet'              →  os.path.join(DADOS_DIR, 'arquivo.parquet')
    """
    # Passo 1: paths com prefixo ../../dados/ ou ../dados/
    source = re.sub(
        r"'(?:\.\.\/)+dados\/([\w\-]+\.parquet)'",
        r"os.path.join(DADOS_DIR, '\1')",
        source
    )
    # Passo 2: paths com só o nome do arquivo (sem pasta)
    # Negative lookbehind: não re-substituir o que já foi processado
    source = re.sub(
        r"(?<!DADOS_DIR, )'([\w\-]+\.parquet)'",
        r"os.path.join(DADOS_DIR, '\1')",
        source
    )
    return source


def adapt_notebook(nb_path: str):
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])

    # ── Verificar se o setup já foi inserido ─────────────────────────────────
    for cell in cells[:4]:   # só olha as primeiras 4 células
        if SETUP_MARKER in cell_source_str(cell):
            print(f"  (já adaptado) {os.path.basename(nb_path)}")
            return

    # ── Inserir célula de setup após a primeira célula (título markdown) ─────
    setup_cell = make_code_cell(SETUP_CELL_SOURCE)
    if cells and cells[0].get("cell_type") == "markdown":
        cells.insert(1, setup_cell)
    else:
        cells.insert(0, setup_cell)

    # ── Atualizar caminhos de parquet em todas as células de código ───────────
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        src = cell_source_str(cell)
        if ".parquet" not in src:
            continue
        new_src = update_parquet_paths(src)
        if new_src != src:
            # Notebook armazena source como lista de strings (uma por linha)
            cell["source"] = [line + ("\n" if not line.endswith("\n") else "")
                              for line in new_src.splitlines()]
            # Remove \n extra da última linha
            if cell["source"]:
                cell["source"][-1] = cell["source"][-1].rstrip("\n")

    nb["cells"] = cells

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    print(f"  Adaptado: {os.path.relpath(nb_path, BASE)}")


if __name__ == "__main__":
    print("Adaptando notebooks para VS Code e Google Colab...\n")
    notebooks = sorted(glob.glob(os.path.join(BASE, "*/aula-*.ipynb")))
    for nb in notebooks:
        adapt_notebook(nb)
    print(f"\nConcluído! {len(notebooks)} notebooks processados.")
