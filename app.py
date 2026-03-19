from flask import Flask, render_template, session, request, redirect, url_for, flash
from banco import conectar, criar_tabela
import os

app = Flask(__name__)
app.secret_key = "chave_secreta"

# Cria as tabelas ao iniciar
criar_tabela()


def criar_tabela_empresas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            num_acoes INTEGER NOT NULL,
            preco_acao REAL NOT NULL,
            lucro_liquido REAL NOT NULL,
            patrimonio REAL NOT NULL,
            ativos REAL NOT NULL,
            divida REAL NOT NULL,
            tipo_acao TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


criar_tabela_empresas()


# ------------------ ROTAS ------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("form-email")
        senha = request.form.get("form-senha")
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            # Se no banco.py usar row_factory, use usuario['nome'].
            # Se não, use usuario[1]
            try:
                session["usuario"] = usuario['nome']
            except:
                session["usuario"] = usuario[1]
            return redirect(url_for("perfil"))
        flash("Erro no login", "danger")
    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            return redirect(url_for("login"))
        except:
            flash("Email já cadastrado!", "danger")
        finally:
            conn.close()
    return render_template("cadastro.html")


@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        return redirect(url_for("login"))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas")
    empresas = cursor.fetchall()
    conn.close()
    return render_template("perfil.html", usuario=session["usuario"], empresas=empresas)


@app.route("/cadastro_de_acao") # Esta é a URL que você digita no navegador
def cadastro_de_acao():
    if "usuario" not in session:
        return redirect(url_for("login"))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas")
    empresas = cursor.fetchall()
    conn.close()
    return render_template("cadastro_acao.html", empresas=empresas)


@app.route("/cadastrar_empresa", methods=["POST"])
def cadastrar_empresa():
    try:
        # Pega os dados do formulário
        empresa = request.form.get("empresa")
        num_acoes = int(request.form.get("num_acoes") or 0)
        preco_acao = float(request.form.get("preco_acao") or 0)
        lucro_liquido = float(request.form.get("lucro_liquido") or 0)
        patrimonio = float(request.form.get("patrimonio") or 1)
        ativos = float(request.form.get("ativos") or 1)
        divida = float(request.form.get("divida") or 0)
        tipo_acao = request.form.get("tipo_acao")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO empresas (empresa, num_acoes, preco_acao, lucro_liquido, patrimonio, ativos, divida, tipo_acao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (empresa, num_acoes, preco_acao, lucro_liquido, patrimonio, ativos, divida, tipo_acao))
        conn.commit()
        conn.close()
        flash("Empresa cadastrada com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao cadastrar: {str(e)}", "danger")

    # CORREÇÃO: Redireciona para o nome da FUNÇÃO correta
    return redirect(url_for("cadastro_de_acao"))


@app.route("/excluir_empresa/<int:id>")
def excluir_empresa(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empresas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("cadastro_de_acao"))


@app.route("/editar_empresa/<int:id>")
def editar_empresa(id):
    # Apenas para o botão do HTML não dar erro
    return f"Editando empresa {id} - Funcionalidade em breve"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
