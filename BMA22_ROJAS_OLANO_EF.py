""" PROGRAMA: Simulador de Demanda y Reabastecimiento de una Farmacia

El siguiente programa modela la compra de 3 diferentes tipos de medicamentos los
cuales siguen una distribución de Poisson cada uno. Y con cadenas de Markov se
analiza las probabilidades de no tener existencias dentro de los próximos 7 días
"""
# IMPORTACIÓN DE LIBRERÍAS:
import time
import random
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from scipy.stats import poisson
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# DEFINICIÓN DE PARÁMETROS
N = 200     # Existencias máximas por medicamento
dias = 7    # Días de análisis
C_M = []    # Lista de Cadenas de Markov para cada medicamento
M_pos = []     # Lista para almacenar las potencias de cada matriz C_M[i]
lam_i = [25, 38, 50]     # Medias de Poisson para cada medicamento
del_ac = [0,0,0.05, 0.15, 0.50, 0.80, 1]    # Probabilidades acumuladas de entrega



#--------------------------------FUNCIONES I: LÓGICA DEL PROGRAMA--------------------------------------

# FUNCIÓN 1: GENERADOR DE LAS MATRICES DE MARKOV PARA CADA MEDICAMENTO
def gen_M(N,lam_i):
    for k in range(len(lam_i)): # Iterador para cada medicamento
        M = np.zeros((N + 2, N + 2)) # Matriz de ceros base
        for i in range(N+2): # Generador de cada matriz
            for j in range(N+2):
                if (i > j):  # No es posible que el inventario aumente sin solicitar reabastecimiento
                    M[i,j] = 0
                elif (j == N + 1): # Estado de pérdida de clientes
                    M[i,j] = 1 - poisson.cdf(N-i,lam_i[k])
                else: # Probabilidad de transicionar a cada estado con menor inventario
                    M[i,j] = poisson.pmf(j-i, lam_i[k])
        C_M.append(M)  # Guardar la matriz de Markov para cada medicamento


# FUNCIÓN 2: POTENCIAS DE MATRICES
def M_temp(C_M, dias):
    for M_i in C_M:  # Recorrer cada Matriz de Markov de cada medicamento
        M_dias = []  # Lista para almacenar las potencias de la Cadena de Markov de cada medicamento
        for p in range(1, dias + 1):  # Recorrer los días 
            A = np.linalg.matrix_power(M_i, p)  # Función para elevar una matriz a una potencia
            M_dias.append(A)  # Agregar la matriz resultante a la lista
        M_pos.append(M_dias)  # Agregar la lista de potencias a la lista principal


# FUNCIÓN 3: BUSCAR LA MATRIZ QUE CUMPLE LA CONDICIÓN
""" La siguiente función busca a partir de qué día la probabilidad de encontrarse
 en los estados de stock 0, o de pérdida de clientes aumenta por encima del 15 % """
def buscar(M_pos, inven_new, N):
    posiciones = []  # Vector para almacenar las posiciones encontradas
    for i in range(len(M_pos)):  # Recorrer las 3 listas en M_pos
        encontrado = False  # Bandera para saber si encontramos una posición
        for j, M in enumerate(M_pos[i]):  # Recorrer las 7 matrices de la lista i
            if (M[N - inven_new[i], N]+M[N - inven_new[i], N+1])*(1-del_ac[j]) > 0.15:  # Verificar condición
                posiciones.append(j + 1)  # Guardar posición (contando desde 1)
                encontrado = True
                break  # Salir del bucle cuando se encuentra la primera coincidencia
        if not encontrado:  
            posiciones.append(-1)  # Guardar -1 si no se encontró ninguna
    return posiciones  # Devolver el vector de posiciones


# FUNCIÓN 4: DISTRIBUCIÓN DEL DELIVERY
def random_delivery_day():
    dias = [3, 4, 5, 6, 7]   # Días en los que puede llegar el pedido
    probabilidades = [0.05, 0.10, 0.35, 0.30, 0.20]   # Distribución de Probabilidades
    return random.choices(dias, weights=probabilidades, k=1)[0] #Retorna un día aleatorio


#-----------------------------FUNCIONES 2: SIMULACIÓN Y VISUALIZACIÓN---------------------------------

