"""
Implementación del algoritmo de Floyd-Warshall para encontrar caminos más cortos en un grafo.
Esta implementación permite:
- Leer un grafo desde un archivo
- Calcular las rutas más cortas entre cualquier par de ciudades
- Encontrar el centro del grafo
- Modificar el grafo dinámicamente
"""

import os
from src.graph import Graph  # Cambiado
from src.floyd_warshall import floyd_warshall  # Cambiado
from src.utils import read_graph_from_file, display_shortest_path, find_graph_center  # Cambiado

def main():
    """
    Función principal del programa que implementa el algoritmo de Floyd.
    
    Este método realiza las siguientes tareas:
    1. Lee un grafo desde un archivo
    2. Calcula las rutas más cortas usando el algoritmo de Floyd-Warshall
    3. Proporciona un menú interactivo con opciones para:
       - Consultar la ruta más corta entre dos ciudades
       - Encontrar el centro del grafo
       - Modificar el grafo
       - Salir del programa
    
    Returns:
        None
    """
    # Cargar el grafo desde el archivo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logistica_path = os.path.join(os.path.dirname(script_dir), 'data', 'logistica.txt')
    print(f"Intentando leer archivo desde: {logistica_path}")
    
    graph = read_graph_from_file(logistica_path)
    
    # Mostrar la matriz de adyacencia inicial
    graph.display_adjacency_matrix()
    
    # Calcular las rutas más cortas con Floyd-Warshall
    print("\nCalculando rutas más cortas con algoritmo de Floyd-Warshall...")
    distance_matrix, path_info = floyd_warshall(graph)
    print("Cálculo completado.")

    while True:
        print("\n" + "="*50)
        print("SISTEMA DE LOGÍSTICA - ALGORITMO DE FLOYD")
        print("="*50)
        print("1. Consultar ruta más corta entre dos ciudades")
        print("2. Encontrar el centro del grafo")
        print("3. Modificar el grafo")
        print("4. Salir del programa")
        print("="*50)

        choice = input("Ingrese su opción (1-4): ")

        if choice == '1':
            """
            Opción 1: Consulta la ruta más corta entre dos ciudades.
            Solicita al usuario los nombres de la ciudad origen y destino,
            y muestra la ruta más corta entre ellas junto con la distancia total.
            """
            city1 = input("Ingrese el nombre de la ciudad origen: ")
            city2 = input("Ingrese el nombre de la ciudad destino: ")
            display_shortest_path(city1, city2, distance_matrix, path_info, graph)

        elif choice == '2':
            """
            Opción 2: Encuentra el centro del grafo.
            Calcula y muestra el vértice que representa el centro del grafo.
            """
            center = find_graph_center(distance_matrix, graph)
            print(f"\nEl centro del grafo es: {center}")

        elif choice == '3':
            """
            Opción 3: Modifica el grafo.
            Permite al usuario realizar modificaciones en el grafo.
            """
            print("\nOpciones de Modificación del Grafo:")
            print("a. Interrumpir tráfico entre ciudades")
            print("b. Agregar nueva conexión entre ciudades")
            print("c. Cambiar condiciones climáticas")
            
            mod_choice = input("Ingrese su opción (a/b/c): ")
            
            if mod_choice.lower() == 'a':
                city1 = input("Ingrese ciudad origen: ")
                city2 = input("Ingrese ciudad destino: ")
                if graph.remove_edge(city1, city2):
                    print(f"\nTráfico entre {city1} y {city2} interrumpido.")
                    print("\nMatriz de adyacencia actualizada:")
                    graph.display_adjacency_matrix()
                    # Recalcular rutas
                    print("\nRecalculando rutas más cortas...")
                    distance_matrix, path_info = floyd_warshall(graph)
                    print("Rutas recalculadas correctamente.")
                else:
                    print("No se pudo interrumpir el tráfico.")

            elif mod_choice.lower() == 'b':
                city1 = input("Ingrese ciudad origen: ")
                city2 = input("Ingrese ciudad destino: ")
                try:
                    normal = float(input("Tiempo con clima normal: "))
                    rain = float(input("Tiempo con lluvia: "))
                    snow = float(input("Tiempo con nieve: "))
                    storm = float(input("Tiempo con tormenta: "))
                    
                    graph.add_edge(city1, city2, normal, rain, snow, storm)
                    print(f"Conexión agregada entre {city1} y {city2}.")
                    # Recalcular rutas
                    distance_matrix, path_info = floyd_warshall(graph)
                except ValueError:
                    print("Error: Los tiempos deben ser valores numéricos.")
                    
            elif mod_choice.lower() == 'c':
                print("Condiciones disponibles: normal, lluvia, nieve, tormenta")
                condition = input("Ingrese nueva condición climática: ").lower()
                
                if graph.set_weather_condition(condition):
                    print(f"Condición climática cambiada a: {condition}")
                    graph.display_adjacency_matrix()
                    # Recalcular rutas
                    distance_matrix, path_info = floyd_warshall(graph)
                else:
                    print("Condición climática no válida.")
            else:
                print("Opción no válida.")

        elif choice == '4':
            """
            Opción 4: Sale del programa.
            """
            print("\nGracias por usar el sistema de logística. ¡Hasta pronto!")
            break

        else:
            """
            Maneja entrada inválida.
            """
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()