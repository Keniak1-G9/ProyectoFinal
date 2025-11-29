# "C:\Users\jtris\Documents\piton\U\ADA\ProyectoFinal"

import os
import json
from pprint import pprint
import time
import tracemalloc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# leer datos desde el json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ruta_archivo(nombre):
    return os.path.join(BASE_DIR, nombre)

def leer_peliculas(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            print("Archivo leído desde:", nombre_archivo)
            return json.load(archivo)

    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {nombre_archivo}")
        return []

    except json.JSONDecodeError as e:
        print("ERROR en el formato JSON:", e)
        return []

def guardar_peliculas(nombre_archivo, peliculas):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(peliculas, archivo, indent=4, ensure_ascii=False)
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(peliculas, archivo, indent=4, ensure_ascii=False)
     
def ingresar_pelicula(peliculas, nombre_archivo):
    print("\n=== INGRESAR NUEVA PELÍCULA ===")

    # Generar id incremental
    nuevo_id = 1 if not peliculas else peliculas[-1]["id"] + 1
    print(f"ID generado automáticamente: {nuevo_id}")

    # Título
    while True:
        titulo = input("Título: ").strip()
        if titulo:
            break
        print("El título no puede estar vacío.")

    # Director
    while True:
        director = input("Director: ").strip()
        if director:
            break
        print("El director no puede estar vacío.")

    # Duración
    while True:
        try:
            duracion = int(input("Duración (minutos): "))
            if duracion > 0:
                break
            else:
                print("La duración debe ser mayor que cero.")
        except ValueError:
            print("Ingrese un número entero válido.")

    # Año
    while True:
        try:
            ano = int(input("Año (entero): "))
            if 1880 < ano <= 2100:
                break
            else:
                print("Ingrese un año razonable (1880 - 2100).")
        except ValueError:
            print("Año inválido. Intente nuevamente.")

    # Rating
    while True:
        try:
            rating = float(input("Rating (0 a 10): "))
            if 0 <= rating <= 10:
                break
            else:
                print("El rating debe estar entre 0 y 10.")
        except ValueError:
            print("Ingrese un número válido.")

    # Crear película
    nueva_peli = {
        "id": nuevo_id,
        "titulo": titulo,
        "director": director,
        "duracion": duracion,
        "ano": ano,
        "rating": rating
    }

    # Guardar
    peliculas.append(nueva_peli)
    guardar_peliculas(nombre_archivo, peliculas)

    print("\nPelícula registrada exitosamente.")
    mostrar_pelicula(nueva_peli)


# algoritmos de ordenamiento
def bubble_sort(lista, campo):
    n = len(lista)

    for i in range(n - 1): 
        for j in range(n - i - 1):
            if lista[j][campo] > lista[j + 1][campo]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def quick_sort(lista, campo, inicio, fin): # (ignorar)
    if inicio >= fin:
        return
    pivote = lista[fin][campo]
    i = inicio - 1
    for j in range(inicio, fin):
        if lista[j][campo] <= pivote:
            i = i + 1
            lista[i], lista[j] = lista[j], lista[i]
    lista[i + 1], lista[fin] = lista[fin], lista[i + 1]
    pos = i + 1
    quick_sort(lista, campo, inicio, pos - 1)
    quick_sort(lista, campo, pos + 1, fin)

# algoritmos de busqueda
def busqueda_secuencial(lista, campo, x):
    resultados = [] # guarda todo los valores que encuentra con el mismo valor de campo
    for i in range(len(lista)):
        if lista[i][campo] == x:
            resultados.append(lista[i])
    return resultados  
        
def busqueda_binaria(lista, campo, x): # ignorar
    resultados = []
    inicio = 0
    fin = len(lista) - 1

    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio][campo] == x:
            resultados.append(lista[medio])

            i = medio - 1  # busca en la izq
            while i >= 0 and lista[i][campo] == x:
                resultados.append(lista[i])
                i -= 1

            i = medio + 1  # busca en la derecha
            while i < len(lista) and lista[i][campo] == x:
                resultados.append(lista[i])
                i += 1
        
            return resultados
        
        elif lista[medio][campo] < x:
            inicio = medio + 1
        else:
            fin = medio - 1

    return [] # pa comparar en el main si no se encontro nada

#complejidades empiricas
def medir_tiempo_memoria(funcion, *args):
    tracemalloc.start()
    inicio = time.perf_counter()
    
    resultado = funcion(*args)
    
    fin = time.perf_counter()
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    tiempo_s = fin - inicio
    tiempo_ms = tiempo_s * 1000
    memoria_kb = memoria_pico / 1024
    
    return tiempo_s, tiempo_ms, memoria_kb, resultado

