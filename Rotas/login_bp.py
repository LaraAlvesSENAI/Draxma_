from flask import render_template, request, redirect,Blueprint, url_for, session
import psycopg2

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="BancoDraxma",
        user="postgres",
        password="senai",
    )
    return banco



bp = Blueprint('login_bp', __name__)

@bp.route("/login", methods=["GET", "POST"])
def tela_login():
    return render_template("login.html")


@bp.route('/autenticar', methods =["POST"])
def autenticar():
    login = request.form['login']
    senha = request.form['senha']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cadastro_usuario WHERE login=%s AND senha=%s", (login, senha))
    usuario = cursor.fetchone()
    if usuario:
        session['Usuario_Logado'] = login
        return redirect('/dashboards')
    else:
        return redirect('/login')

# @bp.route('/deslogar')
# def deslogar():
#     session.clear()
#     return redirect('/login')