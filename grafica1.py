import scipy.io
import os
import chardet
import matplotlib.pyplot as plt

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



# Crea una figura con 3 gráficas verticalmente
fig, ax = plt.subplots()
fig.subplots_adjust(hspace=0.526)
# Grafica la columna 8 versus la columna 9 en la primera gráfica
ax.plot([row[7] for row in values], [row[8] for row in values])
ax.set_xlabel("Ewe, V")
ax.set_ylabel("I, mA")

subcadenas = filename.split("_")
titulo = subcadenas[0]

cadena = subcadenas[2]

subcadenas = cadena.split(".")

# Tomar el primer elemento de la lista
sal = subcadenas[0]

ax.set_title(titulo + ". Electrolito: " + sal)

# Muestra la gráfica
# plt.show()





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
leyendas_str = titulo + "," + sal + "," + leyendas_str

# Abre el archivo en modo a (para añadir al final del archivo)
with open("resultados.txt", "a") as f:
    # Escribe la nueva línea en el archivo
    f.write(leyendas_str + "\n")


x= 0
y = 0.04

# Itera sobre los elementos de la lista
for i, elemento in enumerate(anotar):
    # Coloca el elemento como anotación en la gráfica
    y = y-0.04
    ax.text(x, y, elemento)

# Guarda la figura como imagen en formato JPG

fig.savefig("graficas/" +titulo + "_" + sal +".jpg", dpi=300)