def generar_graficas_interactivas(tamaños, tiempos, memorias):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('<b>Complejidad Temporal</b>', '<b>Complejidad Espacial</b>'),
        horizontal_spacing=0.10
    )
    
    # tiempos
    fig.add_trace(
        go.Scatter(
            x=tamaños,
            y=tiempos['suma_elementos'],
            mode='lines+markers',
            name='Búsqueda Secuencial O(n)',
            line=dict(color='green', width=3),
            marker=dict(size=10),
            legendgroup='busqueda',
            hovertemplate='<b>Búsqueda Secuencial</b><br>n: %{x}<br>Tiempo: %{y:.9f}s<extra></extra>'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=tamaños,
            y=tiempos['contar_pares'],
            mode='lines+markers',
            name='Bubble Sort O(n²)',
            line=dict(color='purple', width=3),
            marker=dict(size=10),
            legendgroup='ordenamiento',
            hovertemplate='<b>Bubble Sort</b><br>n: %{x}<br>Tiempo: %{y:.9f}s<extra></extra>'
        ),
        row=1, col=1
    )

    # memorias
    fig.add_trace(
        go.Scatter(
            x=tamaños,
            y=memorias['suma_elementos'],
            mode='lines+markers',
            name='Búsqueda Secuencial O(n)',
            line=dict(color='green', width=3),
            marker=dict(size=10),
            legendgroup='busqueda',
            showlegend=False,
            hovertemplate='<b>Búsqueda Secuencial</b><br>n: %{x}<br>Memoria: %{y:.2f} KB<extra></extra>'
        ),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(
            x=tamaños,
            y=memorias['contar_pares'],
            mode='lines+markers',
            name='Bubble Sort O(n²)',
            line=dict(color='purple', width=3),
            marker=dict(size=10),
            legendgroup='ordenamiento',
            showlegend=False,
            hovertemplate='<b>Bubble Sort</b><br>n: %{x}<br>Memoria: %{y:.2f} KB<extra></extra>'
        ),
        row=1, col=2
    )

    # ejes
    fig.update_xaxes(
        title_text="<b>Tamaño de entrada (n)</b>",
        row=1, col=1
    )
    fig.update_xaxes(
        title_text="<b>Tamaño de entrada (n)</b>",
        row=1, col=2
    )

    fig.update_yaxes(
        title_text="<b>Tiempo (segundos)</b>",
        type="log",
        row=1, col=1
    )
    fig.update_yaxes(
        title_text="<b>Memoria pico usada (KB)</b>",
        row=1, col=2
    )

    #layout
    fig.update_layout(
        title={
            'text': "<b>Análisis Empírico de Búsqueda y Ordenamiento</b><br>"
                    "<sub>Búsqueda Secuencial O(n) y Bubble Sort O(n²)</sub>",
            'x': 0.5
        },
        height=700,
        width=1600,
        hovermode='closest',
        template='plotly_white',
        legend=dict(
            orientation="v",
            y=0.98,
            x=1.02,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="black",
            borderwidth=2
        ),
        margin=dict(l=80, r=200, t=120, b=80)
    )

    # pagina
    html_content = fig.to_html(include_plotlyjs='cdn')

    css_style = """
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 30px;
            max-width: 1700px;
            width: 100%;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
        }
        .header h1 { margin: 0; }
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #888;
            font-size: 12px;
        }
    </style>
    """

    html_final = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Análisis Empírico</title>
        {css_style}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Análisis Empírico de Algoritmos</h1>
                <p>Búsqueda Secuencial y Bubble Sort</p>
            </div>

            {html_content.split('<body>')[1].split('</body>')[0]}

            <div class="info-box">
                <ul>
                    <li><b style="color:green">Búsqueda Secuencial:</b> O(n)</li>
                    <li><b style="color:purple">Bubble Sort:</b> O(n²)</li>
                </ul>
            </div>

            <div class="footer">
                Proyecto – Análisis y Diseño de Algoritmos
            </div>
        </div>
    </body>
    </html>
    """

    with open("analisis_empirico_peliculas.html", "w", encoding="utf-8") as f:
        f.write(html_final)

    print("\n Gráfica generada en 'analisis_empirico_peliculas.html'\n")

def analisis_empirico():
    print("\n" + "=" * 80)
    print("ANÁLISIS EMPÍRICO – BÚSQUEDA SECUENCIAL Y BUBBLE SORT")
    print("=" * 80)

    archivos = {
        50: "peliculas_50.json",
        200: "peliculas_200.json",
        500: "peliculas_500.json",
        1000: "peliculas_1000.json"
    }

    tamaños = list(archivos.keys())

    # ESTRUCTURA ESPERADA POR LA GRÁFICA
    tiempos = {
        'suma_elementos': [],   # busqueda secuencial 
        'contar_pares': []      # bubble Sort 
    }

    memorias = {
        'suma_elementos': [],
        'contar_pares': []
    }

    for n in tamaños:
        print(f"Procesando tamaño n = {n}...")

        peliculas = leer_peliculas(archivos[n])

        # =========================
        # BÚSQUEDA SECUENCIAL
        # =========================
        t_s, _, mem, _ = medir_tiempo_memoria(
            busqueda_secuencial,
            peliculas,
            "id",
            -1        # valor que no existe para forzar recorrido completo
        )

        tiempos['suma_elementos'].append(t_s)
        memorias['suma_elementos'].append(mem)

        # =========================
        # BUBBLE SORT
        # =========================
        copia = peliculas.copy()  # importante para no alterar la original

        t_s, _, mem, _ = medir_tiempo_memoria(
            bubble_sort,
            copia,
            "rating"
        )

        tiempos['contar_pares'].append(t_s)
        memorias['contar_pares'].append(mem)

    print("\nAnálisis finalizado. Generando gráfica...\n")

    generar_graficas_interactivas(tamaños, tiempos, memorias)


# vainas pal main
def menu_principal():
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Ingresar película")
    print("2. Búsqueda de película por ID")
    print("3. Búsqueda de película por título")
    print("4. Generar reporte de películas con mayor rating")
    print("5. Ordenamiento")
    print("6. Búsqueda")
    print("7. Análisis empírico")
    print("8. Salir")


def menu_ordenamiento():
    print("\n--- ORDENAMIENTO ---")
    print("1. Bubble Sort")
    print("2. Quick Sort")
    print("3. Volver")


def menu_busqueda():
    print("\n--- BÚSQUEDA ---")
    print("1. Búsqueda Secuencial")
    print("2. Búsqueda Binaria")
    print("3. Volver")


def mostrar_pelicula(p):
    print("\n==============================")
    print("Película")
    print("==============================")
    print(f"ID: {p['id']}")
    print(f"Título: {p['titulo']}")
    print(f"Director: {p['director']}")
    print(f"Año: {p['ano']}")
    print(f"Duración: {p['duracion']} minutos")
    print(f"Rating: {p['rating']}")
    print("==============================\n")













## BORRAR
def buscar_por_id(peliculas):
    try:
        _id = int(input("Ingrese el ID a buscar: "))
    except:
        print("ID inválido.")
        return

    for p in peliculas:
        if p["id"] == _id:
            print("\nPelícula encontrada:")
            mostrar_pelicula(p)
            return

    print("No existe una película con ese ID.")


def buscar_por_titulo(peliculas):
    titulo = input("Ingrese el título a buscar: ").lower().strip()
    resultados = [p for p in peliculas if titulo in p["titulo"].lower()]

    if resultados:
        print("\nResultados:")
        for r in resultados:
            mostrar_pelicula(r)
    else:
        print("No se encontraron películas con ese título.")


# =========================
#   REPORTE: MAYOR RATING
# =========================

def reporte_mayor_rating(peliculas):
    if not peliculas:
        print("No hay películas registradas.")
        return

    max_rating = max(p["rating"] for p in peliculas)
    mejores = [p for p in peliculas if p["rating"] == max_rating]

    print(f"\n=== PELÍCULAS CON MAYOR RATING ({max_rating}) ===")
    for p in mejores:
        mostrar_pelicula(p)
        print("-" * 40)

####







def main():
    archivo = ruta_archivo("peliculas.json")
    peliculas = leer_peliculas(archivo)

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")

        match opcion:

            case "1":
                ingresar_pelicula(peliculas, archivo)

            case "2":
                buscar_por_id(peliculas)

            case "3":
                buscar_por_titulo(peliculas)

            case "4":
                reporte_mayor_rating(peliculas)

            case "5":
                # aquí se conecta con tu código ya existente
                print("Menú de ordenamiento (integración con tu lógica)…")
                # tu mismo copias el bloque que ya tienes

            case "6":
                print("Menú de búsqueda (integración con tu lógica)…")

            case "7":
                print("Llamar al análisis empírico…")

            case "8":
                print("Saliendo del programa...")
                break

            case _:
                print("Opción no válida.")
                

main()