from dataclasses import dataclass
from typing import List, Tuple, Set
import collections
from analizador_gramatica import Produccion, parsear_gramatica

TYPE_LABELS = {
    0: "Tipo 0 - Lenguaje Recursivamente Enumerable",
    1: "Tipo 1 - Lenguaje Sensible al Contexto",
    2: "Tipo 2 - Lenguaje Libre de Contexto",
    3: "Tipo 3 - Lenguaje Regular",
}

@dataclass
class ResultadoClasificacion:
    tipo: int
    etiqueta: str
    explicacion: List[str]

def es_no_terminal(s: str) -> bool:
    return len(s) == 1 and s.isupper()

def revisar_regular(producciones: List[Produccion]) -> Tuple[bool, List[str]]:
    razones: List[str] = []
    razones.append("Revisando si la gramatica puede ser Tipo 3 (Regular).")
    for p in producciones:
        L = p.izquierda
        R = p.derecha
        if len(L) != 1 or not es_no_terminal(L):
            razones.append(f"- La produccion '{L} -> {R or 'epsilon'}' no tiene un solo no terminal en el lado izquierdo.")
            razones.append("Conclusion: la gramatica no es Tipo 3.")
            return False, razones
        if R == "":
            razones.append(f"- La produccion '{L} -> epsilon' se acepta como caso especial.")
            continue
        if len(R) == 1:
            a = R[0]
            if es_no_terminal(a):
                razones.append(f"- La produccion '{L} -> {R}' usa solo no terminales en el lado derecho, no es de la forma A -> a.")
                razones.append("Conclusion: la gramatica no es Tipo 3.")
                return False, razones
            razones.append(f"- La produccion '{L} -> {R}' es de la forma A -> a.")
            continue
        if len(R) == 2:
            a, B = R[0], R[1]
            if es_no_terminal(a) or not es_no_terminal(B):
                razones.append(f"- La produccion '{L} -> {R}' no es de la forma A -> aB.")
                razones.append("Conclusion: la gramatica no es Tipo 3.")
                return False, razones
            razones.append(f"- La produccion '{L} -> {R}' es de la forma A -> aB.")
            continue
        razones.append(f"- La produccion '{L} -> {R}' tiene longitud mayor que 2 en el lado derecho.")
        razones.append("Conclusion: la gramatica no es Tipo 3.")
        return False, razones
    razones.append("Todas las producciones cumplen las formas permitidas para una gramatica regular.")
    return True, razones

def revisar_libre_contexto(producciones: List[Produccion]) -> Tuple[bool, List[str]]:
    razones: List[str] = []
    razones.append("Revisando si la gramatica puede ser Tipo 2 (Libre de contexto).")
    for p in producciones:
        L = p.izquierda
        R = p.derecha
        if len(L) != 1 or not es_no_terminal(L):
            razones.append(f"- La produccion '{L} -> {R or 'epsilon'}' no tiene exactamente un no terminal en el lado izquierdo.")
            razones.append("Conclusion: la gramatica no es Tipo 2.")
            return False, razones
    razones.append("Todas las producciones tienen un solo no terminal en el lado izquierdo.")
    return True, razones

def revisar_sensible_contexto(producciones: List[Produccion]) -> Tuple[bool, List[str]]:
    razones: List[str] = []
    razones.append("Revisando si la gramatica puede ser Tipo 1 (Sensible al contexto).")
    if not producciones:
        razones.append("No hay producciones.")
        return False, razones
    simbolo_inicial = producciones[0].izquierda
    for p in producciones:
        L = p.izquierda
        R = p.derecha
        if R == "" and L != simbolo_inicial:
            razones.append(f"- La produccion '{L} -> epsilon' esta permitida solo para el simbolo inicial '{simbolo_inicial}'.")
            razones.append("Conclusion: la gramatica no es Tipo 1.")
            return False, razones
        if len(L) > len(R) and R != "":
            razones.append(f"- La produccion '{L} -> {R}' viola la condicion |LHS| <= |RHS|.")
            razones.append("Conclusion: la gramatica no es Tipo 1.")
            return False, razones
    razones.append("Todas las producciones respetan la condicion de longitud para Tipo 1.")
    return True, razones

