from calculadora_app.interpreter.CalculadoraParser import CalculadoraParser
from calculadora_app.interpreter.CalculadoraListener import CalculadoraListener

class Visitor(CalculadoraListener):
    def __init__(self):
        self.variables = {}
        self.traza = []

    def visitPrograma(self, ctx):
        resultado_final = None
        for instruccion in ctx.instruccion():
            resultado_final = self.visit(instruccion)
        return resultado_final

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()
        valor = self.visit(ctx.expresion())
        self.variables[nombre] = valor
        self.traza.append(f"• Asigna {valor} a la variable {nombre}. Estado: {self.variables}")
        return valor

    def visitExpresion(self, ctx):
        if ctx.NUM():
            return int(ctx.NUM().getText())
        elif ctx.ID():
            nombre = ctx.ID().getText()
            return self.variables.get(nombre, 0)
        elif len(ctx.termino()) > 1:
            resultado = self.visit(ctx.termino(0))
            for i in range(1, len(ctx.termino())):
                op = ctx.getChild(2 * i - 1).getText()
                val = self.visit(ctx.termino(i))
                if op == '+':
                    resultado += val
                elif op == '-':
                    resultado -= val
            return resultado
        else:
            return self.visit(ctx.termino(0))

    def visitTermino(self, ctx):
        if len(ctx.factor()) > 1:
            resultado = self.visit(ctx.factor(0))
            for i in range(1, len(ctx.factor())):
                op = ctx.getChild(2 * i - 1).getText()
                val = self.visit(ctx.factor(i))
                if op == '*':
                    resultado *= val
                elif op == '/':
                    resultado /= val
            return resultado
        else:
            return self.visit(ctx.factor(0))

    def visitFactor(self, ctx):
        if ctx.NUM():
            return int(ctx.NUM().getText())
        elif ctx.ID():
            nombre = ctx.ID().getText()
            return self.variables.get(nombre, 0)
        elif ctx.expresion():
            return self.visit(ctx.expresion())
