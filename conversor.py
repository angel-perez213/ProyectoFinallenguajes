import string

def _insertar_concat(regex):
    resultado = []
    simbolos = set(string.ascii_letters + string.digits)
    for i, ch in enumerate(regex):
        resultado.append(ch)
        if i + 1 < len(regex):
            c1 = ch
            c2 = regex[i + 1]
            if (c1 in simbolos or c1 == ")" or c1 == "*") and (c2 in simbolos or c2 == "("):
                resultado.append(".")
    return "".join(resultado)

def _a_postfijo(regex):
    prec = {"*": 3, ".": 2, "|": 1}
    salida = []
    pila = []
    for ch in regex:
        if ch == "(":
            pila.append(ch)
        elif ch == ")":
            while pila and pila[-1] != "(":
                salida.append(pila.pop())
            if pila and pila[-1] == "(":
                pila.pop()
        elif ch in prec:
            while pila and pila[-1] in prec and prec[pila[-1]] >= prec[ch]:
                salida.append(pila.pop())
            pila.append(ch)
        else:
            salida.append(ch)
    while pila:
        salida.append(pila.pop())
    return "".join(salida)

class NFA:
    def __init__(self):
        self.trans = {}
        self.start = None
        self.accepts = set()
        self._next = 0

    def nuevo_estado(self):
        e = self._next
        self._next += 1
        self.trans[e] = {}
        return e

    def agregar(self, origen, simbolo, destino):
        if origen not in self.trans:
            self.trans[origen] = {}
        if simbolo not in self.trans[origen]:
            self.trans[origen][simbolo] = set()
        self.trans[origen][simbolo].add(destino)

def _nfa_desde_postfijo(post):
    nfa = NFA()
    pila = []
    for ch in post:
        if ch not in {"*", ".", "|"}:
            s = nfa.nuevo_estado()
            t = nfa.nuevo_estado()
            nfa.agregar(s, ch, t)
            pila.append((s, {t}))
        elif ch == ".":
            n2 = pila.pop()
            n1 = pila.pop()
            for a in n1[1]:
                nfa.agregar(a, None, n2[0])
            pila.append((n1[0], n2[1]))
        elif ch == "|":
            n2 = pila.pop()
            n1 = pila.pop()
            s = nfa.nuevo_estado()
            t = nfa.nuevo_estado()
            nfa.agregar(s, None, n1[0])
            nfa.agregar(s, None, n2[0])
            for a in n1[1]:
                nfa.agregar(a, None, t)
            for a in n2[1]:
                nfa.agregar(a, None, t)
            pila.append((s, {t}))
        elif ch == "*":
            n = pila.pop()
            s = nfa.nuevo_estado()
            t = nfa.nuevo_estado()
            nfa.agregar(s, None, n[0])
            nfa.agregar(s, None, t)
            for a in n[1]:
                nfa.agregar(a, None, n[0])
                nfa.agregar(a, None, t)
            pila.append((s, {t}))
    inicio, aceptos = pila.pop()
    nfa.start = inicio
    nfa.accepts = aceptos
    return nfa

def _epsilon_cierre(nfa, estados):
    pila = list(estados)
    cierre = set(estados)
    while pila:
        e = pila.pop()
        for simbolo, dests in nfa.trans.get(e, {}).items():
            if simbolo is None:
                for d in dests:
                    if d not in cierre:
                        cierre.add(d)
                        pila.append(d)
    return cierre

def _mover(nfa, estados, simbolo):
    res = set()
    for e in estados:
        for s, dests in nfa.trans.get(e, {}).items():
            if s == simbolo:
                res.update(dests)
    return res

def _nfa_a_dfa(nfa):
    simbolos = set()
    for e, m in nfa.trans.items():
        for s in m.keys():
            if s is not None:
                simbolos.add(s)
    simbolos = sorted(simbolos)

    inicio = frozenset(_epsilon_cierre(nfa, {nfa.start}))
    pendientes = [inicio]
    visitados = []
    trans_dfa = {}
    aceptos_dfa = set()

    while pendientes:
        estado = pendientes.pop()
        if estado in visitados:
            continue
        visitados.append(estado)
        trans_dfa[estado] = {}
        if any(e in nfa.accepts for e in estado):
            aceptos_dfa.add(estado)
        for s in simbolos:
            mov = _mover(nfa, estado, s)
            if not mov:
                continue
            cierre = frozenset(_epsilon_cierre(nfa, mov))
            trans_dfa[estado][s] = cierre
            if cierre not in visitados and cierre not in pendientes:
                pendientes.append(cierre)

    estados_lista = list(visitados)
    nombres = {e: "q" + str(i) for i, e in enumerate(estados_lista)}
    estado_inicial = nombres[inicio]
    estados_finales = [nombres[e] for e in aceptos_dfa]

    transiciones = []
    for e, m in trans_dfa.items():
        for s, dest in m.items():
            transiciones.append(
                {
                    "origen": nombres[e],
                    "simbolo": s,
                    "destino": nombres[dest],
                }
            )

    automata = {
        "tipo": "AFD",
        "estados": list(nombres.values()),
        "alfabeto": simbolos,
        "estado_inicial": estado_inicial,
        "estados_finales": estados_finales,
        "transiciones": transiciones,
    }
    return automata

def regex_a_afd(regex):
    regex = regex.replace(" ", "")
    if not regex:
        raise ValueError("regex vacia")
    con = _insertar_concat(regex)
    post = _a_postfijo(con)
    nfa = _nfa_desde_postfijo(post)
    dfa = _nfa_a_dfa(nfa)
    return dfa

def afd_a_gramatica_regular(automata):
    estados = automata.get("estados", [])
    estado_inicial = automata.get("estado_inicial")
    estados_finales = set(automata.get("estados_finales", []))
    transiciones = automata.get("transiciones", [])

    lineas = []
    for t in transiciones:
        origen = str(t.get("origen"))
        destino = str(t.get("destino"))
        simbolo = str(t.get("simbolo", ""))
        if simbolo == "":
            continue
        linea = origen + " -> " + simbolo + destino
        lineas.append(linea)

    for f in estados_finales:
        lineas.append(f + " -> epsilon")

    if estado_inicial and estado_inicial not in estados_finales:
        pass

    return "\n".join(lineas)

def regex_a_gramatica_regular(regex):
    afd = regex_a_afd(regex)
    gr = afd_a_gramatica_regular(afd)
    return afd, gr
