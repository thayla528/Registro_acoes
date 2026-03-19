from flask import Flask, render_template, session, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "chave_secreta"

# ------------------ FUNÇÕES DE BANCO ------------------
def conectar():
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
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

    # Tabela de Empresas (corrigida: campos numéricos permitem NULL)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            empresa TEXT NOT NULL,
            setor TEXT NOT NULL,
            num_acoes INTEGER,
            preco_acao REAL,
            lucro_liquido REAL,
            patrimonio REAL,
            ativos REAL,
            divida REAL,
            lote INTEGER,
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
    return render_template("perfil.html", usuario=session["usuario"], empresas=empresas, os=os)


@app.route("/upload_foto", methods=["POST"])
def upload_foto():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if "foto" not in request.files:
        flash("Nenhum arquivo enviado!", "danger")
        return redirect(url_for("perfil"))

    foto = request.files["foto"]
    if foto.filename == "":
        flash("Nenhum arquivo selecionado!", "warning")
        return redirect(url_for("perfil"))

    filename = session["usuario"] + ".png"
    caminho = os.path.join("static/perfil", filename)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    foto.save(caminho)
    flash("Foto atualizada com sucesso!", "success")
    return redirect(url_for("perfil"))


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


@app.route("/cadastrar_empresa", methods=["POST"])
def cadastrar_empresa():
    try:
        # Captura todos os campos do formulário
        ticker = request.form.get("ticker").upper()
        empresa = request.form.get("empresa")
        setor = request.form.get("setor")
        num_acoes = int(request.form.get("num_acoes") or 0)
        preco_acao = float(request.form.get("preco_acao") or 0)
        lucro_liquido = float(request.form.get("lucro_liquido") or 0)
        patrimonio = float(request.form.get("patrimonio") or 0)
        ativos = float(request.form.get("ativos") or 0)
        divida = float(request.form.get("divida") or 0)
        lote = int(request.form.get("lote") or 100)
        tipo_acao = request.form.get("tipo_acao").upper() or "ON"

        # Insere no banco
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO empresas (ticker, empresa, setor, num_acoes, preco_acao, lucro_liquido, patrimonio, ativos, divida, lote, tipo_acao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticker, empresa, setor, num_acoes, preco_acao, lucro_liquido, patrimonio, ativos, divida, lote, tipo_acao))

        conn.commit()
        conn.close()

        flash("Empresa cadastrada com sucesso!", "success")
    except Exception as e:
        print(f"ERRO NO CONSOLE: {e}")
        flash(f"Erro ao cadastrar: {e}", "danger")

    return redirect(url_for("perfil"))


@app.route("/editar_empresa/<int:id>", methods=["GET", "POST"])
def editar_empresa(id):
    if "usuario" not in session:
        return redirect(url_for("login"))
    conn = conectar()
    cursor = conn.cursor()
    if request.method == "POST":
        cursor.execute("UPDATE empresas SET ticker=?, empresa=?, setor=?, preco_acao=?, lucro_liquido=? WHERE id=?",
                       (request.form.get("ticker"), request.form.get("empresa"), request.form.get("setor"),
                        float(request.form.get("preco_acao")), float(request.form.get("lucro_liquido")), id))
        conn.commit()
        conn.close()
        return redirect(url_for("perfil"))
    cursor.execute("SELECT * FROM empresas WHERE id = ?", (id,))
    empresa = cursor.fetchone()
    conn.close()
    return render_template("editar_acao.html", empresa=empresa)


@app.route("/excluir_empresa/<int:id>")
def excluir_empresa(id):
    if "usuario" not in session:
        return redirect(url_for("login"))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empresas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Empresa excluída com sucesso!", "success")
    return redirect(url_for("perfil"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)