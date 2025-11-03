grammar Calculadora;

// --- Regla inicial del programa ---
programa
    : (instruccion)* EOF
    ;

// --- Instrucciones válidas ---
instruccion
    : asignacion
    | condicional
    ;

// --- Asignación de variables ---
asignacion
    : ID '=' expr ';'
    ;

// --- Condicional IF ---
condicional
    : 'if' '(' condicion ')' '{' (instruccion)* '}'
    ;

// --- Expresiones aritméticas ---
expresion
    : termino (('+' | '-') termino)*
    ;

termino
    : factor (('*' | '/') factor)*
    ;

factor
    : NUM
    | ID
    | '(' expresion ')'
    ;

// --- Operadores lógicos de condición ---
condicion
    : expresion ('>' | '<' | '==' | '!=' | '>=' | '<=') expresion
    ;

// === TOKENS (Reglas Léxicas) ===
ID  : [a-zA-Z_][a-zA-Z_0-9]* ;
NUM : [0-9]+ ;

// Espacios → ignorados
WS : [ \t\r\n]+ -> skip ;
