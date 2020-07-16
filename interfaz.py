from tkinter import *
import datetime
import time
import roster
#import ventanas

# Ventana principal
fecha=datetime.date.today()
ventana=Tk()
ventana.title("Mamoots {}".format(fecha.year))
ventana.state('zoomed')

ver=roster.version()

arriba=LabelFrame(ventana,text="Generales")
arriba.grid(row=0,columnspan=3)
abajo=LabelFrame(ventana,text="Acciones")
abajo.grid(row=2,columnspan=3)
jugadores=roster.lista_jugadores()
izquierda=LabelFrame(ventana,text="Lista de jugadores activos:")
derecha=LabelFrame(ventana,text="Otros")
derecha.grid(row=1,column=2)
derechaI=LabelFrame(derecha,text="Log")
derechaI.grid(row=1)

panLog=Listbox(derechaI)
loghoy=["Se inició la aplicación el {}".format(fecha),"Versión {}".format(ver)]

# Métodos de creacion
def agregar_log(entrada):
    loghoy.append(entrada)
    panLog.insert(END,entrada)
""" def venAgregar()->None:
    agregar_log("Se quiere agregar un nuevo jugador.")
    disp=roster.numeros()
    eps=roster.eps()
    nuevo=ventanas.ventana_agregar(ventana,disp,eps)
    res=roster.nuevo_jugador(nuevo)
    agregar_log(res)
def agregar_formato():
    agregar_log("Se quiere agregar jugadores usando un formato.")
    archivo=ventanas.ventana_dir_formato(ventana)
    numeros=roster.numeros()
    res=roster.nuevos_formato(archivo,numeros)
    for s in res:
        agregar_log(s)
    agregar_log("Fin de agregar por formato.")
def borrar_jugador():
    idd=ventanas.ventana_borrar_id(ventana)
    agregar_log("Se desea borrar un jugador.")
    if idd != -1:
        res=roster.borrar_jugador(idd)
        agregar_log(res)
    else: agregar_log("Cancelado por el usuario.") """


# Panel superior
actividad=roster.activos()
lblJug=Label(arriba,text="Jugadores del club: {}".format(actividad[0]))
lblAct=Label(arriba,text="Jugadores activos: {}".format(actividad[1]))
lblJug.grid(row=1,column=0)
lblAct.grid(row=2,column=0,sticky=W)

# Panel izquierda
izquierda.grid(row=1,column=0,columnspan=2)
barraIz=Scrollbar(izquierda)
barraIz.pack(side=RIGHT, fill=Y)
listaId=Listbox(izquierda,yscrollcommand=barraIz.set,width=16)
listaJug=Listbox(izquierda,yscrollcommand=barraIz.set,width=40)
listaId.pack(side=LEFT,fill=BOTH)
listaJug.pack(side=RIGHT,fill=BOTH)
def metodoRaro(*args):
    listaId.yview(*args)
    listaJug.yview(*args)
barraIz.config(command=metodoRaro)
for jugador in jugadores:
    listaJug.insert(END,jugador[1]+", "+jugador[0])
    listaId.insert(END,"Id de Jugador: "+str(jugador[2]))

#Panel Derecha

#Panel derecha abajo
barraDinf=Scrollbar(derechaI)
barraDinf.pack(side=RIGHT,fill=Y)
panLog.configure(yscrollcommand=barraDinf.set,width=50)
for evento in loghoy:
    panLog.insert(END,evento)
panLog.pack(anchor=CENTER)

#Métodos varios
def actualizar():
    actividad=roster.activos()
    lblJug.config(text="Jugadores del club: {}".format(actividad[0]))
    lblAct.config(text="Jugadores activos: {}".format(actividad[1]))
    listaJug.delete(0,END)
    listaId.delete(0,END)
    jugadores=roster.lista_jugadores()
    for jugador in jugadores:
        listaJug.insert(END,jugador[1]+", "+jugador[0])
        listaId.insert(END,"Id de Jugador: "+str(jugador[2]))


#Panel inferior
ag=Button(abajo,text="Agregar Jugador")#,command=venAgregar)
ag2=Button(abajo,text="Agregar con formato")#,command=agregar_formato)
buj=Button(abajo,text="Buscar Jugador")
buc=Button(abajo,text="Buscar por criterio")
boj=Button(abajo,text="Borrar Jugador")#,command=borrar_jugador)
act=Button(abajo,text="Actualizar lista",command=actualizar)
bob=Button(abajo,text="Borrar base de datos")

ag.grid(row=0,column=0,sticky=W,padx=5)
ag2.grid(row=0,column=1,sticky=W,padx=5)
buj.grid(row=0,column=2,sticky=W,padx=5)
buc.grid(row=0,column=3,sticky=W,padx=5)
boj.grid(row=0,column=4,sticky=W,padx=5)
act.grid(row=0,column=5,sticky=W,padx=5)
bob.grid(row=0,column=6,sticky=W,padx=5)

ventana.mainloop()