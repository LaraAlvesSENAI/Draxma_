from flask import Blueprint, send_file, session, current_app, render_template
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import psycopg2
import os
from datetime import datetime
# from psycopg2 import sql

bp = Blueprint('api_dashboard', __name__)


def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="BancoDraxma",
        user="postgres",
        password="senai",
    )
    return banco

@bp.route("/gerar-pdf")
def gerar_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = []

# ------------------------------------------------------- TÍTULO -------------------------------------------------------

    content.append(Paragraph("Relatório Financeiro", styles["Title"]))
    content.append(Spacer(1, 20))

# ---------------------------------------------- BUSCA DOS DADOS DO CAMPO ----------------------------------------------

    conn = ligar_banco()
    cur = conn.cursor()
    usuario = session['Usuario_Logado']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        "SELECT id_empresa FROM cadastro_usuario WHERE login=%s",
        (usuario,)
    )
    id_empresa = cursor.fetchone()[0]
    cur.execute("""
        SELECT tipo_conta, valor_despesa, vencimento_despesa, situacao_despesa
        FROM cadastro_despesa
        WHERE id_empresa = %s
        ORDER BY vencimento_despesa ASC;
    """, (id_empresa,))

    registros = cur.fetchall()
    conn.close()

# -------------------------------------------------- TABELA DOS CAMPOS --------------------------------------------------

    tabela = [["Conta", "Vencimento", "Valor", "Situação"]]

    for nome, valor, venc, sit in registros:
        tabela.append([nome, str(venc), f"R$ {valor:.2f}", sit])

    table = Table(tabela, colWidths=[140, 90, 80, 70])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.grey),
        ("BOX", (0,0), (-1,-1), 0.6, colors.black),
    ]))

    content.append(table)

    doc.build(content)

    buffer.seek(0)
    # nome_pdf = f"relatorio-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
    nome_pdf = f"relatorio-{id_empresa}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"

    caminho_pasta = os.path.join(current_app.root_path, "relatorios")

    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

    caminho_final = os.path.join(caminho_pasta, nome_pdf)

    with open(caminho_final, "wb") as f:
        f.write(buffer.getvalue())


    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=nome_pdf)
    # return send_file(buffer, as_attachment=True, download_name="relatorio.pdf")


@bp.route("/dashboards")
def listar_relatorios():
    pasta = os.path.join(current_app.root_path, "relatorios")


    if not os.path.exists(pasta):
        os.makedirs(pasta)

    usuario = session['Usuario_Logado']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        "SELECT id_empresa FROM cadastro_usuario WHERE login=%s",
        (usuario,)
    )
    id_empresa = cursor.fetchone()[0]
    prefixo = f"relatorio-{id_empresa}-"
    # arquivos = [f for f in os.listdir(pasta) if f.endswith(".pdf")]
    # arquivos.sort(reverse=True)

    arquivos = [
        f for f in os.listdir(pasta)
        if f.startswith(prefixo) and f.endswith(".pdf")
    ]

    arquivos.sort(reverse=True)

    return render_template("dashboards.html", relatorios=arquivos)


@bp.route("/baixar-relatorio/<nome>")
def baixar_relatorio(nome):
    pasta = os.path.join(current_app.root_path, "relatorios")
    caminho = os.path.join(pasta, nome)

    if not os.path.exists(caminho):
        return "Arquivo não encontrado", 404

    return send_file(caminho, as_attachment=True)