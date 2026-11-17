"""Configurações centrais do projeto Brasileirão 2026."""

# --- API (json-server) ---
API_HOST = "localhost"
API_PORT = 3000
API_URL = f"http://{API_HOST}:{API_PORT}/jogadores"
API_TIMEOUT = 5  # segundos

# --- Dados ---
POSICOES = ["Atacante", "Meia", "Lateral", "Zagueiro", "Volante", "Goleiro"]

# --- Interface gráfica (front.py) ---
JANELA_TITULO = "Brasileirão 2026 - Jogadores"
JANELA_TAMANHO = "860x560"
