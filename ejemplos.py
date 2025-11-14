from typing import Dict
import json
import random

def obtener_ejemplo_gramatica(tipo: int) -> str:
    if tipo == 3:
        return "S -> aA\nA -> b | aA"
    if tipo == 2:
        return "S -> aSb | ab"
    if tipo == 1:
        return "AB -> aB\nA -> a\nB -> b"
    if tipo == 0:
        return "S -> aS\nS -> epsilon\nA -> aSb"
    return "S -> aA\nA -> b"

def obtener_ejemplo_automata(tipo: int) -> str:
    if tipo == 3:
        data: Dict = {
            "tipo": "AFD",
            "estados": ["q0", "q1"],
            "alfabeto": ["a", "b"],
            "estado_inicial": "q0",
            "estados_finales": ["q1"],
            "transiciones": [
                {"origen": "q0", "simbolo": "a", "destino": "q1"},
                {"origen": "q1", "simbolo": "b", "destino": "q1"},
            ],
        }
        return json.dumps(data, indent=2)
    if tipo == 2:
        data = {
            "tipo": "AP",
            "estados": ["q0", "q1", "qf"],
            "alfabeto": ["a", "b"],
            "estado_inicial": "q0",
            "estados_finales": ["qf"],
            "transiciones": [
                {"origen": "q0", "simbolo": "a", "destino": "q0"},
                {"origen": "q0", "simbolo": "b", "destino": "q1"},
                {"origen": "q1", "simbolo": "b", "destino": "qf"},
            ],
        }
        return json.dumps(data, indent=2)
    if tipo == 0:
        data = {
            "tipo": "MT",
            "estados": ["q0", "q1", "qf"],
            "alfabeto": ["a", "b", "_"],
            "estado_inicial": "q0",
            "estados_finales": ["qf"],
            "transiciones": [
                {"origen": "q0", "simbolo": "a", "destino": "q1"},
                {"origen": "q1", "simbolo": "b", "destino": "qf"},
            ],
        }
        return json.dumps(data, indent=2)
    return obtener_ejemplo_automata(3)

def generar_gramatica_aleatoria(tipo: int) -> str:
    base = obtener_ejemplo_gramatica(tipo)
    simbolos = ["a", "b", "c"]
    cambio = random.choice(simbolos)
    return base.replace("a", cambio, 1)
