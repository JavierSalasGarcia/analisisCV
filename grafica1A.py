import scipy.io
import os
import chardet
import matplotlib.pyplot as plt

def suavizar(estimulo, tamanio_ventana=200):
  # Crear una lista para almacenar el vector suavizado
  estimulo_suavizado = []
  
  # Recorrer la lista de estimulo
  for i in range(len(estimulo)):
    # Calcular el promedio de los tamanio_ventana elementos anteriores y posteriores al elemento actual
    promedio = sum(estimulo[max(0, i-tamanio_ventana):min(len(estimulo), i+tamanio_ventana+1)]) / (2*tamanio_ventana+1)
    # Añadir el promedio a la lista de estimulo_suavizado
    estimulo_suavizado.append(promedio)
    
  # Devolver el vector suavizado
  return estimulo_suavizado

def integral(Ewe, minimos):
  # Crear una lista para almacenar las integrales
  Integrales = []
  
  # Recorrer la lista de mínimos locales
  for i in range(len(minimos)-1):
    # Calcular el área bajo la curva entre el mínimo local actual y el siguiente
    area = sum(Ewe[minimos[i]:minimos[i+1]])
    # Añadir el área a la lista de integrales
    Integrales.append(area)
    
  # Devolver la lista de integrales
  return Integrales

# Función para encontrar los mínimos locales en una lista
def minimos_locales(estimulo):
    # Crear una lista para almacenar los mínimos locales
    minimos = []
    # Recorrer la lista de estimulo
    i = 100
    while i < len(estimulo) - 100:
        # Si el valor actual es un mínimo local, añadirlo a la lista de mínimos
        if estimulo[i] < estimulo[i-100] and estimulo[i] < estimulo[i+100]:
            minimos.append(i)
            i = i + 1000
        else:
            i = i + 1
    # Devolver la lista de mínimos locales
    return minimos

# Obtiene la lista de archivos en la carpeta "pruebas"
files = os.listdir("pruebas")

# Muestra la lista de archivos al usuario y le permite seleccionar uno
print("Selecciona un archivo:")
for i, file in enumerate(files):
    print("{}. {}".format(i + 1, file))

selected = int(input())

# Obtiene el nombre del archivo seleccionado
filename = files[selected - 1]

# Especifica el número de línea a partir de la cual se deben leer las líneas del archivo
n = 56

# Abre el archivo en modo lectura
with open("pruebas/{}".format(filename), "r", encoding="ISO-8859-1") as f:
    # Lee las líneas del archivo
    lines = f.readlines()
    # Toma las líneas a partir de la línea n
    lines = lines[n:]
    values =[]
    # itera sobre las líneas
    for line in lines:
        row = line.split("\t")
        # Itera sobre la lista
        float_lst = [float(item) for item in row]
        values.append(float_lst)

# Crea un diccionario con la matriz que quieres guardar
data = {"matrix": values}

# Guarda la matriz en un archivo con extensión .mat
scipy.io.savemat("datos.mat", data)

# Calcula la carga (integral de I en mA por tiempo en s)
tiempo = [row[5] for row in values]
Ewe = [row[7] for row in values]
ImA = [row[8] for row in values]
Ewe_absoluto = [abs(x) for x in Ewe]
estimulo = Ewe
estimulo_suavizado = suavizar(estimulo, tamanio_ventana=200)

# Encontrar los mínimos locales en la lista de estimulo
minimos = minimos_locales(estimulo_suavizado)
minimosC = [x - 50 for x in minimos]

# Calcular las integrales entre los mínimos locales en la lista de Ewe
Integrales = integral(Ewe, minimos)
IntegralesAbs = integral(Ewe_absoluto, minimos)

# Crea una figura con 3 gráficas verticalmente
fig, ax = plt.subplots(3,1)
fig.set_size_inches(6, 8)

fig.subplots_adjust(hspace=0.526)
# Grafica la columna 8 versus la columna 9 en la primera gráfica
ax[0].plot(Ewe, ImA)
ax[0].set_xlabel("Ewe, V")
ax[0].set_ylabel("I, mA")

subcadenas = filename.split("_")
titulo = subcadenas[0]
cadena = subcadenas[2]
subcadenas = cadena.split(".")

sal = subcadenas[0]
ax[0].set_title(titulo + ". Electrolito: " + sal, size=10)

# Grafica Ewe vs tiempo
ax[1].plot(tiempo, estimulo)
ax[1].set_xlabel("tiempo, s")
ax[1].set_ylabel("Ewe, V")

# Grafica Ima vs tiempo en dos colores. Rojo positivos, azul negativos
ax[2].fill_between(tiempo, ImA, 0, where=[x > 0 for x in ImA], color='red')
ax[2].fill_between(tiempo, ImA, 0, where=[x < 0 for x in ImA], color='blue')
ax[2].set_xlabel("tiempo, s")
ax[2].set_ylabel("I, mA")

