from collections import Counter
from itertools import product

# --- Funciones Auxiliares ---

# Esta función es clave para pedir números al usuario de forma segura.
# mensaje , es lo que le mostramos al usuario
#Single_input nos dice si esparmos 1 numero solo o varios separados por comas.
def solicitar_numeros(mensaje, single_input=False):
    while True: # Entramos en un bucle infinito hasta que la entrada sea válida.
        entrada = input(mensaje) # Pedimos al usuario que ingrese el número o números.
        try:
            if single_input: # Si esperamos un solo número (como un DNI o un año de nacimiento individual).
                numero = int(entrada.strip()) # Convertimos la entrada a un número entero, quitando espacios.
                # Aquí hay una validación específica para DNIs, común en Argentina.
                if "DNI" in mensaje and len(str(numero)) != 8:
                    print("Advertencia: Se espera un DNI de 8 dígitos. El ingresado no cumple.")
                return [numero] # Devolvemos el número dentro de una lista para uniformidad.
            else: # Si esperamos varios números separados por comas (como en el ejemplo original).
                numeros = [int(n.strip()) for n in entrada.split(',')] # Separamos por comas y convertimos cada uno a entero.
                if "DNI" in mensaje and any(len(str(n)) != 8 for n in numeros):
                    print("Advertencia: Se esperan DNIs de 8 dígitos. Algunos de los ingresados no cumplen.")
                return numeros # Devolvemos la lista de números.
        except ValueError: # Si el usuario ingresa algo que no es un número.
            print("Entrada inválida. Por favor, ingrese números válidos.") # informamos del error y el bucle continúa.

# Convierte cada número de DNI en un conjunto de sus dígitos únicos.
# Un conjunto es útil porque automáticamente elimina los dígitos repetidos.
def obtener_conjuntos_dni(dni):
    return [set(str(numero)) for numero in dni]

# --- Operaciones con Conjuntos (Dígitos de DNIs) ---

# Esta función realiza varias operaciones matemáticas con los conjuntos de dígitos de los DNIs.
def calcular_operaciones(conjuntos):
    if not conjuntos: # Si no hay datos, devolvemos conjuntos vacíos para evitar errores.
        return set(), set(), [], set()

    # La unión contiene todos los dígitos que aparecen en al menos uno de los DNIs.
    union = set.union(*conjuntos)  
    # La intersección contiene solo los dígitos que están presentes en *todos* los DNIs.
    interseccion = set.intersection(*conjuntos)  
    
    diferencias = []
    # Calculamos la diferencia entre conjuntos consecutivos.
    for i in range(len(conjuntos) - 1):
        diferencias.append(conjuntos[i] - conjuntos[i+1])
    
    # La diferencia simétrica muestra los dígitos que están en un conjunto o en otro, pero no en ambos.
    # Es como el 'O exclusivo'.
    diferencia_simetrica = conjuntos[0]
    for conjunto in conjuntos[1:]:  
        diferencia_simetrica = diferencia_simetrica.symmetric_difference(conjunto)
    
    return union, interseccion, diferencias, diferencia_simetrica

# --- Análisis de Dígitos y Sumas ---

# Cuenta la frecuencia de cada dígito y calcula la suma de los dígitos en cada DNI.
def contar_frecuencia_suma(dni):
    # 'Counter' de la colección 'collections' nos ayuda a contar la aparición de cada dígito.
    frecuencias = [Counter(str(numero)) for numero in dni]  
    # Sumamos cada dígito de cada DNI. Convertimos los dígitos a enteros antes de sumar.
    sumas = [sum(map(int, str(numero))) for numero in dni]  
    return frecuencias, sumas

# --- Evaluación de Condiciones Especiales de Dígitos ---

# Esta función analiza si hay patrones interesantes en los dígitos de los DNIs.
def evaluar_condiciones(conjuntos):
    if not conjuntos:
        print("No hay datos de DNI para evaluar condiciones.")
        return

    # Verificamos si hay dígitos que todos los DNI tienen en común.
    digitos_comunes = set.intersection(*conjuntos)  
    if digitos_comunes:
        print(f"Dígitos compartidos en todos los DNIs: {digitos_comunes}")
    else:
        print("No hay dígitos compartidos entre todos los DNIs.")
    
    # Una diversidad numérica alta significa que el DNI utiliza muchos dígitos diferentes.
    if any(len(conjunto) > 6 for conjunto in conjuntos):
        print("¡Atención! Algunos DNIs tienen una alta diversidad numérica (más de 6 dígitos únicos).")
    else:
        print("Ningún DNI presenta una diversidad numérica excepcionalmente alta (menos de 7 dígitos únicos por DNI).")

# --- Análisis de Años de Nacimiento ---

# Función para determinar si un año es bisiesto. Útil para análisis de fechas.
def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

