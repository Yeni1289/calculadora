from flask import Blueprint, render_template, request
from .pao_interpreter import ejecutar_pao

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        codigo = request.form["codigo"]
        result = ejecutar_pao(codigo)
    return render_template("index.html", result=result)
