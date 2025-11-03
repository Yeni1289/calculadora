# pao_calculadora_completa.py
from antlr4 import *
from CalculadoraLexer import CalculadoraLexer
from CalculadoraParser import CalculadoraParser
from CalculadoraParserListener import CalculadoraParserListener

# Diccionario global para el estado de variables
variables = {}

class PAOListener(CalculadoraParserListener):
    def __init__(self):
        super().__init__()
        self.paso = 1

    # --- Ejecutar asignación ---
    def exitAsignacion(self, ctx:CalculadoraParser.AsignacionContext):
        var = ctx.ID().getText()
        valor = self.evalua_expresion(ctx.expresion())
        variables[var] = valor
        print(f"{self.paso} {var} = {valor};")
        print(f"Asigna {valor} a la variable {var}. Estado: {variables}")
        self.paso += 1

    # --- Ejecutar condicional ---
    def enterCondicional(self, ctx:CalculadoraParser.CondicionalContext):
        resultado = self.evalua_condicion(ctx.condicion())
        cond_text = ctx.condicion().getText()
        print(f"{self.paso} if ({cond_text})")
        print(f"Evalúa {self.evalua_expresion(ctx.condicion().expresion(0))} {ctx.condicion().getChild(1).getText()} "
              f"{self.evalua_expresion(ctx.condicion().expresion(1))}, resultado: {resultado}.", end=" ")
        if resultado:
            print("Entra al bloque")
        else:
            print("No entra al bloque")
        self.condicion_valida = resultado
        self.paso += 1

    # --- Evaluar expresiones aritméticas ---
    def evalua_expresion(self, ctx):
        if ctx.NUM():
            return int(ctx.NUM().getText())
        elif ctx.ID():
            var = ctx.ID().getText()
            return variables.get(var, 0)
        elif ctx.getChildCount() == 3:
            left = self.evalua_expresion(ctx.getChild(0))
            right = self.evalua_expresion(ctx.getChild(2))
            op = ctx.getChild(1).getText()
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left // right
        elif ctx.getChildCount() == 1:
            return self.evalua_expresion(ctx.getChild(0))
        else:
            return 0

    # --- Evaluar condición ---
    def evalua_condicion(self, ctx):
        left = self.evalua_expresion(ctx.expresion(0))
        right = self.evalua_expresion(ctx.expresion(1))
        op = ctx.getChild(1).getText()
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '==': return left == right
        if op == '!=': return left != right
        if op == '>=': return left >= right
        if op == '<=': return left <= right

def main():
    print("=== Calculadora Interactiva PAO ===")
    archivo = input("Ingrese el nombre del archivo con su programa (ej: programa.txt): ")
    input_stream = FileStream(archivo, encoding="utf-8")
    lexer = CalculadoraLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CalculadoraParser(stream)
    tree = parser.programa()
    listener = PAOListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    print("\nAl finalizar, el programa imprime el diccionario de variables mostrando todos los valores calculados:")
    print(variables)

if __name__ == "__main__":
    main()
