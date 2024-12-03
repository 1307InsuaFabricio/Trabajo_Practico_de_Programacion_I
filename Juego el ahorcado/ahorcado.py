import json  # Importamos la librería JSON para manejar archivos en este formato
import random  # Importamos random para seleccionar palabras aleatoriamente

# Cargar palabras desde el archivo JSON "data.json"
def cargar_palabras(palabra): ## yo
    """
    Esta función carga una lista de palabras desde un archivo JSON.
    El archivo debe contener una clave "ahorcado" que almacene las palabras.
    """
    try:
        # Intentamos abrir el archivo en modo lectura con codificación UTF-8
        with open(palabra, "r", encoding="utf-8") as file:
            data = json.load(file)  # Cargamos el contenido del archivo como un diccionario
            return data.get("ahorcado", [])  # Devolvemos la lista de palabras asociada a la clave "ahorcado"
    except FileNotFoundError:  # Si el archivo no existe
        print(f"El archivo {palabra} no existe.")
        return []
    except json.JSONDecodeError:  # Si el archivo tiene errores de formato
        print(f"Error al leer el archivo {palabra}. Verifica el formato.")
        return []

# Cargar puntajes desde el archivo JSON "scores.json"
def cargar_puntajes(palabra): ## yo
    """
    Esta función carga una lista de puntajes desde un archivo JSON.
    """
    try:
        # Intentamos abrir el archivo en modo lectura con codificación UTF-8
        with open(palabra, "r", encoding="utf-8") as file:
            return json.load(file)  # Retornamos la lista de puntajes
    except FileNotFoundError:  # Si el archivo no existe
        return []  # Retornamos una lista vacía por defecto
    except json.JSONDecodeError:  # Si el archivo tiene errores de formato
        print(f"Error al leer el archivo {palabra}. Verifica el formato.")
        return []

def guardar_puntajes(archivo, puntajes_existentes): ## fran
    """
    Esta función guarda una lista de puntajes en un archivo JSON.
    """
    with open(archivo, "w", encoding="utf-8") as file:  # Abrimos el archivo en modo escritura
        json.dump(puntajes_existentes, file, indent=4)  # Guardamos la lista en formato JSON con indentación

# Mostrar horca y monigote progresivamente
def mostrar_monigote(intentos_restantes): ## yo
    """
    Muestra el monigote y la horca de acuerdo con los intentos restantes.
    """
    muñeco = [
        # Representaciones ASCII del monigote en cada etapa
        """
        ════════
         |    ║
              ║
              ║
              ║
              ║
    ════════════
        """,
        """
        ════════
         |    ║
         O    ║
              ║
              ║
              ║
    ════════════
        """,
        """
        ════════
         |    ║
         O    ║
         |    ║
              ║
              ║
    ════════════
        """,
        """
        ════════
         |    ║
         O    ║
        /|    ║
              ║
              ║
    ════════════
        """,
        """
        ════════
         |    ║
         O    ║
        /|\\   ║
              ║
              ║
    ════════════
        """,
        """
        ════════
         |    ║
         O    ║
        /|\\   ║
        /     ║
              ║
    ════════════
        """,
        """
        ════════
         |    ║
         O    ║
        /|\\   ║
        / \\   ║
              ║
    ════════════
        """
    ]
    # Mostramos la parte del monigote correspondiente a los intentos restantes
    print(muñeco[6 - intentos_restantes])  

# Mostrar menú principal
def mostrar_menu(): 
    """
    Despliega el menú principal del juego.
    """
    print("\n--- Menú Principal ---")
    print("1. Jugar")
    print("2. Puntajes")
    print("3. Salir")
    return input("Seleccione una opción: ")

