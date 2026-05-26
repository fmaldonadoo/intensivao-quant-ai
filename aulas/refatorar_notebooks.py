# -*- coding: utf-8 -*-
"""
Refatora todos os notebooks do Intensivão Quant AI para serem 100% portáveis:
  - Célula 0: instala TUDO que precisa (pip install automático), reinicia kernel se necessário
  - Célula 1: detecta ambiente (VS Code / Colab) e define DADOS_DIR
  - Célula de check: avisa se dados da aula anterior estão faltando
  - Normaliza todos os caminhos para usar DADOS_DIR
"""
import json, re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# CÉLULA 0 — INSTALAÇÃO DE DEPENDÊNCIAS
# Roda antes de qualquer import. Instala o que falta e reinicia o kernel
# automaticamente se algo foi instalado (necessário para o import funcionar).
# ─────────────────────────────────────────────────────────────────────────────

INSTALL_CELL = """\
# ── INSTALAÇÃO AUTOMÁTICA DE DEPENDÊNCIAS ────────────────────────────────────
# Esta célula garante que todas as bibliotecas necessárias estão instaladas.
# Rode ela primeiro — ela detecta o que falta e instala automaticamente.

import subprocess, sys, importlib

PACOTES = {
    'pandas':      'pandas>=2.0',
    'numpy':       'numpy>=1.26',
    'matplotlib':  'matplotlib>=3.8',
    'yfinance':    'yfinance>=0.2.40',
    'pyarrow':     'pyarrow>=15.0',
    'scipy':       'scipy>=1.11',
    'statsmodels': 'statsmodels>=0.14',
    'sklearn':     'scikit-learn>=1.4',
    'anthropic':   'anthropic>=0.25',
}

instalou = False
for modulo, pacote in PACOTES.items():
    try:
        importlib.import_module(modulo)
    except ImportError:
        print(f"Instalando {pacote}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pacote],
                       check=False)
        instalou = True

if instalou:
    print("\\n✓ Instalação concluída.")
    print("  Reiniciando o kernel para carregar as novas bibliotecas...")
    # Reinicia o kernel automaticamente (funciona no VS Code e no Colab)
    try:
        import IPython
        IPython.Application.instance().kernel.do_shutdown(restart=True)
    except Exception:
        print("  Reinicie o kernel manualmente (Ctrl+Shift+P → Restart Kernel)")
        print("  e rode todas as células novamente.")
else:
    print("✓ Todas as dependências já estão instaladas. Pode continuar.")
"""

# ─────────────────────────────────────────────────────────────────────────────
# CÉLULA 1 — CONFIGURAÇÃO DO AMBIENTE (VS Code / Colab + DADOS_DIR)
# ─────────────────────────────────────────────────────────────────────────────

SETUP_CELL = """\
# ── CONFIGURAÇÃO DO AMBIENTE ─────────────────────────────────────────────────
# Detecta se está rodando no VS Code ou no Google Colab e define DADOS_DIR —
# a pasta onde todos os arquivos de dados do curso serão salvos.
# Funciona em qualquer computador, sem precisar alterar nada.

import os, sys, subprocess

try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    # ── Google Colab ──────────────────────────────────────────────────────────
    print("Ambiente: Google Colab")
    from google.colab import drive
    drive.mount('/content/drive')

    # Clonar o repositório do curso se ainda não existir
    REPO_DIR = '/content/intensivao-quant-ai'
    if not os.path.exists(REPO_DIR):
        print("Clonando repositório do curso...")
        subprocess.run(['git', 'clone',
                        'https://github.com/fmaldonadoo/intensivao-quant-ai.git',
                        REPO_DIR], check=False)

    # Dados salvos no Google Drive — persistem entre sessões
    DADOS_DIR = '/content/drive/MyDrive/intensivao_quant/dados'

else:
    # ── VS Code / Jupyter local ───────────────────────────────────────────────
    print("Ambiente: VS Code / Jupyter local")

    # Sobe pastas até encontrar a raiz do repositório (onde fica o .git)
    # Funciona independente de onde o usuário salvou o projeto
    _p = os.path.abspath(os.getcwd())
    _root = None
    while _p != os.path.dirname(_p):
        if os.path.exists(os.path.join(_p, '.git')):
            _root = _p
            break
        _p = os.path.dirname(_p)

    if _root is None:
        # Fallback: usa a pasta onde o notebook está
        _root = os.path.dirname(os.path.abspath('__file__'))

    DADOS_DIR = os.path.join(_root, 'dados')

os.makedirs(DADOS_DIR, exist_ok=True)
print(f"Pasta de dados: {DADOS_DIR}")
"""

