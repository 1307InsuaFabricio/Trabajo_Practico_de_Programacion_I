import json
import random

# Cargar palabras desde el archivo JSON "data.json"
def cargar_palabras(palabra):
    try:
        with open(palabra, "r", encoding="utf-8") as file:
            data = json.load(file)  # Cargar el JSON completo
            return data.get("ahorcado", [])  # Acceder a la clave "ahorcado"
    except FileNotFoundError:
        print(f"El archivo {palabra} no existe.")
        return []
    except json.JSONDecodeError:
        print(f"Error al leer el archivo {palabra}. Verifica el formato.")
        return []

# Cargar puntajes desde el archivo JSON "scores.json"
def cargar_puntajes(palabra):
    try:
        with open(palabra, "r", encoding="utf-8") as file:
            return json.load(file)  # Cargar la lista de puntajes
    except FileNotFoundError:
        return []  # Si el archivo no existe, retornamos una lista vacía
    except json.JSONDecodeError:
        print(f"Error al leer el archivo {palabra}. Verifica el formato.")
        return []

def guardar_puntajes(archivo, puntajes_existentes):
    # Guardar el archivo con los puntajes actualizados, sin sobrescribir los anteriores
    with open(archivo, "w", encoding="utf-8") as file:
        json.dump(puntajes_existentes, file, indent=4)

# Mostrar horca y monigote progresivamente
def mostrar_monigote(intentos_restantes):
    muñeco = [
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
    
    # Mostrar la parte del muñeco correspondiente al intento fallido
    print(muñeco[6 - intentos_restantes])  # Seleccionar el muñeco de acuerdo con los intentos restantes

# Mostrar menú principal
def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Jugar")
    print("2. Puntajes")
    print("3. Salir")
    return input("Seleccione una opción: ")

# Jugar una partida
def jugar(palabras, puntajes):
    idioma = input("Seleccione el idioma (es/en): ").strip().lower()
    palabra_clave = "ES" if idioma == "es" else "EN"
    palabra_seleccionada = random.choice(palabras)[palabra_clave].lower()
    palabra_oculta = ["_" for _ in palabra_seleccionada]
    letras_usadas = set()
    intentos_restantes = 6
    puntaje = 0
    
    while intentos_restantes > 0 and "_" in palabra_oculta:
        print("\nPalabra:", " ".join(palabra_oculta))
        print("Letras usadas:", ", ".join(sorted(letras_usadas)))
        print("Intentos restantes:", intentos_restantes)
        mostrar_monigote(intentos_restantes)  # Mostrar la horca y el monigote
        
        letra = input("Introduce una letra: ").strip().lower()
        
        # Verificar que solo se ingrese una letra
        if len(letra) != 1 or not letra.isalpha():
            print("Por favor, ingresa solo una letra válida.")
            continue
        
        if letra in letras_usadas:
            print("¡Ya usaste esa letra! Intenta con otra.")
            continue
        
        letras_usadas.add(letra)
        
        if letra in palabra_seleccionada:
            print("¡Bien hecho! Adivinaste una letra.")
            for i, l in enumerate(palabra_seleccionada):
                if l == letra:
                    palabra_oculta[i] = letra
                    puntaje += 1
        else:
            print(f"Letra incorrecta. Te quedan {intentos_restantes - 1} intentos.")
            intentos_restantes -= 1
            mostrar_monigote(intentos_restantes)  # Solo mostrar monigote cuando haya un fallo
    
    if "_" not in palabra_oculta:
        print("¡Ganaste! La palabra era:", palabra_seleccionada, "y tu puntuación es:", puntaje * 2)
        puntaje += len(palabra_seleccionada)  # Aseguramos que el puntaje se sume al ganar
    else:
        print("¡Perdiste! La palabra era:", palabra_seleccionada)
    
    nombre = input("Introduce tu nombre: ").strip()
    puntajes.append({"nombre": nombre, "puntaje": puntaje, "palabra": palabra_seleccionada})
    
    # Ordenar puntajes de mayor a menor
    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)
    
    # Guardar solo los 5 mejores puntajes
    guardar_puntajes("Juego el ahorcado\\scores.json", puntajes_ordenados[:15])
    
    print("¡Puntaje guardado!")

# Mostrar mejores puntajes
def mostrar_puntajes(puntajes):
    print("\n--- Mejores Puntajes ---")
    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)[:5]
    for idx, score in enumerate(puntajes_ordenados, start=1):
        print(f"{idx}. {score['nombre']} - {score['puntaje']} puntos - Palabra: {score['palabra']}")

# Programa principal
def main():
    palabras = cargar_palabras("Juego el ahorcado\\data.json")
    puntajes = cargar_puntajes("Juego el ahorcado\\scores.json")
    
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            jugar(palabras, puntajes)
        elif opcion == "2":
            mostrar_puntajes(puntajes)
        elif opcion == "3":
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
