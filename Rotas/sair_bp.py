from flask import render_template, request, redirect,Blueprint,session,url_for
import psycopg2


def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="BancoDraxma",
        user="postgres",
        password="senai",
    )
    return banco
bp = Blueprint('sair_bp', __name__)

@bp.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("tela_index"))