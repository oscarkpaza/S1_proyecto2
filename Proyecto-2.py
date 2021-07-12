import csv
from os import closerange
import matplotlib.pyplot as plt

# FUNCIONES

# Devuelve una lista con los valores acumulados
def lista_acumulada(lista):
    acumulada = []
    for i in range(len(lista)):
        # Primer elemento de la lista
        if i == 0:
            acumulada.append(lista[i])
        # Todos los demas elementos
        else:
            acumulada.append(lista[i] + acumulada[i-1])
    return acumulada
        
# Muestra en pantalla un grafico acumulado de la region
def grafico_acumulado(codigo_region):
    # Se obtienen los datos de la region
    nombre_region = nombres_regiones[codigo_region]
    fechas_region = list(datos_regiones[codigo_region].keys())
    pcrs_fechas_region = list(datos_regiones[codigo_region].values())
    # Se obtiene una lista acumulada de los PCRs de la region
    pcrs_acumulados = lista_acumulada(pcrs_fechas_region)
    # Se prepara el grafico 
    plt.title('PCRs acumulados en ' + nombre_region)
    plt.plot(fechas_region, pcrs_acumulados) #(eje_x, eje_y)
    # Se muestra el grafico
    plt.show()

# Muestra en pantalla un grafico no acumulado de la region
def grafico_no_acumulado(codigo_region):
    # Se obtienen los datos de la region
    nombre_region = nombres_regiones[codigo_region]
    fechas_region = datos_regiones[codigo_region].keys()
    pcrs_fechas_region = datos_regiones[codigo_region].values()
    # Se prepara el grafico
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(fechas_region, pcrs_fechas_region) #(eje_x, eje_y)
    ax.set_title('PCRs por día en ' + nombre_region)
    # Se muestra el grafico
    plt.show()

# Se muestran los datos estadisticos y los graficos de la region que se seleccione
def ver_datos_por_region():
    region = ""
    while(region != "q"):
        print("\n")
        # Se imprimen las opciones
        for reg, cod in codigos_regiones.items():
            print(cod + " " + reg)
        print("q Volver") 
        region = input("Seleccione una opcion: ")
        if region == "q":
            break
        # Se Verifica si la region o codigo de region ingresado existe 
        elif list(codigos_regiones.keys()).count(region) == 0 and list(codigos_regiones.values()).count(region) == 0:
            print("Region invalida") 
        else:
            # Se obtiene el codigo de la region
            if list(codigos_regiones.values()).count(region) > 0:
                codigo_region = region
            elif list(codigos_regiones.keys()).count(region) > 0:
                codigo_region = codigos_regiones[region]

            nombre_region = nombres_regiones[codigo_region]
            datos_region = datos_regiones[codigo_region]
            pcrs_region = list(datos_region.values())
            # Se hace un analisis estadistico de los PCRs de la region
            min_pcr = min(pcrs_region)
            max_pcr = max(pcrs_region)
            total_pcr = sum(pcrs_region)
            prom_pcr = int(total_pcr/len(pcrs_region))
            print("\n" + nombre_region.upper())
            print("Cantidad minima de PCRs: " + str(min_pcr))
            print("Cantidad maxima de PCRs: " + str(max_pcr))
            print("Cantidad promedio de PCRs: " + str(prom_pcr))
            print("Cantidad total de PCRs: " + str(total_pcr))
            # Se muestran los graficos que se seleccione de la region
            grafico = ""
            while(grafico != "q"):
                print("\n1 Ver grafico PCRs no acumulados de " + nombre_region)
                print("2 Ver grafico PCRs acumulados de " + nombre_region)
                print("q Volver")
                grafico = input("Seleccione una opcion: ")
                if grafico == "1":
                    grafico_no_acumulado(codigo_region)
                elif grafico == "2":
                    grafico_acumulado(codigo_region)
                elif grafico != "q":
                    print("Opcion invalida!")

