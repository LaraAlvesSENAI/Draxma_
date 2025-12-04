from flask import Flask, render_template
import psycopg2
from Rotas import (index_bp, sobre_bp, contato_bp, login_bp, cadastroUsuario_bp,
                   # dashboards_bp,
                   despesas_bp, perfil_bp, cadastroDespesa_bp, sair_bp, api_dashboard)


def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="BancoDraxma",
        user="postgres",
        password="senai",
    )
    return banco

app = Flask(__name__)
app.secret_key="autenticacao"
app.register_blueprint(index_bp.bp)
app.register_blueprint(sobre_bp.bp)
app.register_blueprint(contato_bp.bp)
app.register_blueprint(login_bp.bp)
app.register_blueprint(cadastroUsuario_bp.bp)
# app.register_blueprint(dashboards_bp.bp)
app.register_blueprint(despesas_bp.bp)
app.register_blueprint(perfil_bp.bp)
app.register_blueprint(cadastroDespesa_bp.bp)
app.register_blueprint(sair_bp.bp)
app.register_blueprint(api_dashboard.bp)

@app.get('/')
def tela_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()