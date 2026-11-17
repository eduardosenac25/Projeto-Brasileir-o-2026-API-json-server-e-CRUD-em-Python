"""Brasileirão 2026 - CRUD de jogadores (menu no terminal).

Requer a API rodando:  cd api && npm start
"""
import requests

from cadastro.listar import listar_artilheiros, listar_jogadores, pesquisar
from config import API_TIMEOUT, API_URL, POSICOES


# ---------- acesso à API ----------

def buscar_por_id(id_jogador):
    resp = requests.get(f"{API_URL}/{id_jogador}", timeout=API_TIMEOUT)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


# ---------- utilidades ----------

def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Este campo não pode ficar vazio.")


def ler_gols(mensagem="Gols: "):
    while True:
        try:
            gols = int(input(mensagem))
            if gols >= 0:
                return gols
        except ValueError:
            pass
        print("Digite um número inteiro maior ou igual a zero.")


# ---------- opções do menu ----------

def incluir_jogador():
    print("\n--- Incluir jogador ---")
    nome = ler_texto("Nome: ")
    clube = ler_texto("Clube: ")
    print(f"Posições sugeridas: {', '.join(POSICOES)}")
    posicao = ler_texto("Posição: ").capitalize()
    gols = ler_gols()
    resp = requests.post(
        API_URL,
        json={"nome": nome, "clube": clube, "posicao": posicao, "gols": gols},
        timeout=API_TIMEOUT,
    )
    resp.raise_for_status()
    print(f"\nJogador '{nome}' cadastrado com ID {resp.json()['id']}!")


def alterar_gols():
    print("\n--- Alterar nº de gols ---")
    id_jogador = ler_texto("ID do jogador: ")
    jogador = buscar_por_id(id_jogador)
    if not jogador:
        print("Jogador não encontrado.")
        return
    print(f"{jogador['nome']} ({jogador['clube']}) tem {jogador['gols']} gol(s).")
    novos_gols = ler_gols("Novo número de gols: ")
    resp = requests.patch(
        f"{API_URL}/{id_jogador}", json={"gols": novos_gols}, timeout=API_TIMEOUT
    )
    resp.raise_for_status()
    print("Gols atualizados!")


def excluir_jogador():
    print("\n--- Excluir jogador ---")
    id_jogador = ler_texto("ID do jogador: ")
    jogador = buscar_por_id(id_jogador)
    if not jogador:
        print("Jogador não encontrado.")
        return
    confirma = input(f"Excluir {jogador['nome']} ({jogador['clube']})? (s/n): ").strip().lower()
    if confirma != "s":
        print("Operação cancelada.")
        return
    resp = requests.delete(f"{API_URL}/{id_jogador}", timeout=API_TIMEOUT)
    resp.raise_for_status()
    print("Jogador excluído!")


# ---------- programa principal ----------
OPCOES = {
    "1": listar_jogadores,
    "2": incluir_jogador,
    "3": alterar_gols,
    "4": excluir_jogador,
    "5": pesquisar,
    "6": listar_artilheiros,
}


def main():
    while True:
        print("\n===== Brasileirão 2026 =====")
        print("1 - Listar jogadores")
        print("2 - Incluir jogador")
        print("3 - Alterar nº de gols")
        print("4 - Excluir jogador")
        print("5 - Pesquisar por nome ou clube")
        print("6 - Listar artilheiros")
        print("7 - Finalizar")
        opcao = input("Opção: ").strip()

        if opcao == "7":
            print("Programa finalizado.")
            break

        acao = OPCOES.get(opcao)
        if not acao:
            print("Opção inválida.")
            continue

        try:
            acao()
        except requests.exceptions.ConnectionError:
            print(f"\nNão foi possível conectar à API em {API_URL}.")
            print("O json-server está rodando? (cd api && npm start)")
        except requests.exceptions.RequestException as e:
            print(f"\nErro na requisição: {e}")


if __name__ == "__main__":
    main()
