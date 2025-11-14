# ProyectoFinallenguajes

Proyecto de escritorio en Python que permite clasificar gramáticas y autómatas dentro de la Jerarquía de Chomsky (Tipo 0, 1, 2 y 3).

El sistema funciona como una herramienta de apoyo para el curso de Lenguajes Formales y Autómatas:

- Analiza gramáticas formales (en formato texto).
- Analiza autómatas (AFD, AP, MT) descritos en JSON.
- Determina el tipo de lenguaje (0–3) según las restricciones teóricas.
- Explica paso a paso el razonamiento usado para la clasificación.
- Genera diagramas con Graphviz y reportes en PDF.
- Incluye un modo tutor tipo quiz para practicar.

## 1. Características principales

- Clasificación de gramáticas  
  - Entrada: reglas como:
    ```text
    S -> aA
    A -> b | aA
    ```
  - Salida:
    - Tipo de lenguaje (regular, libre de contexto, sensible al contexto o recursivamente enumerable).
    - Explicación línea por línea de qué condiciones se cumplen o se violan.

- Clasificación de autómatas  
  - Entrada: JSON con la definición del autómata (AFD, AP, MT).
  - Salida:
    - Tipo de máquina.
    - Nivel de la jerarquía (3, 2 o 0) según el modelo.
    - Explicación textual.

- Comparación de gramáticas  
  - Compara dos gramáticas generando cadenas hasta una longitud máxima.
  - Informa si parecen generar el mismo lenguaje (heurístico).

- Generador de ejemplos  
  - Genera gramáticas aleatorias por tipo (0–3).
  - Muestra autómatas de ejemplo en JSON.

- Modo tutor (quiz)  
  - Genera ejercicios aleatorios.
  - El usuario intenta clasificar.
  - El sistema corrige y explica.

- Reportes PDF  
  - Generación de PDF con:
    - Gramática o autómata.
    - Tipo detectado.
    - Explicación.
    - Diagramas generados.


## 2. Requisitos

- Sistema operativo: Windows 10 / 11 (64 bits).
- Python: versión 3.x (recomendado 3.10+).
- Librerías de Python:
  - `graphviz` (para hablar con Graphviz desde Python).
  - `reportlab` (para generar PDFs).
  - `tkinter` (ya viene incluido con Python en Windows).

Además, es obligatorio instalar el programa Graphviz en Windows, no solo el paquete de Python.

## 3. Instalación paso a paso

### 3.1. Instalar Python

1. Ir a la página oficial:  
   <https://www.python.org/downloads/windows/>
2. Descargar la versión para Windows (64-bit).
3. Ejecutar el instalador y marcar:
   - `Add python.exe to PATH`
4. Terminar la instalación.
5. Comprobar en una consola (`cmd`):

   ```bash
   python --version
3.2. Instalar Graphviz (programa de Windows)

### Este paso es el que permite que el botón “Ver diagrama” funcione sin errores.
Ir a: https://graphviz.org/download/

### En la sección Windows, descargar:
graphviz-14.0.2 (64-bit) EXE installer

### Ejecutar el archivo .exe. Durante la instalación:
Dejar la ruta por defecto, algo como:
C:\Program Files\Graphviz\

### En la pantalla Install Options seleccionar:
Add Graphviz to the system PATH for current user
(o “for all users” si se prefiere)
Terminar la instalación.
Cerrar y volver a abrir cualquier consola o VS Code.

### Verificar en cmd:
dot -V

### Si el comando muestra algo como:
dot - graphviz version 14.0.2 (...


entonces Graphviz está correctamente instalado y agregado al PATH.

Si no reconoce dot, hay que revisar el PATH o reinstalar marcando la opción de “Add Graphviz to the system PATH…”.
