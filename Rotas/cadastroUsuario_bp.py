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

bp = Blueprint('cadastroUsuario_bp', __name__)


# @bp.get('/cadastro-usuario')
# def tela_cadastroUsuario():
#     return render_template('cadastroUsuario.html')


@bp.route("/cadastro-usuario", methods=["GET", "POST"])
def tela_cadastroUsuario():
    if request.method == "POST":
        nomeempresa = request.form["nome_empresa"]
        nome_representante = request.form['nome_representante']
        porte_empresa = request.form["porte_empresa"]
        email_recuperacao = request.form["email_recuperacao"]
        tel_recuperacao = request.form["tel_recuperacao"]
        cidade = request.form["cidade"]
        estado = request.form["estado"]
        rua = request.form["rua"]
        bairro = request.form["bairro"]
        cep = request.form["cep"]
        numero_predio = request.form["numpredio"]
        login = request.form['login']
        senha = request.form['senha']

        erros = validar_usuario(email_recuperacao, login, tel_recuperacao, senha)

        if erros:
            return render_template(
                "cadastroUsuario.html",
                mensagens_erro=erros
            )

        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute(
            """
            INSERT INTO cadastro_usuario
            (nome_empresa, nome_representante, email_recuperacao, telefone_recuperacao,
             porte_empresa, nome_estado, nome_cidade, nome_rua, nome_bairro, numero_cep, numero_predio,login,senha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nomeempresa, nome_representante, email_recuperacao, tel_recuperacao,
             porte_empresa, estado, cidade, rua, bairro, cep, numero_predio, login, senha)
        )
        banco.commit()
        banco.close()

        session['Usuario_Logado'] = login
        # return redirect(url_for('dashboards_bp.tela_dashboards'))
        return redirect(url_for('api_dashboard.listar_relatorios'))
    return render_template("cadastroUsuario.html")


# def valor_existe(campo, valor):
#     banco = ligar_banco()
#     cursor = banco.cursor()
#
#     query = f"SELECT 1 FROM cadastro_usuario WHERE {campo} = %s LIMIT 1"
#     cursor.execute(query, (valor,))
#
#     existe = cursor.fetchone() is not None
#
#     banco.close()
#     return existe

def validar_usuario(email, login, telefone, senha):
    erros = []

# ----------------------------------------- VERIFICA A QUANTIDADE DE CARACTERES -----------------------------------------

    if len(login) > 10:
        erros.append("O login deve conter no máximo 10 caracteres.")

    if len(senha) > 10:
        erros.append("A senha deve conter no máximo 10 caracteres.")

# -------------------------------------------- VERIFICA A REPETIÇÃO DE DADOS --------------------------------------------

    if valor_existe("email_recuperacao", email):
        erros.append("E-mail já cadastrado!")

    if valor_existe("login", login):
        erros.append("Login já cadastrado!")

    if valor_existe("telefone_recuperacao", telefone):
        erros.append("Telefone já cadastrado!")

    return erros



def valor_existe(campo, valor):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        f"SELECT 1 FROM cadastro_usuario WHERE {campo} = %s LIMIT 1",
        (valor,)
    )

    existe = cursor.fetchone() is not None

    banco.close()
    return existe







# @bp.route("/cadastro-usuario", methods=["GET", "POST"])
# def tela_cadastroUsuario():
#     if request.method == "POST":
#         nomeempresa = request.form["nome_empresa"]
#         nome_representante = request.form['nome_representante']
#         porte_empresa = request.form["porte_empresa"]
#         email_recuperacao = request.form["email_recuperacao"]
#         tel_recuperacao = request.form["tel_recuperacao"]
#         cidade = request.form["cidade"]
#         estado = request.form["estado"]
#         rua = request.form["rua"]
#         bairro = request.form["bairro"]
#         cep = request.form["cep"]
#         numero_predio = request.form["numpredio"]
#         login = request.form['login']
#         senha = request.form['senha']
#         banco = ligar_banco()
#         cursor = banco.cursor()
#         cursor.execute(
#             """
#             INSERT INTO cadastro_usuario
#             (nome_empresa, nome_representante, email_recuperacao, telefone_recuperacao,
#              porte_empresa, nome_estado, nome_cidade, nome_rua, nome_bairro, numero_cep, numero_predio,login,senha)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """,
#             (nomeempresa, nome_representante, email_recuperacao, tel_recuperacao,
#              porte_empresa, estado, cidade, rua, bairro, cep, numero_predio, login, senha)
#         )
#         banco.commit()
#         banco.close()
#
#         banco = ligar_banco()
#         cursor = banco.cursor()
#         usuario = session['Usuario_Logado']
#         cursor.execute("SELECT * FROM cadastro_usuario WHERE login=%s", (usuario,))
#         perfil = cursor.fetchone()
#         return redirect(url_for('dashboards_bp.tela_dashboards',perfil=perfil))
#     return render_template("cadastroUsuario.html")

    # @bp.get('/perfil')
    # def tela_perfil():
    #     usuario = session['Usuario_Logado']
    #     banco = ligar_banco()
    #     cursor = banco.cursor()
    #     cursor.execute("SELECT * FROM cadastro_usuario WHERE login=%s", (usuario,))
    #     perfil = cursor.fetchone()
    #     banco.close()
    #
    #     return render_template('perfil.html', perfil=perfil)

    #     return redirect('cadastroUsuario_bp.tela_cadastroUsuario')
    # return render_template("cadastroUsuario.html")


# @bp.route("/verificar-email", methods=["POST"])
# def verificar_email():
#     # Recebe o email enviado pelo front-end
#     data = request.get_json()
#     email_recuperacao = data.get("email_recuperacao")
#
#     # Conecta ao banco
#     banco = ligar_banco()
#     cursor = banco.cursor()
#
#     # Verifica se já existe
#     cursor.execute(
#         "SELECT 1 FROM cadastro_usuario WHERE email_recuperacao = %s",
#         (email_recuperacao,)
#     )
#     existe = cursor.fetchone() is not None
#
#     banco.close()
#
#     # Retorna JSON indicando se existe ou não
#     return {"existe": existe}