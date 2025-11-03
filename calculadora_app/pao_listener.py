from .interpreter.CalculadoraParser import CalculadoraParser
from .interpreter.CalculadoraListener import CalculadoraListener
from antlr4 import ParseTreeWalker

class PAOListener(CalculadoraListener):
    def __init__(self):
        self.variables = {}
        self.arbol = []

    def exitAsignacion(self, ctx:CalculadoraParser.AsignacionContext):
        if ctx.ID() is None:
            return
        var_name = ctx.ID().getText()
        value = self.eval_expr(ctx.expresion())
        self.variables[var_name] = value
        self.arbol.append(f"• Asigna {value} a la variable {var_name}. Estado: {self.variables.copy()}")

    def exitCondicional(self, ctx:CalculadoraParser.CondicionalContext):
        # Evaluar condición
        left = self.eval_expr(ctx.condicion().getChild(0))
        op = ctx.condicion().getChild(1).getText()
        right = self.eval_expr(ctx.condicion().getChild(2))
        result = False
        if op == '>': result = left > right
        elif op == '<': result = left < right
        elif op == '==': result = left == right
        elif op == '!=': result = left != right
        elif op == '>=': result = left >= right
        elif op == '<=': result = left <= right

        self.arbol.append(f"• Evalúa condición: {left} {op} {right} -> {result}")

        # Ejecutar instrucciones dentro del bloque si es True
        if result:
            walker = ParseTreeWalker()
            for instr in ctx.instruccion():
                walker.walk(self, instr)

    # Función recursiva para evaluar expresiones
    def eval_expr(self, ctx):
        if ctx.getChildCount() == 1:  # Número o variable
            text = ctx.getText()
            if text.isdigit():
                return int(text)
            else:
                return self.variables.get(text, 0)
        elif ctx.getChildCount() == 3:  # Operación binaria
            left = self.eval_expr(ctx.getChild(0))
            op = ctx.getChild(1).getText()
            right = self.eval_expr(ctx.getChild(2))
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
        return 0

    #python manage.py runserver