# Marcadores para identificar as células
INSTALL_MARKER = "INSTALAÇÃO AUTOMÁTICA DE DEPENDÊNCIAS"
SETUP_MARKER   = "CONFIGURAÇÃO DO AMBIENTE"

# ─────────────────────────────────────────────────────────────────────────────
# CÉLULAS DE VERIFICAÇÃO DE DADOS por notebook
# ─────────────────────────────────────────────────────────────────────────────

CHECKS = {
    'aula-03': (
        ['precos_ibov.parquet', 'retornos_diarios.parquet', 'retornos_mensais.parquet'],
        'aula-02-dados'
    ),
    'aula-04': (
        ['retornos_mensais_limpo.parquet', 'retornos_diarios_limpo.parquet'],
        'aula-03-eda'
    ),
    'aula-05': (
        ['retornos_mensais_limpo.parquet', 'sinal_v1.parquet'],
        'aula-04-sinal-v1'
    ),
    'aula-06': (
        ['retornos_mensais_limpo.parquet', 'retornos_diarios_limpo.parquet',
         'sinal_v1.parquet', 'retorno_carteira_v1.parquet'],
        'aula-05-backtest-v1'
    ),
    'aula-07': (
        ['retornos_mensais_limpo.parquet', 'retornos_diarios_limpo.parquet',
         'sinal_v1.parquet', 'retorno_carteira_v1.parquet'],
        'aula-06-alocacao'
    ),
    'aula-08': (
        ['retornos_mensais_limpo.parquet', 'sinal_v1.parquet',
         'sinal_v2.parquet', 'retorno_carteira_v1.parquet'],
        'aula-07-sinal-v2'
    ),
    'aula-09': (
        ['retornos_mensais_limpo.parquet', 'retorno_carteira_v1.parquet',
         'retorno_walkforward_liquido.parquet'],
        'aula-08-backtest-rigoroso'
    ),
}

def make_check_cell(arquivos, aula_anterior):
    linhas = '\n'.join(f"    os.path.join(DADOS_DIR, '{f}')," for f in arquivos)
    return f"""\
# ── VERIFICAÇÃO DE DADOS DA AULA ANTERIOR ────────────────────────────────────
_necessarios = [
{linhas}
]
_faltando = [f for f in _necessarios if not os.path.exists(f)]
if _faltando:
    print("\\n⚠  Arquivos necessários não encontrados:")
    for f in _faltando:
        print(f"   • {{os.path.basename(f)}}")
    print(f"\\n   Execute primeiro: {aula_anterior}")
    print(f"   Dados esperados em: {{DADOS_DIR}}")
else:
    print("✓  Dados encontrados. Pode continuar.")
"""

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def src(cell):
    s = cell.get('source', [])
    return ''.join(s) if isinstance(s, list) else s

def make_code_cell(source):
    lines = source.splitlines(keepends=True)
    if lines and lines[-1].endswith('\n'):
        lines[-1] = lines[-1].rstrip('\n')
    return {'cell_type': 'code', 'execution_count': None,
            'metadata': {}, 'outputs': [], 'source': lines}

