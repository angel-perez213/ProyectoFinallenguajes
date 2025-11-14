from graphviz import Digraph


def dibujar_gramatica(producciones, ruta_salida_base: str) -> str:
    dot = Digraph("Gramatica")
    dot.attr(rankdir="LR")

    nodos = set()
    for izq, der in producciones:
        nodos.add(str(izq))
        if der == "" or str(der).lower() in ("epsilon", "eps", "e"):
            nodos.add("epsilon")
        else:
            nodos.add(str(der))

    for n in nodos:
        dot.node(str(n))

    for izq, der in producciones:
        origen = str(izq)
        if der == "" or str(der).lower() in ("epsilon", "eps", "e"):
            destino = "epsilon"
        else:
            destino = str(der)
        dot.edge(origen, destino)

    ruta_png = ruta_salida_base + ".png"
    dot.render(ruta_salida_base, format="png", cleanup=True)
    return ruta_png


def dibujar_automata(automata, ruta_salida_base: str) -> str:
    dot = Digraph("Automata")
    dot.attr(rankdir="LR")

    if isinstance(automata, dict):
        estados = automata.get("estados", [])
        estado_inicial = automata.get("estado_inicial")
        estados_finales = set(automata.get("estados_finales", []))
        transiciones = automata.get("transiciones", [])
    else:
        estados = list(getattr(automata, "estados", []))
        estado_inicial = getattr(automata, "estado_inicial", None)
        estados_finales = set(getattr(automata, "estados_finales", []))
        transiciones = getattr(automata, "transiciones", [])

    for e in estados:
        if e in estados_finales:
            dot.node(str(e), shape="doublecircle")
        else:
            dot.node(str(e), shape="circle")

    if estado_inicial is not None:
        dot.node("ini", shape="point")
        dot.edge("ini", str(estado_inicial))

    for t in transiciones:
        if isinstance(t, dict):
            origen = t.get("origen")
            destino = t.get("destino")
            simbolo = t.get("simbolo", "")
        else:
            origen = getattr(t, "origen", None)
            destino = getattr(t, "destino", None)
            simbolo = getattr(t, "simbolo", "")
        if origen is not None and destino is not None:
            dot.edge(str(origen), str(destino), label=str(simbolo))

    ruta_png = ruta_salida_base + ".png"
    dot.render(ruta_salida_base, format="png", cleanup=True)
    return ruta_png
