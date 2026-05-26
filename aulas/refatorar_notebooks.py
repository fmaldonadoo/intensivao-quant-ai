# -*- coding: utf-8 -*-
"""
Refatora todos os notebooks do Intensivão Quant AI para serem 100% portáveis:
  - Setup cell melhorado: instala pyarrow localmente, fallback se .git não existe
  - Célula de verificação de dados em cada notebook que carrega parquets
  - Corrige tickers_finais.csv para usar DADOS_DIR
  - Normaliza todos os caminhos de parquet e csv para usar DADOS_DIR
"""
import json, re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# NOVA SETUP CELL (substitui a anterior em todos os notebooks)
# ─────────────────────────────────────────────────────────────────────────────

SETUP_CELL = """\
# ── CONFIGURAÇÃO DO AMBIENTE ─────────────────────────────────────────────────
# Este notebook roda no VS Code (Jupyter local) E no Google Colab.
# Execute esta célula primeiro — ela detecta o ambiente e configura os caminhos.
# Qualquer pessoa que clonar o repositório pode rodar sem modificações.

import os, sys, subprocess

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
    subprocess.run(['pip', 'install', '-q', 'yfinance', 'pyarrow',
                    'statsmodels', 'python-docx', 'anthropic'], check=False)

    # Clonar o repositório do curso (pula automaticamente se já existir)
    REPO_DIR = '/content/intensivao-quant-ai'
    if not os.path.exists(REPO_DIR):
        print("Clonando repositório do curso...")
        subprocess.run([
            'git', 'clone',
            'https://github.com/fmaldonadoo/intensivao-quant-ai.git',
            REPO_DIR
        ], check=False)
        print("Repositório clonado com sucesso.")

    # Pasta de dados no Google Drive — persiste entre sessões do Colab
    DADOS_DIR = '/content/drive/MyDrive/intensivao_quant/dados'
    os.makedirs(DADOS_DIR, exist_ok=True)
    print(f"Dados em: {DADOS_DIR}")

else:
    # ── VS Code / Jupyter local ───────────────────────────────────────────────
    print("Ambiente detectado: VS Code / Jupyter local")

    # Garante que pyarrow está instalado (necessário para ler/salvar parquet)
    try:
        import pyarrow
    except ImportError:
        print("Instalando pyarrow...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'pyarrow'],
                       check=False)

    # Localiza a raiz do repositório subindo a árvore de diretórios até o .git
    # Funciona independente de onde o usuário clonou o projeto
    _p = os.path.abspath(os.getcwd())
    _root = None
    while _p != os.path.dirname(_p):
        if os.path.exists(os.path.join(_p, '.git')):
            _root = _p
            break
        _p = os.path.dirname(_p)

    # Fallback: se não encontrar .git, usa a pasta pai do notebook
    if _root is None:
        _root = os.path.dirname(os.path.abspath('__file__'))
        print("  Aviso: repositório .git não encontrado. Usando pasta do notebook.")

    DADOS_DIR = os.path.join(_root, 'dados')
    os.makedirs(DADOS_DIR, exist_ok=True)
    print(f"Dados em: {DADOS_DIR}")
"""

# Marcador para detectar se a setup cell já está no novo formato
NOVO_SETUP_MARKER = "Qualquer pessoa que clonar o repositório pode rodar sem modificações."
SETUP_MARKER_ANTIGO = "IN_COLAB"  # detecta a setup cell antiga

# ─────────────────────────────────────────────────────────────────────────────
# CÉLULAS DE VERIFICAÇÃO DE DADOS por notebook
# Cada chave = substring do nome do arquivo; valor = (arquivos_necessários, aula_anterior)
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
    arquivos_str = '\n'.join(
        f"    os.path.join(DADOS_DIR, '{f}')," for f in arquivos
    )
    return f"""\
# ── VERIFICAÇÃO DE DEPENDÊNCIAS ──────────────────────────────────────────────
# Este notebook depende dos dados gerados pela aula anterior.
# Se algum arquivo estiver faltando, rode o notebook indicado primeiro.

_arquivos_necessarios = [
{arquivos_str}
]

_faltando = [f for f in _arquivos_necessarios if not os.path.exists(f)]
if _faltando:
    print("\\n⚠  ATENÇÃO: arquivos necessários não encontrados:")
    for f in _faltando:
        print(f"   Faltando: {{os.path.basename(f)}}")
    print(f"\\n   Execute primeiro o notebook: {aula_anterior}")
    print(f"   Os dados devem ficar em: {{DADOS_DIR}}")
else:
    print("✓  Todos os arquivos necessários encontrados.")
"""