# Jugar una partida
def jugar(palabras, puntajes): # ambos
    """
    Ejecuta la lógica principal del juego del ahorcado.
    """
    idioma = input("Seleccione el idioma (es/en): ").strip().lower()  # Selección del idioma
    palabra_clave = "ES" if idioma == "es" else "EN"  # Definimos la clave en base al idioma
    palabra_seleccionada = random.choice(palabras)[palabra_clave].lower()  # Seleccionamos una palabra al azar
    palabra_oculta = ["_" for _ in palabra_seleccionada]  # Creamos una representación oculta de la palabra
    letras_usadas = set()  # Inicializamos un conjunto para las letras usadas
    intentos_restantes = 6  # Número máximo de intentos
    puntaje = 0  # Inicializamos el puntaje
    
    while intentos_restantes > 0 and "_" in palabra_oculta:  # Continuamos mientras queden intentos o letras por adivinar
        print("\nPalabra:", " ".join(palabra_oculta))
        print("Letras usadas:", ", ".join(sorted(letras_usadas)))
        print("Intentos restantes:", intentos_restantes)
        mostrar_monigote(intentos_restantes)  # Mostramos el monigote
        
        letra = input("Introduce una letra: ").strip().lower()  # Solicitamos una letra al usuario
        
        if len(letra) != 1 or not letra.isalpha():  # Verificamos que sea una sola letra válida
            print("Por favor, ingresa solo una letra válida.")
            continue
        
        if letra in letras_usadas:  # Verificamos si la letra ya fue usada
            print("¡Ya usaste esa letra! Intenta con otra.")
            continue
        
        letras_usadas.add(letra)  # Añadimos la letra al conjunto de usadas
        
        if letra in palabra_seleccionada:  # Si la letra está en la palabra
            print("¡Bien hecho! Adivinaste una letra.")
            for i, l in enumerate(palabra_seleccionada):  # Reemplazamos los guiones correspondientes
                if l == letra:
                    palabra_oculta[i] = letra
                    puntaje += 1
        else:  # Si la letra no está en la palabra
            print(f"Letra incorrecta. Te quedan {intentos_restantes - 1} intentos.")
            intentos_restantes -= 1
            mostrar_monigote(intentos_restantes)  # Mostramos el monigote actualizado
    
    if "_" not in palabra_oculta:  # Si adivinó toda la palabra
        print("¡Ganaste! La palabra era:", palabra_seleccionada, "y tu puntuación es:", puntaje * 2)
        puntaje += len(palabra_seleccionada)  # Sumamos un bonus al puntaje
    else:  # Si perdió
        print("¡Perdiste! La palabra era:", palabra_seleccionada)
    
    nombre = input("Introduce tu nombre: ").strip()  # Solicitamos el nombre del jugador
    puntajes.append({"nombre": nombre, "puntaje": puntaje, "palabra": palabra_seleccionada})  # Registramos el puntaje
    
    # Ordenamos los puntajes de mayor a menor
    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)
    
    # Guardamos solo los 15 mejores puntajes
    guardar_puntajes("Juego el ahorcado\\scores.json", puntajes_ordenados[:15])
    
    print("¡Puntaje guardado!")

# Mostrar mejores puntajes
def mostrar_puntajes(puntajes): # ambos
    """
    Muestra los mejores puntajes registrados.
    """
    print("\n--- Mejores Puntajes ---")
    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)[:5]  # Ordenamos y limitamos a 5
    for idx, score in enumerate(puntajes_ordenados, start=1):  # Mostramos los puntajes
        print(f"{idx}. {score['nombre']} - {score['puntaje']} puntos - Palabra: {score['palabra']}")

# Programa principal
def main():
    """
    Función principal que maneja el flujo del programa.
    """
    palabras = cargar_palabras("data.json")  # Cargamos las palabras
    puntajes = cargar_puntajes("scores.json")  # Cargamos los puntajes
    
    while True:  # Ciclo del menú principal
        opcion = mostrar_menu()  # Mostramos el menú y pedimos una opción
        if opcion == "1":
            jugar(palabras, puntajes)  # Iniciamos el juego
        elif opcion == "2":
            mostrar_puntajes(puntajes)  # Mostramos los puntajes
        elif opcion == "3":
            print("¡Gracias por jugar!")  # Salimos del programa
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# Iniciamos el programa si el archivo es ejecutado directamente
if __name__ == "__main__":
    main()
