import tkinter as tk
from tkinter import ttk, messagebox

import requests

from config import API_URL as URL, API_TIMEOUT, POSICOES, JANELA_TITULO, JANELA_TAMANHO


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(JANELA_TITULO)
        self.geometry(JANELA_TAMANHO)
        self.minsize(760, 480)

        self.jogadores = []
        self.id_selecionado = None

        self._montar_busca()
        self._montar_tabela()
        self._montar_formulario()
        self.carregar()

    # ---------- interface ----------
    def _montar_busca(self):
        frame = ttk.Frame(self, padding=(10, 10, 10, 0))
        frame.pack(fill="x")

        ttk.Label(frame, text="Pesquisar (nome ou clube):").pack(side="left")
        self.var_busca = tk.StringVar()
        self.var_busca.trace_add("write", lambda *_: self.atualizar_tabela())
        ttk.Entry(frame, textvariable=self.var_busca, width=30).pack(side="left", padx=8)

        self.var_ordem = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frame,
            text="Ordenar por gols (maior → menor)",
            variable=self.var_ordem,
            command=self.atualizar_tabela,
        ).pack(side="left", padx=8)

        ttk.Button(frame, text="Recarregar", command=self.carregar).pack(side="right")

    def _montar_tabela(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        colunas = ("id", "nome", "clube", "posicao", "gols")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings", selectmode="browse")
        cabecalhos = {"id": "ID", "nome": "Nome", "clube": "Clube", "posicao": "Posição", "gols": "Gols"}
        larguras = {"id": 50, "nome": 240, "clube": 200, "posicao": 130, "gols": 70}
        for c in colunas:
            self.tree.heading(c, text=cabecalhos[c])
            self.tree.column(c, width=larguras[c], anchor="center" if c in ("id", "gols") else "w")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar)

    def _montar_formulario(self):
        frame = ttk.LabelFrame(self, text="Jogador", padding=10)
        frame.pack(fill="x", padx=10, pady=(0, 10))

        self.var_nome = tk.StringVar()
        self.var_clube = tk.StringVar()
        self.var_posicao = tk.StringVar()
        self.var_gols = tk.StringVar()

        ttk.Label(frame, text="Nome").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.var_nome, width=28).grid(row=1, column=0, padx=(0, 8))

        ttk.Label(frame, text="Clube").grid(row=0, column=1, sticky="w")
        ttk.Entry(frame, textvariable=self.var_clube, width=22).grid(row=1, column=1, padx=(0, 8))

        ttk.Label(frame, text="Posição").grid(row=0, column=2, sticky="w")
        ttk.Combobox(frame, textvariable=self.var_posicao, values=POSICOES, width=14).grid(
            row=1, column=2, padx=(0, 8)
        )

        ttk.Label(frame, text="Gols").grid(row=0, column=3, sticky="w")
        ttk.Entry(frame, textvariable=self.var_gols, width=8).grid(row=1, column=3, padx=(0, 8))

        botoes = ttk.Frame(frame)
        botoes.grid(row=2, column=0, columnspan=4, pady=(10, 0), sticky="w")
        ttk.Button(botoes, text="Adicionar", command=self.adicionar).pack(side="left", padx=(0, 6))
        ttk.Button(botoes, text="Atualizar", command=self.atualizar).pack(side="left", padx=6)
        ttk.Button(botoes, text="Excluir", command=self.excluir).pack(side="left", padx=6)
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left", padx=6)

    # ---------- API ----------
    def carregar(self):
        try:
            resp = requests.get(URL, timeout=API_TIMEOUT)
            resp.raise_for_status()
            self.jogadores = resp.json()
        except requests.exceptions.RequestException:
            messagebox.showerror(
                "Erro de conexão",
                "Não foi possível conectar à API.\nO json-server está rodando em localhost:3000?",
            )
            self.jogadores = []
        self.atualizar_tabela()

    def _ler_formulario(self):
        nome = self.var_nome.get().strip()
        clube = self.var_clube.get().strip()
        posicao = self.var_posicao.get().strip()
        if not nome or not clube or not posicao:
            messagebox.showwarning("Atenção", "Preencha nome, clube e posição.")
            return None
        try:
            gols = int(self.var_gols.get())
            if gols < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atenção", "Gols deve ser um número inteiro maior ou igual a zero.")
            return None
        return {"nome": nome, "clube": clube, "posicao": posicao, "gols": gols}

    def adicionar(self):
        dados = self._ler_formulario()
        if not dados:
            return
        try:
            resp = requests.post(URL, json=dados, timeout=API_TIMEOUT)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {e}")
            return
        self.limpar()
        self.carregar()

    def atualizar(self):
        if not self.id_selecionado:
            messagebox.showinfo("Atenção", "Selecione um jogador na tabela para atualizar.")
            return
        dados = self._ler_formulario()
        if not dados:
            return
        try:
            resp = requests.put(f"{URL}/{self.id_selecionado}", json=dados, timeout=API_TIMEOUT)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")
            return
        self.limpar()
        self.carregar()

    def excluir(self):
        if not self.id_selecionado:
            messagebox.showinfo("Atenção", "Selecione um jogador na tabela para excluir.")
            return
        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este jogador?"):
            return
        try:
            resp = requests.delete(f"{URL}/{self.id_selecionado}", timeout=API_TIMEOUT)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao excluir: {e}")
            return
        self.limpar()
        self.carregar()

    # ---------- tabela / seleção ----------
    def atualizar_tabela(self):
        termo = self.var_busca.get().strip().lower()
        lista = [
            j for j in self.jogadores
            if termo in j["nome"].lower() or termo in j["clube"].lower()
        ]
        if self.var_ordem.get():
            lista.sort(key=lambda j: j["gols"], reverse=True)

        self.tree.delete(*self.tree.get_children())
        for j in lista:
            self.tree.insert(
                "", "end", iid=str(j["id"]),
                values=(j["id"], j["nome"], j["clube"], j["posicao"], j["gols"]),
            )

    def ao_selecionar(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        valores = self.tree.item(sel[0], "values")
        self.id_selecionado = valores[0]
        self.var_nome.set(valores[1])
        self.var_clube.set(valores[2])
        self.var_posicao.set(valores[3])
        self.var_gols.set(valores[4])

    def limpar(self):
        self.id_selecionado = None
        for v in (self.var_nome, self.var_clube, self.var_posicao, self.var_gols):
            v.set("")
        self.tree.selection_remove(self.tree.selection())


if __name__ == "__main__":
    App().mainloop()
