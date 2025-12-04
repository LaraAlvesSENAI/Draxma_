from flask import render_template, request, redirect,Blueprint, url_for,session
import psycopg2

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="BancoDraxma",
        user="postgres",
        password="senai",
    )
    return banco

bp = Blueprint('cadastroDespesa_bp', __name__)

# -------------------------------------------------- ROTA DE CADASTRO --------------------------------------------------
@bp.route("/cadastro-despesa", methods=["GET", "POST"])
def tela_cadastroDespesa():
    if request.method == "POST":
        tipo_conta = request.form["tipo_conta"]
        valor_conta = request.form['valor']
        vencimento_conta = request.form['vencimento']
        situacao_conta = request.form['situacao']
        usuario = session['Usuario_Logado']
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute(
            "SELECT id_empresa FROM cadastro_usuario WHERE login=%s",
            (usuario,)
        )
        id_empresa = cursor.fetchone()[0]
        cursor.execute(
            """
            INSERT INTO cadastro_despesa
            (id_empresa, tipo_conta, valor_despesa, vencimento_despesa, situacao_despesa)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_empresa, tipo_conta, valor_conta, vencimento_conta, situacao_conta)
        )
        banco.commit()
        banco.close()
        return redirect(url_for('despesas_bp.tela_despesas'))
    return render_template("cadastroDespesa.html")


# --------------------------------------------------- ROTA DE EDIÇÃO ---------------------------------------------------
@bp.route("/editar-despesa/<int:id_despesa>", methods=["GET", "POST"])
def tela_editarDespesa(id_despesa):
    banco = ligar_banco()
    cursor = banco.cursor()
    if request.method == "POST":
        tipo_conta = request.form["tipo_conta"]
        valor_conta = request.form['valor']
        vencimento_conta = request.form['vencimento']
        situacao_conta = request.form['situacao']
        cursor.execute("""
            UPDATE cadastro_despesa 
            SET tipo_conta=%s, valor_despesa=%s, vencimento_despesa=%s, situacao_despesa=%s
            WHERE id_despesa=%s
        """, (tipo_conta, valor_conta, vencimento_conta, situacao_conta, id_despesa))
        banco.commit()
        banco.close()
        return redirect(url_for('despesas_bp.tela_despesas'))
    cursor.execute("SELECT * FROM cadastro_despesa WHERE id_despesa=%s", (id_despesa,))
    d = cursor.fetchone()
    banco.close()
    return render_template("editardespesa.html", d=d)


# -------------------------------------------------- ROTA DE EXCLUSÃO --------------------------------------------------
@bp.route("/excluir-despesa/<int:id_despesa>", methods=["GET","DELETE","POST"])
def telaExcluirDespesa(id_despesa):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM cadastro_despesa WHERE id_despesa = %s", (id_despesa,))
    banco.commit()
    banco.close()
    return redirect("/despesas")