"""Funções de listagem de jogadores (consomem a API do json-server)."""
import requests

from config import API_TIMEOUT, API_URL


def buscar_todos():
    """Retorna a lista de todos os jogadores cadastrados na API."""
    resp = requests.get(API_URL, timeout=API_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def mostrar(jogadores, ranking=False):
    """Imprime os jogadores em formato de tabela (com posição no ranking, se pedido)."""
    if not jogadores:
        print("\nNenhum jogador encontrado.")
        return
    prefixo = f"{'#':<4}" if ranking else ""
    print(f"\n{prefixo}{'ID':<5}{'Nome':<22}{'Clube':<22}{'Posição':<12}{'Gols':>5}")
    print("-" * (70 if ranking else 66))
    for i, j in enumerate(jogadores, start=1):
        pos = f"{i}º".ljust(4) if ranking else ""
        print(f"{pos}{j['id']:<5}{j['nome']:<22}{j['clube']:<22}{j['posicao']:<12}{j['gols']:>5}")


def listar_jogadores():
    """Lista todos os jogadores."""
    mostrar(buscar_todos())


def listar_artilheiros():
    """Lista os jogadores ordenados por gols (maior → menor)."""
    jogadores = sorted(buscar_todos(), key=lambda j: j["gols"], reverse=True)
    mostrar(jogadores, ranking=True)


def pesquisar_jogadores(termo):
    """Retorna os jogadores cujo nome ou clube contém o termo (sem diferenciar maiúsculas)."""
    termo = termo.strip().lower()
    return [
        j for j in buscar_todos()
        if termo in j["nome"].lower() or termo in j["clube"].lower()
    ]


def pesquisar():
    """Pede um termo ao usuário e lista os jogadores encontrados."""
    print("\n--- Pesquisar ---")
    termo = ""
    while not termo.strip():
        termo = input("Nome ou clube: ")
    mostrar(pesquisar_jogadores(termo))