def fix_paths(source):
    # Caminhos com ../../dados/ ou ../dados/
    source = re.sub(
        r"'(?:\.\.[\\/])+dados[\\/]([\w\-\.]+\.(parquet|csv))'",
        r"os.path.join(DADOS_DIR, '\1')", source)
    # Caminhos com só o nome do arquivo
    source = re.sub(
        r"(?<!DADOS_DIR, )'([\w\-]+\.(parquet|csv))'",
        r"os.path.join(DADOS_DIR, '\1')", source)
    return source

def update_or_insert(cells, marker, new_cell, after_idx=0):
    """Substitui célula com marker, ou insere em after_idx+1."""
    for i, cell in enumerate(cells):
        if marker in src(cell):
            cells[i] = new_cell
            return cells, 'updated', i
    cells.insert(after_idx, new_cell)
    return cells, 'inserted', after_idx

# ─────────────────────────────────────────────────────────────────────────────

def refactor(nb_path):
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)

    cells   = nb.get('cells', [])
    nome    = os.path.basename(nb_path)
    changed = False

    # ── 1. Célula de instalação (posição 0, logo antes do título markdown) ───
    install_cell = make_code_cell(INSTALL_CELL)
    cells, action, pos = update_or_insert(cells, INSTALL_MARKER, install_cell, after_idx=0)
    if action == 'inserted':
        # Garante que o título markdown fica antes da instalação
        if cells and cells[0].get('cell_type') == 'markdown' and pos == 0:
            cells.insert(1, cells.pop(0))   # título sobe para [0], install fica [1]
        changed = True
        print(f"  [install inserido]  {nome}")
    else:
        changed = True
        print(f"  [install atualizado] {nome}")

    # ── 2. Célula de setup (logo após install) ───────────────────────────────
    setup_cell = make_code_cell(SETUP_CELL)
    cells, action, pos = update_or_insert(cells, SETUP_MARKER, setup_cell,
                                          after_idx=1)
    if action == 'inserted':
        changed = True
        print(f"  [setup inserido]    {nome}")
    else:
        if src(cells[pos]) != SETUP_CELL:
            changed = True
            print(f"  [setup atualizado]  {nome}")

    # ── 3. Célula de verificação de dados (aulas 03–09) ──────────────────────
    chave = next((k for k in CHECKS if k in nb_path), None)
    if chave:
        arquivos, aula_ant = CHECKS[chave]
        check_src  = make_check_cell(arquivos, aula_ant)
        check_cell = make_code_cell(check_src)
        CHECK_MARKER = "VERIFICAÇÃO DE DADOS DA AULA ANTERIOR"

        # Inserir logo após o bloco de imports (procura célula com 'import pandas')
        import_pos = next(
            (i for i, c in enumerate(cells)
             if 'import pandas' in src(c) or 'import numpy' in src(c)), 3)

        cells, action, _ = update_or_insert(cells, CHECK_MARKER, check_cell,
                                            after_idx=import_pos)
        if action == 'inserted':
            changed = True
            print(f"  [check inserido]    {nome}")

    # ── 4. Normalizar caminhos de parquet/csv ────────────────────────────────
    for cell in cells:
        if cell.get('cell_type') != 'code':
            continue
        orig = src(cell)
        fixado = fix_paths(orig)
        if fixado != orig:
            lines = fixado.splitlines(keepends=True)
            if lines and lines[-1].endswith('\n'):
                lines[-1] = lines[-1].rstrip('\n')
            cell['source'] = lines
            changed = True

    if changed:
        nb['cells'] = cells
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)

    return changed


if __name__ == '__main__':
    print("Refatorando notebooks...\n")
    notebooks = sorted(glob.glob(os.path.join(BASE, '*/aula-*.ipynb')))
    n = sum(1 for nb in notebooks if refactor(nb))
    print(f"\nConcluído! {len(notebooks)} notebooks, {n} modificados.")
