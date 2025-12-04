# from flask import render_template, request, redirect,Blueprint
# import psycopg2
#
# def ligar_banco():
#     banco = psycopg2.connect(
#         host="localhost",
#         dbname="BancoDraxma",
#         user="postgres",
#         password="senai",
#     )
#     return banco
#
# bp = Blueprint('conclusaoCadastroUsuario_bp', __name__)
#
#
# # @bp.get('/cadastro-usuario')
# # def tela_cadastroUsuario():
# #     return render_template('cadastroUsuario.html')
#
#
# @bp.route("/conclusao-cadastro-usuario", methods=["GET", "POST"])
# def tela_cadastroUsuario():
#     if request.method == "POST":
#         login = request.form['login']
#         senha = request.form['senha']
#
#         banco = ligar_banco()
#         cursor = banco.cursor()
#         cursor.execute(
#             """
#             INSERT INTO cadastro_usuario
#             (login, senha)
#             VALUES (%s, %s)
#             """,
#             (login, senha)
#         )
#         banco.commit()
#         banco.close()
#         return redirect('cadastroUsuario_bp.tela_cadastroUsuario')
#     return render_template("cadastroUsuario.html")