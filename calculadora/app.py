from flask import Flask, render_template_string, request
from antlr4 import *
from CalculadoraLexer import CalculadoraLexer
from CalculadoraParser import CalculadoraParser
from CalculadoraListener import CalculadoraListener

# ============================================================
#   Listener personalizado para interpretar el lenguaje
# ============================================================
class EjecutarListener(CalculadoraListener):
    def __init__(self):
        self.variables = {}
        self.salida = []

    # --- Asignación ---
    def exitAsignacion(self, ctx):
        var = ctx.ID().getText()
        valor = self.eval_expresion(ctx.expresion())
        self.variables[var] = valor
        self.salida.append(f"Asigna {valor} a la variable {var}. Estado: {self.variables}")

    # --- Condicional ---
    def exitCondicional(self, ctx):
        cond = self.eval_condicion(ctx.condicion())
        self.salida.append(f"Evalúa condición ({ctx.condicion().getText()}): {cond}")
        if cond:
            for inst in ctx.instruccion():
                if inst.asignacion():
                    self.exitAsignacion(inst.asignacion())

    # --- Evaluación de expresiones ---
    def eval_expresion(self, ctx):
        if ctx.termino() and len(ctx.termino()) == 1:
            return self.eval_termino(ctx.termino(0))
        total = self.eval_termino(ctx.termino(0))
        for i, op in enumerate(ctx.getChildren()):
            if op.getText() == '+':
                total += self.eval_termino(ctx.termino(i + 1))
            elif op.getText() == '-':
                total -= self.eval_termino(ctx.termino(i + 1))
        return total

    def eval_termino(self, ctx):
        if ctx.factor() and len(ctx.factor()) == 1:
            return self.eval_factor(ctx.factor(0))
        total = self.eval_factor(ctx.factor(0))
        for i, op in enumerate(ctx.getChildren()):
            if op.getText() == '*':
                total *= self.eval_factor(ctx.factor(i + 1))
            elif op.getText() == '/':
                val = self.eval_factor(ctx.factor(i + 1))
                total /= val if val != 0 else 1
        return total

    def eval_factor(self, ctx):
        if ctx.NUM():
            return int(ctx.NUM().getText())
        elif ctx.ID():
            return self.variables.get(ctx.ID().getText(), 0)
        elif ctx.expresion():
            return self.eval_expresion(ctx.expresion())

    def eval_condicion(self, ctx):
        izq = self.eval_expresion(ctx.expresion(0))
        der = self.eval_expresion(ctx.expresion(1))
        op = ctx.getChild(1).getText()
        if op == '>': return izq > der
        if op == '<': return izq < der
        if op == '==': return izq == der
        if op == '!=': return izq != der
        if op == '>=': return izq >= der
        if op == '<=': return izq <= der
        return False


# ============================================================
#   Función de ejecución del código
# ============================================================
def ejecutar_codigo(codigo):
    input_stream = InputStream(codigo)
    lexer = CalculadoraLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = CalculadoraParser(tokens)
    tree = parser.programa()

    listener = EjecutarListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.salida, listener.variables, tree.toStringTree(recog=parser)


# ============================================================
#   Aplicación Flask
# ============================================================
app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Lenguaje - Pao / Calculadora</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f5f9ff; margin: 30px; color:#222; }
    h1 { color: #0052cc; text-align:center; }
    textarea { width:100%; height:150px; padding:10px; font-family:monospace; border-radius:6px; border:1px solid #ccc; }
    button { margin-top:10px; padding:10px 20px; background:#0052cc; color:#fff; border:none; border-radius:6px; cursor:pointer; }
    button:hover { background:#003d99; }
    .panel { background:#fff; padding:15px; border-radius:10px; box-shadow:0 3px 10px rgba(0,0,0,0.1); margin-top:20px; }
    pre { background:#f2f6ff; padding:10px; border-radius:6px; overflow-x:auto; }
    ul { margin-left:20px; }
  </style>
</head>
<body>
  <h1>💡 Lenguaje: Operaciones y Condicionales</h1>
  <form method="POST">
    <textarea name="codigo" placeholder="Escribe tu programa aquí...">{{ request.form.get('codigo','') }}</textarea>
    <button type="submit">Ejecutar</button>
  </form>

  {% if salida %}
  <div class="panel">
    <h2>🧩 Ejecución paso a paso</h2>
    <ul>
      {% for paso in salida %}
        <li>{{ paso }}</li>
      {% endfor %}
    </ul>

    <h2>📦 Variables finales</h2>
    <pre>{{ variables }}</pre>

    <h2>🌳 Árbol de análisis</h2>
    <pre>{{ arbol }}</pre>
  </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    salida = variables = arbol = None
    if request.method == "POST":
        codigo = request.form["codigo"]
        try:
            salida, variables, arbol = ejecutar_codigo(codigo)
        except Exception as e:
            salida = [f"⚠️ Error al ejecutar: {e}"]
    return render_template_string(html, salida=salida, variables=variables, arbol=arbol)

if __name__ == "__main__":
    app.run(debug=True)