# FUNCIÓN 5: VISUALIZAR LAS CADENAS DE MARKOV
def visual(M_pos):
    time.sleep(10)
    def plot_2d_matrix(matrix, med_name, day_name):
        fig, ax = plt.subplots(figsize=(7, 7))
        norm = mcolors.PowerNorm(gamma=0.1, vmin=0, vmax=1)  # Normalización con gamma extremadamente baja  

        cax = ax.imshow(matrix, cmap='plasma', norm=norm, interpolation='nearest') # Paleta "plasma"
        plt.colorbar(cax, label='Probabilidad')

        ax.set_xticks(np.arange(0, matrix.shape[1], step=20))     # Ajustar ejes para que comiencen en 200
        ax.set_yticks(np.arange(0, matrix.shape[0], step=20))
        ax.set_xticklabels(reversed(range(0, matrix.shape[1], 20)))  # Decreciente en X
        ax.set_yticklabels(reversed(range(0, matrix.shape[0], 20)))  # Decreciente en Y
        ax.set_xlabel('Índice X')
        ax.set_ylabel('Índice Y')
                # Título dinámico con medicamento y día
        ax.set_title(f'Mapa de Calor de Probabilidades\n{med_name} - {day_name}')
        plt.show()
    root = tk.Tk()
    root.title("Selector de Medicamento y Día")
    tk.Label(root, text="Selecciona Medicamento:").pack()
    med_var = tk.StringVar()
    med_selector = ttk.Combobox(root, textvariable=med_var)
    med_selector['values'] = [f"Medicamento {i+1}" for i in range(len(M_pos))]
    med_selector.pack()
    
    tk.Label(root, text="Selecciona Día:").pack()
    dia_var = tk.StringVar()
    dia_selector = ttk.Combobox(root, textvariable=dia_var)
    dia_selector['values'] = [f"Día {i+1}" for i in range(len(M_pos[0]))]
    dia_selector.pack()

    def actualizar():
        med_index = med_selector.current()
        dia_index = dia_selector.current()
        if med_index != -1 and dia_index != -1:
            matrix = np.array(M_pos[med_index][dia_index])
            med_name = med_selector.get()
            day_name = dia_selector.get()
            plot_2d_matrix(matrix, med_name, day_name)
    
    boton = tk.Button(root, text="Mostrar Gráfico", command=actualizar)
    boton.pack()
    root.mainloop()


# FUNCIÓN 6: SIMULACIÓN DE CONSUMO Y REPOSICIÓN
def simular():
    gen_M(N,lam_i)
    M_temp(C_M, dias)
    inventario = np.full(len(lam_i), N)
    dias_restantes_pedido = np.zeros(len(lam_i), dtype=int)
    while True:
        print("Inventario inicial:  ", inventario)
        consumo_diario = np.array([poisson.rvs(lam) for lam in lam_i])  # Generar consumo diario
        inventario -= consumo_diario   # Restar consumo al inventario (evitando negativos)
        inventario = np.maximum(inventario, 0)
        
        print("Consumo diario:      ", consumo_diario)
        print("Inventario final:    ", inventario)
    
        pos = buscar(M_pos, inventario, N)  # Buscar cuándo se quedarán sin stock
        print("Posiciones de agotamiento: ", pos)
        
        for i in range(len(lam_i)):   # Gestionar pedidos
            if pos[i] != -1 and dias_restantes_pedido[i] == 0:
                dias_restantes_pedido[i] = random_delivery_day()
                print(f"Pedido realizado para medicamento {i+1}")
        
        for i in range(len(lam_i)):   # Reducir los días restantes para que llegue el pedido
            if dias_restantes_pedido[i] > 0:
                dias_restantes_pedido[i] -= 1
                if dias_restantes_pedido[i] == 0:
                    inventario[i] = 200  # Reabastecer
                    print(f"Pedido recibido para medicamento {i+1}, inventario restaurado a 200")
        print("-------------------------------")
        time.sleep(10)         # Esperar 10 segundos antes de pasar al siguiente día



#---------------------------------EJECUCIÓN DEL PROGRAMA-----------------------------------

hilo_simular = threading.Thread(target=simular) # Ejecutar la simulación en paralelo
hilo_simular.start() # Empezar simulación
visual(M_pos) # Ejecutar la visualización en paralelo