# Brasileirão 2026 - API + CRUD em Python

## Estrutura
- `api/` -> API com json-server (db.json com o artilheiro de cada time da Série A)
- `app/main.py` -> menu no terminal (while True)
- `app/front.py` -> interface gráfica (Tkinter)
- `app/config.py` -> configurações (URL da API, posições, janela)

## Como rodar

### 1) API (terminal 1)
```
cd api
npm install
npm start
```
Fica em http://localhost:3000/jogadores

### 2) Aplicação (terminal 2)
```
cd app
pip install -r requirements.txt
python main.py      # menu no terminal
python front.py     # interface gráfica
```
