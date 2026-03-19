from flask import Flask, render_template, session, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "chave_secreta"


# ------------------ FUNÇÕES DE BANCO ------------------
def conectar():
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row  # Para poder acessar colunas por nome
    return conn


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Tabela de Empresas (com todas as colunas do formulário)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            empresa TEXT NOT NULL,
            setor TEXT NOT NULL,
            num_acoes INTEGER NOT NULL,
            preco_acao REAL NOT NULL,
            lucro_liquido REAL NOT NULL,
            patrimonio REAL NOT NULL,
            ativos REAL NOT NULL,
            divida REAL NOT NULL,
            lote INTEGER NOT NULL,
            tipo_acao TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Cria tabelas ao iniciar
criar_tabela()


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
            session["usuario"] = usuario['nome']
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
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email já cadastrado!", "danger")
        except Exception as e:
            flash(f"Erro ao cadastrar: {e}", "danger")
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


@app.route("/cadastro_de_acao")
def cadastro_de_acao():
    if "usuario" not in session:
        return redirect(url_for("login"))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas")
    empresas = cursor.fetchall()
    conn.close()
    return render_template("cadastro_acao.html", empresas=empresas)


@app.route("/cadastrar_empresa", methods=["GET", "POST"])
def cadastrar_empresa():
    if request.method == "POST":
        try:
            ticker = request.form.get("ticker")
            empresa = request.form.get("empresa")
            setor = request.form.get("setor")
            num_acoes = int(request.form.get("num_acoes") or 0)
            preco_acao = float(request.form.get("preco_acao") or 0)
            lucro_liquido = float(request.form.get("lucro_liquido") or 0)
            patrimonio = float(request.form.get("patrimonio") or 0)
            ativos = float(request.form.get("ativos") or 0)
            divida = float(request.form.get("divida") or 0)
            lote = int(request.form.get("lote") or 0)
            tipo_acao = request.form.get("tipo_acao")

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO empresas (ticker, empresa, setor, num_acoes, preco_acao, lucro_liquido, patrimonio, ativos, divida, lote, tipo_acao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ticker, empresa, setor, num_acoes, preco_acao, lucro_liquido, patrimonio, ativos, divida, lote,
                  tipo_acao))
            conn.commit()
            conn.close()
            flash("Empresa cadastrada com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao cadastrar: {e}", "danger")
        return redirect(url_for("cadastro_de_acao"))
    else:
        flash("Use o formulário para cadastrar empresas.", "warning")
        return redirect(url_for("cadastro_de_acao"))


@app.route("/excluir_empresa/<int:id>")
def excluir_empresa(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empresas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Empresa excluída com sucesso!", "success")
    return redirect(url_for("cadastro_de_acao"))


@app.route("/editar_empresa/<int:id>")
def editar_empresa(id):
    # Funcionalidade futura
    return f"Editando empresa {id} - Funcionalidade em breve"


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("login"))




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)