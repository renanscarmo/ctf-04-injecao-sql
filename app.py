import os
import sqlite3

from flask import Flask, request
from werkzeug.security import check_password_hash

app = Flask(__name__)

FLAG = "FLAG{injecao_sql_corrigida}"
BANCO = "loja.db"

FORMULARIO = """
<h1>Area Restrita</h1>
<form method="post">
  <input name="usuario" placeholder="usuario">
  <input name="senha" type="password" placeholder="senha">
  <button type="submit">Entrar</button>
</form>
"""


def iniciar_banco():
    conexao = sqlite3.connect(BANCO)
    conexao.execute("DROP TABLE IF EXISTS usuarios")
    conexao.execute("CREATE TABLE usuarios (usuario TEXT, senha_hash TEXT)")
    conexao.execute(
        "INSERT INTO usuarios VALUES (?, ?)",
        ("admin", os.environ.get("ADMIN_SENHA_HASH", "")),
    )
    conexao.commit()
    conexao.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")
        conexao = sqlite3.connect(BANCO)
        linha = conexao.execute(
            "SELECT senha_hash FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()
        conexao.close()
        if linha and check_password_hash(linha[0], senha):
            return f"<h1>Bem-vindo!</h1><p>{FLAG}</p>"
        return FORMULARIO + "<p>Usuario ou senha incorretos.</p>"
    return FORMULARIO


if __name__ == "__main__":
    iniciar_banco()
    app.run()