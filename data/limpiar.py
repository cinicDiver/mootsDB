import pandas as pd
import datetime as dt
import locale
import re

locale.setlocale(locale.LC_TIME,"es_ES")
hoy=dt.datetime.today()

hoja=pd.read_excel("encabezados.xlsx")
df=pd.DataFrame(hoja.values)
df.columns=df.iloc[0,:]
df.drop(df.index[0],inplace=True)
df.drop(df.columns[[0]],axis=1,inplace=True)
act=[ [] for _ in range(len(df.columns.tolist()))]
rost=41
# ====================
# REVISANDO DATOS1.CSV
# ====================
fhand=open("datos1.csv")
print("Abriendo datos1.csv")
heads=None
filas=[]
for line in fhand:
    if heads is None:
        line=line.lower().split(";")
        heads=line[:-1]
        continue
    line=line.strip()
    fil=line.split(";")
    filas.append(fil[:-1])
fhand.close()
noNum=-2
for fila in filas:
    # Nombres y apellidos
    nomsap=fila[1].strip().split(" ")
    if len(nomsap)==3:
        act[1].append(nomsap[0])
        act[2].append("{} {}".format(nomsap[1],nomsap[2]))
    elif len(nomsap)==4:
        act[1].append("{} {}".format(nomsap[0],nomsap[1]))
        act[2].append("{} {}".format(nomsap[2],nomsap[3]))
    else:
        print("Los datos de {} no se pudieron agregar a la matriz en la limpiada de datos1.csv".format(fila[1]))
        continue
    print("Adicionando datos a:", fila[1].strip())
    # Numero
    if fila[0]!="":
        act[0].append(int(fila[0]))
    else:
        act[0].append(noNum)
        noNum-=1
     # Correo
    act[3].append(fila[2])
    # Nacimiento
    act[4].append(dt.datetime.strptime(fila[3].strip(),"%d/%m/%Y").date())
    # Celular
    act[5].append(int(fila[4]))
    # Documento
    act[6].append(fila[8])
    # nDoc
    act[7].append(int(fila[9]))
    # Pasaporte
    if fila[10]=="SI":
        act[8].append(1)
    else:
        act[8].append(0)
    # amVisa
    if fila[11]=="SI":
        act[10].append(1)
    else:
        act[10].append(0)
    # apodo
    if fila[13]=="":
        act[11].append("No aplica")
    else:
        act[11].append(fila[13])
    # aIngreso
    act[12].append(int(fila[14]))
    # alimentacion
    if fila[15]=="NO":
        act[13].append(0)
    else:
        act[13].append(1)
    # activo
    act[14].append(1)
    # direccion
    act[18].append(fila[5])
    # seleCol
    if fila[16]=="NO":
        act[26].append(0)
        act[27].append("No aplica")
    else:
        act[26].append(1)
        act[27].append(fila[16])
    # Eps
    act[38].append(fila[12].lower().capitalize().strip())
    # ciudadR
    act[39].append(fila[6].strip())
    # ciudadN
    act[40].append(fila[7].strip())
dfHeads=df.columns.tolist()
print(len(dfHeads),len(act))
for i in range(0,len(act)):
    if len(act[i])!=rost:
        print("No se pudo actualizar:",dfHeads[i])
        continue
    if len(act[i])>1:
        df[dfHeads[i]]=act[i]
print("=======================================================================")
print("Titulos de datos1.csv:",heads)
# ====================
# REVISANDO DATOS2.CSV
# ====================
fhand=open("datos2.csv")
print("Abriendo datos2.csv")
heads=None
filas=[]
for line in fhand:
    if heads is None:
        line=line.lower().split(";")
        heads=line
        continue
    line=line.strip()
    fil=line.split(";")
    filas.append(fil)
# Revisar copias
borrar=[]
print()
for i in range(0,len(filas)):
    copias=[]
    if len(filas[i][0])<1:continue
    actual=dt.datetime.strptime(filas[i][0].strip(),"%m/%d/%Y %H:%M:%S")
    for j in range(0,len(filas)):
        if len(filas[i][6])<1 or len(filas[j][6])<1:continue
        if int(filas[i][6])==int(filas[j][6]):
            revi=dt.datetime.strptime(filas[j][0].strip(),"%m/%d/%Y %H:%M:%S")
            copias.append((j,revi))
    copias.sort(reverse=True)
    copias.pop(0)
    for copia in copias:
        if copia[0] not in borrar:
            borrar.append(copia[0])