def clasificar_gramatica_texto(texto: str) -> ResultadoClasificacion:
    producciones = parsear_gramatica(texto)
    explicacion_total: List[str] = []
    es_reg, exp_reg = revisar_regular(producciones)
    explicacion_total.extend(exp_reg)
    if es_reg:
        tipo = 3
        explicacion_total.append("La gramatica cumple las condiciones de Tipo 3 (Regular).")
        return ResultadoClasificacion(tipo=tipo, etiqueta=TYPE_LABELS[tipo], explicacion=explicacion_total)
    es_glc, exp_glc = revisar_libre_contexto(producciones)
    explicacion_total.extend(exp_glc)
    if es_glc:
        tipo = 2
        explicacion_total.append("La gramatica cumple las condiciones de Tipo 2 (Libre de contexto).")
        return ResultadoClasificacion(tipo=tipo, etiqueta=TYPE_LABELS[tipo], explicacion=explicacion_total)
    es_sens, exp_sens = revisar_sensible_contexto(producciones)
    explicacion_total.extend(exp_sens)
    if es_sens:
        tipo = 1
        explicacion_total.append("La gramatica cumple las condiciones de Tipo 1 (Sensible al contexto).")
        return ResultadoClasificacion(tipo=tipo, etiqueta=TYPE_LABELS[tipo], explicacion=explicacion_total)
    tipo = 0
    explicacion_total.append("La gramatica no cumple las condiciones de los tipos 3, 2 ni 1.")
    explicacion_total.append("Conclusion final: se clasifica como Tipo 0 (Lenguaje recursivamente enumerable).")
    return ResultadoClasificacion(tipo=tipo, etiqueta=TYPE_LABELS[tipo], explicacion=explicacion_total)

def generar_cadenas(producciones: List[Produccion], max_longitud: int = 4, simbolo_inicial: str = "S") -> Set[str]:
    agenda = collections.deque()
    visitados: Set[str] = set()
    agenda.append(simbolo_inicial)
    visitados.add(simbolo_inicial)
    resultados: Set[str] = set()
    while agenda:
        cadena = agenda.popleft()
        if all(not c.isupper() for c in cadena):
            if len(cadena) <= max_longitud:
                resultados.add(cadena)
            continue
        if len(cadena) > max_longitud + 2:
            continue
        idx = None
        for i, c in enumerate(cadena):
            if c.isupper():
                idx = i
                break
        if idx is None:
            continue
        nt = cadena[idx]
        for p in producciones:
            if p.izquierda == nt:
                reemplazo = p.derecha
                nueva = cadena[:idx] + reemplazo + cadena[idx + 1 :]
                if len(nueva) <= max_longitud + 2 and nueva not in visitados:
                    visitados.add(nueva)
                    agenda.append(nueva)
    return resultados

def comparar_gramaticas_texto(texto1: str, texto2: str, max_longitud: int = 4) -> str:
    p1 = parsear_gramatica(texto1)
    p2 = parsear_gramatica(texto2)
    lang1 = generar_cadenas(p1, max_longitud=max_longitud)
    lang2 = generar_cadenas(p2, max_longitud=max_longitud)
    if lang1 == lang2:
        return "Posible equivalencia: los lenguajes generados coinciden hasta la longitud maxima indicada."
    solo1 = sorted(list(lang1 - lang2))
    solo2 = sorted(list(lang2 - lang1))
    partes: List[str] = []
    partes.append("Los lenguajes no coinciden completamente en la longitud probada.")
    if solo1:
        partes.append("Cadenas generadas solo por la primera gramatica: " + ", ".join(solo1))
    if solo2:
        partes.append("Cadenas generadas solo por la segunda gramatica: " + ", ".join(solo2))
    return "\n".join(partes)
