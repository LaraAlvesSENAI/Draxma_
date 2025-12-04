from flask import render_template, request, redirect,Blueprint
import psycopg2

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="BancoDraxma",
        user="postgres",
        password="senai",
    )
    return banco

bp = Blueprint('contato_bp', __name__)

@bp.route("/contato",methods=["GET","POST"])
def tela_contato():
    if request.method == "POST":
        nome = request.form["nome_contato"]
        empresa = request.form['nome_empresa']
        email = request.form["email"]
        assunto = request.form["assunto"]
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute(
            "INSERT INTO contato (nome_contato, id_empresa, email, assunto) VALUES (%s, %s, %s, %s)",
            (nome, empresa, email, assunto)
        )
        banco.commit()
        banco.close()
        return redirect("/contato")
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_empresa, nome_empresa FROM cadastro_usuario ORDER BY nome_empresa")
    empresas = cursor.fetchall()
    banco.close()
    return render_template("contato.html", empresas=empresas)