# ─────────────────────────────────────────────────────────────────────────────
# Helpers de manipulação de notebook
# ─────────────────────────────────────────────────────────────────────────────

def src(cell):
    s = cell.get('source', [])
    return ''.join(s) if isinstance(s, list) else s

def make_cell(source):
    return {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': source
    }

def to_source_list(text):
    lines = text.splitlines(keepends=True)
    # Remove \n da última linha
    if lines and lines[-1].endswith('\n'):
        lines[-1] = lines[-1].rstrip('\n')
    return lines


def fix_paths(source: str) -> str:
    """
    Normaliza todos os caminhos relativos para usar DADOS_DIR.
    Trata parquet e csv.
    """
    # 1. Caminhos com ../../dados/ ou ../dados/
    source = re.sub(
        r"'(?:\.\.[\\/])+dados[\\/]([\w\-\.]+\.(parquet|csv))'",
        r"os.path.join(DADOS_DIR, '\1')",
        source
    )
    # 2. Caminhos só com nome do arquivo (sem prefixo de pasta)
    # Negative lookbehind para não duplicar
    source = re.sub(
        r"(?<!DADOS_DIR, )'([\w\-]+\.(parquet|csv))'",
        r"os.path.join(DADOS_DIR, '\1')",
        source
    )
    return source


def refactor_notebook(nb_path: str):
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)

    cells  = nb.get('cells', [])
    nome   = os.path.basename(nb_path)
    changed = False

    # ── 1. Substituir (ou inserir) setup cell ────────────────────────────────
    setup_idx = None
    for i, cell in enumerate(cells[:5]):
        s = src(cell)
        if SETUP_MARKER_ANTIGO in s or NOVO_SETUP_MARKER in s:
            setup_idx = i
            break

    new_setup = make_cell(to_source_list(SETUP_CELL))

    if setup_idx is not None:
        if NOVO_SETUP_MARKER not in src(cells[setup_idx]):
            cells[setup_idx] = new_setup
            print(f"  [setup atualizado]  {nome}")
            changed = True
        else:
            print(f"  [setup ok]          {nome}")
    else:
        # Insere após o primeiro cell markdown (título)
        insert_at = 1 if (cells and cells[0].get('cell_type') == 'markdown') else 0
        cells.insert(insert_at, new_setup)
        print(f"  [setup inserido]    {nome}")
        changed = True

    # ── 2. Inserir / atualizar célula de verificação de dependências ─────────
    chave = next((k for k in CHECKS if k in nb_path), None)
    if chave:
        arquivos, aula_ant = CHECKS[chave]
        check_source = make_check_cell(arquivos, aula_ant)
        CHECK_MARKER = "VERIFICAÇÃO DE DEPENDÊNCIAS"

        check_idx = None
        for i, cell in enumerate(cells):
            if CHECK_MARKER in src(cell):
                check_idx = i
                break

        new_check = make_cell(to_source_list(check_source))

        if check_idx is not None:
            if src(cells[check_idx]) != check_source:
                cells[check_idx] = new_check
                print(f"  [check atualizado]  {nome}")
                changed = True
        else:
            # Insere logo após a setup cell e o bloco de imports (posição ~3)
            import_idx = next(
                (i for i, c in enumerate(cells)
                 if 'import pandas' in src(c) or 'import numpy' in src(c)),
                None
            )
            pos = (import_idx + 1) if import_idx else 3
            cells.insert(pos, new_check)
            print(f"  [check inserido]    {nome}")
            changed = True

    # ── 3. Normalizar caminhos em células de código ──────────────────────────
    for cell in cells:
        if cell.get('cell_type') != 'code':
            continue
        original = src(cell)
        fixado   = fix_paths(original)
        if fixado != original:
            cell['source'] = to_source_list(fixado)
            changed = True

    # ── 4. Salvar se houve mudança ───────────────────────────────────────────
    if changed:
        nb['cells'] = cells
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)

    return changed


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Refatorando notebooks para portabilidade total...\n")
    notebooks = sorted(glob.glob(os.path.join(BASE, '*/aula-*.ipynb')))
    n_changed = 0
    for nb in notebooks:
        if refactor_notebook(nb):
            n_changed += 1
    print(f"\nConcluído! {len(notebooks)} notebooks processados, {n_changed} modificados.")
