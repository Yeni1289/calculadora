from antlr4 import *
from .CalculadoraLexer import CalculadoraLexer
from .CalculadoraParser import CalculadoraParser
from .Visitor import Visitor  # Tú lo desarrollas

def run_code(code):
    try:
        input_stream = InputStream(code)
        lexer = CalculadoraLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = CalculadoraParser(stream)
        tree = parser.programa()

        visitor = Visitor()
        output = visitor.visit(tree)
        return str(output)
    except Exception as e:
        return f"Error de ejecución: {e}"
