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
bp = Blueprint('perfil_bp', __name__)

# @bp.get('/perfil')
# def tela_perfil():
#     # login = request.form['login']
#     # senha = request.form['senha']
#     banco = ligar_banco()
#     cursor = banco.cursor()
#     # cursor.execute("SELECT * FROM cadastro_usuario WHERE login=%s AND senha=%s", (login, senha))
#     perfil = cursor.fetchone()
#     banco.close()
#     return render_template('perfil.html', perfil=perfil)

@bp.get('/perfil')
def tela_perfil():
    usuario = session['Usuario_Logado']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cadastro_usuario WHERE login=%s",(usuario,))
    perfil = cursor.fetchone()
    banco.close()
    return render_template('perfil.html', perfil=perfil)



@bp.route("/editar-perfil/<int:id_empresa>", methods=["GET", "POST"])
def tela_editarPerfil(id_empresa):
    banco = ligar_banco()
    cursor = banco.cursor()
    if request.method == "POST":
        nomeempresa = request.form["nome_empresa"]
        nome_representante = request.form['nome_representante']
        porte_empresa = request.form["porte_empresa"]
        tel_recuperacao = request.form["tel_recuperacao"]
        email_recuperacao = request.form["email_recuperacao"]
        cidade = request.form["cidade"]
        estado = request.form["estado"]
        rua = request.form["rua"]
        bairro = request.form["bairro"]
        cep = request.form["cep"]
        numero_predio = request.form["numpredio"]
        senha = request.form['senha']
        cursor.execute("""
            UPDATE cadastro_usuario 
            SET nome_empresa=%s, nome_representante=%s, porte_empresa=%s, telefone_recuperacao=%s, email_recuperacao=%s,
            nome_cidade=%s, nome_estado=%s, nome_rua=%s, nome_bairro=%s, numero_cep=%s,
            numero_predio=%s, senha=%s
            WHERE id_empresa=%s
        """, (nomeempresa, nome_representante, porte_empresa, tel_recuperacao, email_recuperacao, cidade, estado,
              rua, bairro, cep, numero_predio, senha, id_empresa))
        banco.commit()
        banco.close()
        return redirect(url_for('perfil_bp.tela_perfil'))
    cursor.execute("SELECT * FROM cadastro_usuario WHERE id_empresa=%s", (id_empresa,))
    e = cursor.fetchone()
    banco.close()
    return render_template("editarperfil.html", e=e)
