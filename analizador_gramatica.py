import re
from dataclasses import dataclass
from typing import List

@dataclass
class Produccion:
    izquierda: str
    derecha: str

LINEA_GRAMATICA_RE = re.compile(r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*(?:->|→)\s*(.+)$')

def parsear_gramatica(texto: str) -> List[Produccion]:
    producciones: List[Produccion] = []
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        m = LINEA_GRAMATICA_RE.match(linea)
        if not m:
            raise ValueError(f"Linea de gramatica no valida: '{linea}'")
        izquierda, rhs = m.groups()
        izquierda = izquierda.strip()
        rhs = rhs.strip()
        for alt in rhs.split("|"):
            alt = alt.strip()
            if alt in ("ε", "epsilon", "EPS", "E"):
                alt = ""
            producciones.append(Produccion(izquierda=izquierda, derecha=alt))
    if not producciones:
        raise ValueError("No se encontraron producciones en el texto ingresado.")
    return producciones