borrar.sort(reverse=True)
for num in borrar:
    filas.pop(num)
for i in range(0,rost):
    for fila in filas:
        if len(fila[6])<1:continue
        if int(fila[6])!=act[7][i]:continue
        print("Adicionando datos a:", act[1][i],act[2][i])
        # barrio
        act[17].append(fila[16].lower().capitalize())
        # talla
        if len(fila[9])<1:
            act[19].append(-1.0)
        elif float(fila[9])>100:
            act[19].append(float(fila[9])/100)
        else:
            act[19].append(float(fila[9]))
        # peso
        if len(fila[10])<1:
            act[20].append(-1.0)
        else:
            act[20].append(float(fila[10]))
        # enfermo y enfermedad
        if len(fila[19])<1:
            act[21].append(0)
            act[22].append("No aplica")
        else:
            act[21].append(1)
            act[22].append(fila[19])
        # pos
        pos=fila[11].split(" ")
        act[33].append(pos[0].capitalize())
        # otros
        if len(fila[23])<1:
            act[34].append("No aplica")
            act[35].append(0)
        else:
            act[34].append(fila[23])
            try:
                svar=re.search("([0-9]*)",fila[24])
                hrs=int(svar)
                act[35].append(hrs)
            except:
                act[35].append(-1)
        # concatcto y nContacto
        if len(fila[18])<7:
            act[42].append("-")
            act[43].append(-1)
        else:
            act[42].append(fila[17].lower())
            act[43].append(int(fila[18]))
dfHeads=df.columns.tolist()
print(len(dfHeads),len(act))
for i in range(0,len(act)):
    if len(act[i])!=rost:
        print("No se pudo actualizar:",dfHeads[i])
        print(act[i])
        continue
    if len(act[i])>1:
        df[dfHeads[i]]=act[i]
print("=======================================================================")
print("Titulos de datos2.csv:",heads)
# ====================
# REVISANDO DATOS3.CSV
# ====================
fhand=open("datos3.csv")
print("Abriendo datos3.csv")
heads=None
filas=[]
for line in fhand:
    if heads is None:
        line=line.lower().split(";")
        heads=line
        continue
    line=line.strip()
    fil=line.split(";")
    filas.append(fil)
# Revisar copias
borrar=[]
for i in range(0,len(filas)):
    copias=[]
    actual=dt.datetime.strptime(filas[i][0].strip(),"%m/%d/%Y %H:%M:%S")
    for j in range(0,len(filas)):
        if len(filas[i][2])<1 or len(filas[j][2])<1:continue
        if int(filas[i][2])==int(filas[j][2]):
            revi=dt.datetime.strptime(filas[j][0].strip(),"%m/%d/%Y %H:%M:%S")
            copias.append((j,revi))
    copias.sort(reverse=True)
    copias.pop(0)
    for copia in copias:
        if copia[0] not in borrar:
            borrar.append(copia[0])
borrar.sort(reverse=True)
for num in borrar:
    filas.pop(num)
# Adicionar datos3
for i in range(0,rost):
    for fila in filas:
        if len(fila[2])<1:continue
        if int(fila[2])!=act[7][i]:continue
        print("Adicionando datos a:", act[1][i],act[2][i])
        # Rh
        act[41].append(fila[8])
        # anios
        if int(fila[12])>1990:
            act[25].append(fila[12])
        else:
            anio=hoy.year-int(fila[12])
            act[25].append(anio)
        # npas
        act[9].append(fila[5])

print("=======================================================================")
print("Titulos de datos3.csv:",heads)
# ========================
# COPIANDO ACT A DATAFRAME
# ========================
dfHeads=df.columns.tolist()
print(len(dfHeads),len(act))
for i in range(0,len(act)):
    print(dfHeads[i],len(act[i]))
    if len(act[i])!=rost:
        print("No se pudo actualizar:",dfHeads[i])
        z="-"
        if dfHeads[i]=="anios" or dfHeads[i] =="seleU" or dfHeads[i]=="rolSele":z=-1
        act[i]=[ z for _ in range(0,rost)]
        df[dfHeads[i]]=act[i]
        continue
    if len(act[i])>1:
        df[dfHeads[i]]=act[i]
print("=======================================================================")
print("Títulos del DF:",df.columns.tolist())

#print("=======================================================================")
#print("Contenido de act:",act)
# ==========================
# EXPORTANDO DATAFRAME LISTO
# ==========================
df.to_excel('datosLimpios.xlsx', index = False, header=True)
