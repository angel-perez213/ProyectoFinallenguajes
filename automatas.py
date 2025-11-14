from dataclasses import dataclass
from typing import List, Any
import json
from clasificador import ResultadoClasificacion, TYPE_LABELS

@dataclass
class Automata:
    tipo: str
    estados: List[str]
    alfabeto: List[str]
    transiciones: List[Any]
    estado_inicial: str
    estados_finales: List[str]

def cargar_automata_desde_json(texto_json: str) -> Automata:
    data = json.loads(texto_json)
    return Automata(
        tipo=data.get("tipo", ""),
        estados=data.get("estados", []),
        alfabeto=data.get("alfabeto", []),
        transiciones=data.get("transiciones", []),
        estado_inicial=data.get("estado_inicial", ""),
        estados_finales=data.get("estados_finales", []),
    )

def clasificar_automata(automata: Automata) -> ResultadoClasificacion:
    explicacion: List[str] = []
    tipo_lower = automata.tipo.lower()
    if "afd" in tipo_lower or "dfa" in tipo_lower or "afn" in tipo_lower or "nfa" in tipo_lower:
        t = 3
        explicacion.append("El automata se identifica como AFD o AFN.")
        explicacion.append("Los automatas finitos reconocen lenguajes regulares (Tipo 3).")
    elif "ap" in tipo_lower or "pda" in tipo_lower:
        t = 2
        explicacion.append("El automata se identifica como automata con pila (AP).")
        explicacion.append("Los automatas con pila reconocen lenguajes libres de contexto (Tipo 2).")
    elif "mt" in tipo_lower or "turing" in tipo_lower:
        t = 0
        explicacion.append("La maquina se identifica como Maquina de Turing.")
        explicacion.append("Las Maquinas de Turing reconocen lenguajes recursivamente enumerables (Tipo 0).")
    else:
        t = 0
        explicacion.append("No se reconoce el tipo de automata de forma especifica.")
        explicacion.append("Por defecto se toma como un modelo al nivel de Maquina de Turing (Tipo 0).")
    return ResultadoClasificacion(tipo=t, etiqueta=TYPE_LABELS[t], explicacion=explicacion)
