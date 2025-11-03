from django.shortcuts import render
from .interpreter.CalculadoraLexer import CalculadoraLexer
from .interpreter.CalculadoraParser import CalculadoraParser
from .pao_listener import PAOListener
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

def index(request):
    resultado_final = None
    arbol = []
    codigo = ""

    if request.method == "POST":
        codigo = request.POST.get("codigo", "")
        try:
            # Crear flujo de entrada
            input_stream = InputStream(codigo)
            lexer = CalculadoraLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = CalculadoraParser(stream)
            tree = parser.programa()  # Regla inicial de tu gramática

            # Listener
            listener = PAOListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)

            # Variables y pasos
            resultado_final = listener.variables.copy()
            arbol = listener.arbol

        except Exception as e:
            resultado_final = f"Error al ejecutar: {str(e)}"

    return render(request, "lenguaje_app/index.html", {
        "resultado_final": resultado_final,
        "arbol": arbol,
        "codigo": codigo
    })