j=0
for i in minimos:
  # Escribir texto  en la gráfica en la coordenada x = tiempo[i]
  if j > 0 and j<len(minimos)-1:
    ax[1].text(tiempo[i], -1, "  ciclo " + str(j), fontsize=6)
  if j > 0 and j<len(minimos):
    ax[1].axvline(tiempo[i], color='k', linestyle='--', linewidth=1)
  j=j+1
j =0

# Integral total de cada ciclo 
Integrales_redondeada = [round(x, 1) for x in Integrales]

# Integral de los semiciclos positivos (oxidación)
Integrales_oxid = [x - ((x-y)/2) for x, y in zip(IntegralesAbs, Integrales)]
Integrales_oxid_redondeada = [round(x, 1) for x in Integrales_oxid]

# Integral de los semiciclos negativos (reducción) 
Integrales_redu = [(x - y)/2 for x, y in zip(IntegralesAbs, Integrales)]
Integrales_redu_redondeada = [round(x, 1) for x in Integrales_redu]

print (Integrales_redondeada)
print (Integrales_oxid_redondeada)
print (Integrales_redu_redondeada)

j=1
# Calcular el promedio de las integrales de los ciclos 
# intermedios para añadirlos a resultados.txt
sumaT = 0
sumaO = 0
sumaR = 0
for i in minimos:
    suma =0
  # Escribir lineas verticales en la coordenada x = tiempo[i] 
    if j < len(minimos)-1:
        sumaT= Integrales[j]+sumaT
        sumaO= Integrales_oxid[j]+sumaO
        sumaR= Integrales_redu[j]+sumaR
    j=j+1
promedioT = sumaT/(j-3)
promedioO = sumaO/(j-3)
promedioR = sumaR/(j-3)

j=0
for i in minimos:
  # Escribir lineas verticales en la coordenada x = tiempo[i] 
    if j < len(minimos):
        ax[2].axvline(tiempo[i], color='k', linestyle='--', linewidth=1)
    if j < len(minimos)-1:
        ax[2].text(tiempo[i], 0.1, Integrales_redondeada[j], fontsize=6)
    j=j+1
j =0

for i in minimos:
  # Escribir Integral de oxidación en la coordenada x = tiempo[i] 
    if j < len(minimos)-1:
        ax[2].text(tiempo[i], -0.1, Integrales_oxid_redondeada[j], fontsize=6, color='red')
    j=j+1

j=0

for i in minimos:
  # Escribir Integral de reducción en la coordenada x = tiempo[i] 
    if j < len(minimos)-1:
        ax[2].text(tiempo[i], -0.2, Integrales_redu_redondeada[j], fontsize=6, color='blue')
    j=j+1

with open("pruebas/{}".format(filename), "r", encoding="ISO-8859-1") as f:
    # Lee todas las líneas del archivo
    lines = f.readlines()


# Lista con los índices de las líneas a extraer
# Ei (V) línea 33, V
# dE/dt línea 35,  mV/s
# E1  línea 37, V
# E2  línea 48, V

line_indices = [33, 35, 37, 48, 50] 

# Lista para guardar las leyendas
leyendas = []
parametros = ['Ei', 'dE/dt', 'E1', 'E2', 'ciclos']
unidades = [' V', ' mV/s', ' V', ' V', '']
# Itera sobre los índices de las líneas
for n in line_indices:
    # Accede a la línea n
    line = lines[n-1]
    # Divide la línea por espacios en blanco
    parts = line.split()
    # Guarda la última parte de la línea (la leyenda) en la lista
    leyendas.append(parts[-1])

# print (leyendas)
# Genera la lista de anotaciones
anotar = [f"{parametro} = {leyenda}{unidad}" for leyenda, parametro, unidad in zip(leyendas, parametros, unidades)]

leyendas_str = ",".join(leyendas)
leyendas_str = titulo + "," + sal + "," + leyendas_str + "," + str(promedioT) + "," + str(promedioO)+ "," + str(promedioR)

# Abre el archivo en modo a (para añadir al final del archivo)
with open("resultados.txt", "a") as f:
    # Escribe la nueva línea en el archivo
    f.write(leyendas_str + "\n")

x= 0
y = 0.04
for i, elemento in enumerate(anotar):
    # Coloca los parámetros, valores y unidades como anotación en la gráfica
    y = y-0.04
    ax[0].text(x, y, elemento, fontsize=7)

# Guarda la figura como imagen en formato JPG
fig.savefig("graficas/" +titulo + "_" + sal +".jpg", dpi=300)