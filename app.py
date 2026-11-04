import secrets
import sqlite3

from flask import Flask, request

app = Flask(__name__)

FLAG = "FLAG{injecao_sql_abriu_a_porta}"
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
    conexao.execute("CREATE TABLE usuarios (usuario TEXT, senha TEXT)")
    sorteada = secrets.token_urlsafe(16)
    conexao.execute("INSERT INTO usuarios VALUES (?, ?)", ("admin", sorteada))
    conexao.commit()
    conexao.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")
        consulta = (
            f"SELECT * FROM usuarios WHERE usuario = '{usuario}' "
            f"AND senha = '{senha}'"
        )
        conexao = sqlite3.connect(BANCO)
        resultado = conexao.execute(consulta).fetchone()
        conexao.close()
        if resultado:
            return f"<h1>Bem-vindo, {resultado[0]}!</h1><p>{FLAG}</p>"
        return FORMULARIO + "<p>Usuario ou senha incorretos.</p>"
    return FORMULARIO


if __name__ == "__main__":
    iniciar_banco()
    app.run()