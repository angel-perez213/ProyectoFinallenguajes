from dataclasses import dataclass
from typing import Tuple
import random
from ejemplos import obtener_ejemplo_gramatica, obtener_ejemplo_automata

@dataclass
class EjercicioTutor:
    tipo_entrada: str
    enunciado: str
    tipo_correcto: int

def generar_ejercicio() -> EjercicioTutor:
    if random.choice([True, False]):
        tipo = random.choice([0, 1, 2, 3])
        gram = obtener_ejemplo_gramatica(tipo)
        enunciado = "Clasifica la siguiente gramatica en la jerarquia de Chomsky:\n\n" + gram
        return EjercicioTutor(tipo_entrada="gramatica", enunciado=enunciado, tipo_correcto=tipo)
    else:
        tipo = random.choice([0, 2, 3])
        auto = obtener_ejemplo_automata(tipo)
        enunciado = "Clasifica el lenguaje reconocido por el siguiente automata (en JSON):\n\n" + auto
        return EjercicioTutor(tipo_entrada="automata", enunciado=enunciado, tipo_correcto=tipo)

def evaluar_respuesta(ejercicio: EjercicioTutor, tipo_usuario: int) -> Tuple[bool, str]:
    correcto = tipo_usuario == ejercicio.tipo_correcto
    if correcto:
        return True, "Respuesta correcta. Coincide con el tipo esperado."
    return False, f"Respuesta incorrecta. El tipo correcto era {ejercicio.tipo_correcto}."
