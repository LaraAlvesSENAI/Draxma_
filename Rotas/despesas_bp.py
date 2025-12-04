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

bp = Blueprint('despesas_bp', __name__)

# @bp.get('/despesas')
# def tela_despesas():
#     return render_template('despesas.html')

# @bp.get('/despesas')
# def tela_despesas():
#     banco = ligar_banco()
#     cursor = banco.cursor()
#     cursor.execute("SELECT * FROM cadastro_despesa")
#     despesas = cursor.fetchall()
#     banco.close()
#     return render_template('despesas.html', despesas=despesas)

@bp.get('/despesas')
def tela_despesas():
    usuario = session['Usuario_Logado']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_empresa FROM cadastro_usuario WHERE login=%s", (usuario,))
    id_empresa = cursor.fetchone()[0]
    cursor.execute("""
        SELECT * FROM cadastro_despesa
        WHERE id_empresa = %s
    """, (id_empresa,))
    despesas = cursor.fetchall()
    banco.close()
    return render_template('despesas.html', despesas=despesas)

# @bp.get('/despesas')
# def tela_despesas():
#     usuario = session['Usuario_Logado']
#     banco = ligar_banco()
#     cursor = banco.cursor()
#     cursor.execute("SELECT * FROM cadastro_usuario WHERE login=%s",(usuario,))
#     despesas = cursor.fetchone()
#     banco.close()
#
#     return render_template('despesas.html', despesas=despesas)


# @bp.route("/cadastro-despesa", methods=["GET", "POST"])
# def tela_cadastroDespesa():
#     if request.method == "POST":
#         tipoConta = request.form["tipo_conta"]
#         valorConta = request.form['valor']
#         dataConta = request.form["vencimento"]
#         situacaoConta = request.form["situacao"]
#
#         banco = ligar_banco()
#         cursor = banco.cursor()
#         cursor.execute(
#             """
#             INSERT INTO cadastro_despesa
#             (tipo_conta, valor_despesa, vencimento_despesa, situacao_despesa)
#             VALUES (%s, %s, %s, %s)
#             """,
#             (tipoConta, valorConta, dataConta, situacaoConta)
#         )
#         banco.commit()
#         banco.close()
#         return redirect(url_for('despesas_bp.tela_despesas'))
#     return render_template("cadastroDespesa.html")