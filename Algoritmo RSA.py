# IMPORTACIÓN DE LIBRERÍAS
import math
import random # Librería para números aleatorios
import time # Librería para medir tiempos

#.............ETAPA 1 - BUSCAR DOS NÚMEROS PRIMOS DE 17 DÍGITOS..................

# FUNCIÓN 1: PRUEBA DE PRIMALIDAD
def primalidad(n): # Algoritmo basado en la criba de Eratóstenes
    if n % 3 == 0: # Se llama a primalidad(n) si n es impar
        return False # La función devuelve False si n NO es primo
    """Trial Division Algorithm: Si n es un número compuesto,
    tiene al menos un factor primo <= sqrt(n)
    
    Se verifican solo las secuencias 5,11,17,23 y 7,13,19,25 para
    evitar redundancia con múltiplos de 2 y de 3, ambas secuencias 
    se incrementan de 6 en 6."""
    i = 5 # Divisores empiezan la secuencia en 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True # Se retorna True si n es primo


# FUNCIÓN 2: BUSCADOR DE NÚMEROS PRIMOS
def buscador(n):
    if n%2==0: # Si n es par, se descarta
        n=n+1 
    while not primalidad(n):
        n += 2 # Solo los impares son candidatos
    return n

# FUNCIÓN 3: GENERADOR DE NÚMEROS PRIMOS
def generadorP(ran):
    return buscador(ran)  # Usando la función buscador

#.................ETAPA 2: GENERACIÓN DE LA CLAVE PÚBLICA "e" ....................

# FUNCIÓN 4: ALGORITMO DE EUCLIDES - HALLAR MCD
def gcd(a, b): # MCD - Algoritmo de Euclides
    while b:
        a, b = b, a % b
    return a
# FUNCIÓN 5: BUSCADOR DE POSIBLES CLAVES PÚBLICAS
def encontrar_e(totient): 
    e = 65537  # Comenzamos a buscar a partir de 65537 - RECOMENDADO
    while gcd(e, totient) != 1:  # Aseguramos que e sea primo y coprimo con totiente(n)
        e = buscador(e)
    return e

#.................ETAPA 3: GENERACIÓN DE LA CLAVE PÚBLICA "d" ...................