# Esta función realiza diversos cálculos y análisis sobre los años de nacimiento.
def operaciones_con_años(años_nacimiento):
    if not años_nacimiento:
        print("No se ingresaron años de nacimiento para analizar.")
        return

    # Contamos cuántos años de nacimiento son pares y cuántos son impares.
    pares = sum(1 for año in años_nacimiento if año % 2 == 0)  
    impares = sum(1 for año in años_nacimiento if año % 2 != 0)  
    print(f"Cantidad de años pares: {pares}")
    print(f"Cantidad de años impares: {impares}")

    # Verificamos si todos los usuarios pertenecen a la "Generación Z" (nacidos después del 2000).
    if all(año > 2000 for año in años_nacimiento):
        print("Este es un Grupo Z: Todos los años de nacimiento son posteriores al 2000.")
    else:
        print("No todos los años de nacimiento son posteriores al 2000.")

    # Comprobamos si alguno de los años de nacimiento es bisiesto, lo que podría ser un "año especial".
    if any(es_bisiesto(año) for año in años_nacimiento):
        print("Tenemos un año especial: Al menos uno de los años de nacimiento es bisiesto.")
    else:
        print("Ninguno de los años de nacimiento es bisiesto.")

    # Calculamos la edad de cada persona basándonos en el año actual (establecido en 2025).
    año_actual = 2025 
    edades = [año_actual - año for año in años_nacimiento]
    print(f"Edades calculadas a partir del año {año_actual}: {edades}")

    # Generamos el producto cartesiano entre años y edades.
    # Esto empareja cada año con cada edad, mostrando todas las combinaciones posibles.
    producto_cartesiano = list(product(años_nacimiento, edades))
    print(f"Producto cartesiano (años y edades): {producto_cartesiano}")


# --- Bloque Principal de Ejecución del Programa con Menú Interactivo ---

# La función 'main' orquesta todo el flujo del programa.
def main():
    print("--- ¡Bienvenido al Analizador de Datos! ---")

    # Primero, preguntamos cuántos usuarios vamos a procesar.
    while True:
        try:
            num_usuarios = int(input("¿Cuántos usuarios desea ingresar? "))
            if num_usuarios > 0:
                break # Si el número es válido y positivo, salimos del bucle.
            else:
                print("Por favor, ingrese un número mayor a cero.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    # Creamos listas vacías para guardar los DNIs y años de nacimiento de todos los usuarios.
    all_dnis = []
    all_años_nacimiento = []

    # Iteramos para pedir los datos de cada usuario individualmente.
    for i in range(num_usuarios):
        print(f"\n--- Datos para el Usuario {i + 1} ---")
        # Usamos 'single_input=True' para pedir un solo DNI a la vez.
        dni_usuario = solicitar_numeros(f"Ingrese el DNI del usuario {i + 1}: ", single_input=True)
        # Y un solo año de nacimiento a la vez.
        año_nacimiento_usuario = solicitar_numeros(f"Ingrese el año de nacimiento del usuario {i + 1}: ", single_input=True)
        
        # Añadimos los datos de este usuario a nuestras listas generales.
        all_dnis.extend(dni_usuario)
        all_años_nacimiento.extend(año_nacimiento_usuario)

    # --- Procesamiento y Resultados de DNIs ---
    print("\n--- Resultados del Análisis de DNI ---")
    
    # Obtenemos los conjuntos de dígitos únicos de todos los DNIs ingresados.
    conjuntos_dni = obtener_conjuntos_dni(all_dnis)
    # Realizamos las operaciones de unión, intersección, diferencias y diferencia simétrica.
    union, interseccion, diferencias, dif_sim = calcular_operaciones(conjuntos_dni)
    # Contamos la frecuencia de cada dígito y la suma total de dígitos por DNI.
    frecuencia_digitos, suma_digitos = contar_frecuencia_suma(all_dnis)

    # Imprimimos todos los resultados de las operaciones con DNIs.
    print(f"Conjuntos de dígitos únicos de los DNIs: {conjuntos_dni}")
    print(f"Unión de todos los dígitos presentes en los DNIs: {union}")
    print(f"Dígitos comunes en todos los DNIs (Intersección): {interseccion}")
    print(f"Diferencias entre conjuntos de DNIs consecutivos: {diferencias}")
    print(f"Diferencia Simétrica de los dígitos entre todos los DNIs: {dif_sim}")
    print(f"Frecuencia de aparición de cada dígito por DNI: {frecuencia_digitos}")
    print(f"Suma total de los dígitos por cada DNI: {suma_digitos}")

    # Evaluamos condiciones especiales sobre los dígitos de los DNIs.
    evaluar_condiciones(conjuntos_dni)

    # --- Procesamiento y Resultados de Años de Nacimiento ---
    print("\n--- Resultados del Análisis de Años de Nacimiento ---")
    operaciones_con_años(all_años_nacimiento)

# Esta línea asegura que la función 'main' se ejecute solo cuando el script se inicia directamente.
if __name__ == "__main__":
    main()