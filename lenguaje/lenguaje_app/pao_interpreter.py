from antlr4 import InputStream, CommonTokenStream
from lenguaje_app.interpreter.CalculadoraLexer import CalculadoraLexer
from lenguaje_app.interpreter.CalculadoraParser import CalculadoraParser
from lenguaje_app.interpreter.Visitor import Visitor

def ejecutar_codigo(codigo):
    try:
        input_stream = InputStream(codigo)
        lexer = CalculadoraLexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = CalculadoraParser(tokens)

        tree = parser.programa()

        visitor = Visitor()
        resultado = visitor.visit(tree)

        # Combinar resultado y árbol de ejecución
        salida = f"Resultado: {resultado}\n\nÁrbol de ejecución:\n" + "\n".join(visitor.traza)
        return salida
    except Exception as e:
        return f"Error al ejecutar: {str(e)}"

