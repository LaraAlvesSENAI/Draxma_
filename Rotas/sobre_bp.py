from flask import render_template, request, redirect,Blueprint

bp = Blueprint('sobre_bp', __name__)

@bp.get('/sobre')
def tela_sobre():
    return render_template('sobre.html')