# Se muestran los datos de la mayor cantidad de PCRs acumulados y no acumulados
def ver_datos_mayor_PCR():
    max_pcr = 0
    max_pcr_region = ""
    max_pcr_fecha = ""
    max_pcr_acum = 0
    max_pcr_acum_region = ""
    # Se revisan todos los datos de las regiones
    for cod_region, datos_region in datos_regiones.items():
        # Se revisa los pcrs de cada region
        for fecha, n_pcrs in datos_region.items():
            if n_pcrs > max_pcr:
                max_pcr = n_pcrs
                max_pcr_region = nombres_regiones[cod_region]
                max_pcr_fecha = fecha
        # Se revisan los valores acumulados de PCRs de la region
        pcrs_acum = sum(list(datos_region.values()))
        if pcrs_acum > max_pcr_acum:
            max_pcr_acum = pcrs_acum
            max_pcr_acum_region = nombres_regiones[cod_region]
    # Se muestran los valores obtenidos
    print("\nMayor cantidad de PCRs")
    print("- Acumulados: " + max_pcr_acum_region + " con " + str(max_pcr_acum))
    print("- No acumulados: " + max_pcr_region + " con " + str(max_pcr) + " el dia " + max_pcr_fecha)
    
    
# Se muestran los datos de la menor cantidad de PCRs acumulados y no acumulados
def ver_datos_menor_PCR():
    min_pcr = 0
    min_pcr_region = ""
    min_pcr_fecha = ""
    min_pcr_acum = 0
    min_pcr_acum_region = ""
    # Se revisan todos los datos de las regiones
    for cod_region, datos_region in datos_regiones.items():
        # Se revisa los pcrs de cada region
        for fecha, n_pcrs in datos_region.items():
            if min_pcr_region == "" or n_pcrs < min_pcr:
                min_pcr = n_pcrs
                min_pcr_region = nombres_regiones[cod_region]
                min_pcr_fecha = fecha      
        # Se revisan los valores acumulados de PCRs de la region
        pcrs_acum = sum(list(datos_region.values()))
        if min_pcr_acum_region == "" or pcrs_acum < min_pcr_acum:
            min_pcr_acum = pcrs_acum
            min_pcr_acum_region = nombres_regiones[cod_region]
    print("\nMenor cantidad de PCRs")
    print("- Acumulados: " + min_pcr_acum_region + " con " + str(min_pcr_acum))
    print("- No acumulados: " + min_pcr_region + " con " + str(min_pcr) + " el dia " + min_pcr_fecha)     


# PROGRAMA

datos_regiones = {}     # { codigo_region: {fecha: cant_pcrs} }
codigos_regiones = {}   # { codigo_region: nombre_region }
nombres_regiones = {}   # { nombre_region: codigo_region }
fechas=[]               # lista con las ultimas 14 fechas del dataset
headers = True          # Se está leyendo el nombre de las columnas del dataset

# Se cargan los datos del dataset
print("Cargando datos...")
# Se abre y lee el archivo con los datos de PCR de cada region
with open('Datos_PCR.csv', 'r') as file:
    reader = csv.reader(file)
    # Se lee cada fila del archivo
    for row in reader:
        
        if headers:
            # Se obtienen las ultimas 14 fechas desde los nombres de las columnas
            for i in range(-1, -15, -1):
                fecha = row[i]
                fechas.append(fecha)
        # Datos de cada region
        else:
            datos_region = {}
            for fecha in fechas:
                datos_region[fecha] = 0
            # Se obtiene el nombre y codigo de cada region 
            region = row[0]
            codigo = row[1]
            codigos_regiones[region] = codigo
            nombres_regiones[codigo] = region
            # Se obtienen los pcrs de los ultimos 14 dias para una region
            for i in range(-1, -15, -1):
                n_pcrs = int(row[i])
                fecha = fechas[abs(i) - 1]
                datos_region[fecha] = n_pcrs
            datos_regiones[codigo] = datos_region
        headers = False
print("Datos cargados!\n")

# Comienza el programa para el usuario
opcion = ""
while(opcion != 'q'):
    print("\n1 Ver datos ultimas dos semanas por region")
    print("2 Ver region con mayor cantidad de examenes PCR realizados en las ultimas dos semanas")
    print("3 Ver region con menor cantidad de examenes PCR realizados en las ultimas dos semanas")
    print("q Salir")
    opcion = input("Seleccione una opcion: ").strip()
    if opcion == "1":
        ver_datos_por_region()
    elif opcion == "2":
        ver_datos_mayor_PCR()
    elif opcion == "3":
        ver_datos_menor_PCR()

    elif opcion != "q":
        print("Opcion invalida!")