# FUNCIÓN 6: ALGORITMO DE EUCLIDES EXTENDIDO
def euclides_extendido(a, b):
    # Este algoritmo devuelve (gcd, x, y) tal que: a*x + b*y = gcd(a, b)
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = euclides_extendido(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

# FUNCIÓN 7: BUSCADOR DE LA CLAVE PRIVADA EN mod(totiente[n])
def encontrar_d(e, totient):
    gcd, x, y = euclides_extendido(e, totient) # Solución a e*d ≡ 1 mod (totient[n])
    d = x % totient  # El valor de d es el valor de x mod phi(n)
    return d

#.................ETAPA 4: ALGORITMOS DE VALIDACIÓN..........

# FUNCIÓN 8: ALGORITMO DE EXPONENCIACIÓN MODULAR RÁPIDA BINARIA
def fme(base, exponente, mod):
    resultado = 1
    base = base % mod  
    while exponente > 0:
        if exponente % 2 == 1:  
            resultado = (resultado * base) % mod
        base = (base * base) % mod
        exponente = exponente // 2  
    return resultado

# FUNCIÓN 9: DE TEXTO A DECIMAL
def texto_a_decimal(mensaje): 
    """ Convierte un mensaje en su representación binaria completa y devuelve su equivalente decimal. """
    binario = ''.join(f'{ord(c):08b}' for c in mensaje)  # Convertir cada caracter a binario de 8 bits
    return int(binario, 2)  # Convertir la cadena binaria a un número decimal

#FUNCIÓN 10: DE DECIMAL A TEXTO
def decimal_a_texto(numero):
    """Convierte un número decimal en texto ASCII, reemplazando bytes inválidos con 'X'."""
    longitud = (numero.bit_length() + 7) // 8  # Calcular cuántos bytes se necesitan
    bytes_numero = numero.to_bytes(longitud, 'big')  # Convertir a bytes
    texto = '' # Intentar decodificar cada byte individualmente
    for byte in bytes_numero:
        try:
            char = bytes([byte]).decode('utf-8')  # Decodificar solo un byte
            texto += char if char.isprintable() else 'X'  # Sustituir si no es imprimible
        except UnicodeDecodeError:
            texto += 'X'  # Si el byte no es válido, reemplazar con 'X'
    return texto

# FUNCIÓN 11: GENERADOR DE CLAVES PÚBLICA Y PRIVADA
def generador_claves():
    t_inicial = time.time() # Tiempo inicial
    # Semillas distintas dentro del rango permitido
    seed1 = random.randint(10**16, 10**17 - 9)
    seed2 = random.randint(10**16, 10**17 - 9)
    while seed1 == seed2:
        seed2 = random.randint(10**16, 10**17 - 9) # Se buscan semillas distintas
    # Generar dos números primos distintos
    primo1 = generadorP(seed1)
    primo2 = generadorP(seed2)

    # Calcular tiempo transcurrido
    t_final = time.time() #Tiempo final
    t_transcurrido = t_final - t_inicial #Tiempo Transcurrido
    # Información Desplegada
    print("Primo 1 (p): ", primo1)
    print("Primo 2 (q): ", primo2)
    print(f"\t\tTiempo de ejecución para obtener p y q: {t_transcurrido:.4f} segundos")

    t_inicial = time.time() # Tiempo inicial
    num=primo1*primo2 #Determinar n
    totient=(primo1-1)*(primo2-1) # Determinar la Función Totitente
    e = encontrar_e(totient) # Determinar la clave pública
    #Información Desplegada
    print("Claves públicas\nn:", num)
    print("e:",e)

    d = encontrar_d(e, totient) # Algoritmo de Euclides Extendidos para hallar d
    t_final = time.time() #Tiempo final
    t_transcurrido = t_final - t_inicial #Tiempo Transcurrido
    #Información Desplegada
    print(f"Claves privadas\nphi(n):",totient)
    print(f"d:     ", d)
    print(f"\t\tTiempo de ejecución para obtener las claves: {t_transcurrido:.5f} segundos")
    return num,e,d

#----------FUNCIONES INTERACTIVAS: NO FORMAN PARTE DE LA LÓGICA DEL PROGRAMA----------------------
"""Las siguientes funciones solo tienen la finalidad de contextualizar el uso de
encriptación de clave pública y privada, no se utilizan conceptos del curso como tal,
por ello a partir de aquí se puede saltar directamente a las últimas dos líneas que 
ejecutan el programa :)"""

# GENERAR MATRIZ DEL USUARIO
def generar_matriz():
    personas = ["Edward", "Rojas"], ["David", "Bowie"], ["Jack", "Nicholson"]
    matriz = []
    n_existentes = set()
    
    for nombre, apellido in personas:
        while True:
            print("Claves pública y privada de: ",nombre,"\n")
            n, e, d = generador_claves()
            print("\n\n")
            if n not in n_existentes:
                n_existentes.add(n)
                matriz.append([nombre, apellido, n, e, d])
                break
    return matriz

# GENERAR LA FIRMA DE UN USUARIO
def firmar_como(usuarios):
    while True:
        print("FIRMA DIGITAL:")
        for i, usuario in enumerate(usuarios, start=1):
            print(f"{i}. {usuario[0]}")
        
        try:
            opcion = int(input("Generar una firma digital como: "))
            if 1 <= opcion <= len(usuarios):
                break
        except ValueError:
            pass  # Ignorar entrada inválida y seguir pidiendo
        print("Entrada inválida. Intente nuevamente.")
    
    nombre, apellido, n, e, d = usuarios[opcion - 1]
    
    texto = input("Ingrese su texto: ")
    firma = f"{nombre[0]}.{apellido}"
    autent=fme(texto_a_decimal(firma),d,n)
    print("\n\n\t\tDOCUMENTO GENERADO\n\n",f"{texto}\n{autent}")
    return f"{texto}\n{autent}"

# LEER EL DOCUMENTO COMO UN USUARIO
def leer_como(usuarios, texto):
    u0=usuarios
    t0=texto
    while True:
        print("\nLECTURA DE DOCUMENTO:")
        for i, usuario in enumerate(usuarios, start=1):
            print(f"{i}. {usuario[0]}")
        print("Presione (S) para salir")
        opcion = input("Leer el siguiente documento con la clave pública de: ")
        if opcion.lower() == 's':  # Si el usuario presiona 's' o 'S', salir del programa
            print("Saliendo del programa...")
            exit()
        try:
            opcion = int(opcion)
            if 1 <= opcion <= len(usuarios):
                break
        except ValueError:
            pass  # Ignorar entrada inválida y seguir pidiendo
        print("Entrada inválida. Intente nuevamente.")
    
    nombre, apellido, n, e, d = usuarios[opcion - 1]
    
    # Extraer el fragmento numérico del texto
    partes = texto.rsplit('\n', 1)  # Dividir por el último salto de línea
    if len(partes) > 1:
        texto, numero_str = partes
        try:
            numero = int(numero_str)  # Convertir a número
        except ValueError:
            print("Error: el fragmento extraído no es un número válido.")
            return
    else:
        print("Error: No se encontró un número en el texto.")
        return
    
    texto += f"\n{decimal_a_texto(fme(numero,e,n))}"
    print("\n",texto)
    while True:
        salir = input("\nPresione 'S' para salir: ")
        if salir.lower() == 's':
            return leer_como(u0, t0)  # Permite volver a leer como otra persona


#-----------------------EJECUCIÓN DEL PROGRAMA---------------------------

usuarios=generar_matriz()
print(leer_como(usuarios,firmar_como(usuarios)))