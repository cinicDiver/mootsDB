from tkinter import *
from tkinter import font,messagebox,simpledialog,filedialog
import pandas as pd
import sqlite3

# Definicion de encabezados
hoja=pd.read_excel(".\datos\encabezados.xlsx")
df=pd.DataFrame(hoja.values)
df.columns=df.iloc[0,:]
df.drop(df.index[0],inplace=True)
df.drop(df.columns[[0]],axis=1,inplace=True)
heads=df.columns.values

# Venatana para gregar un nuevo jugador
def ventana_agregar(padre,numeros,eps):
    nuevo=dict()
    ven=Toplevel()
    ven.title("Agregar Jugador")

    datos=LabelFrame(ven,text="Datos")
    varios=LabelFrame(ven,text="Varios")
    numero=LabelFrame(ven,text="Número")
    salud=LabelFrame(ven,text="Salud")
    ultimate=LabelFrame(ven,text="Ultimate")
    residencia=LabelFrame(ven,text="Residencia")
    ocupacion=LabelFrame(ven,text="Ocupación")

    acciones=LabelFrame(ven,text="Acciones")
    #ven.state("zoomed")

    entries=[]
    for i in range(len(heads)):
        if i == 0:
            entries.append(Entry(numero))
        elif i in [1,2,3,4,5,6,7,40,42,43]:
            entries.append(Entry(datos))
        elif i in range(9,14):
            entries.append(Entry(varios))
        elif i in [19,20,21,22,23,24,38,41]:
            entries.append(Entry(salud))
        elif i in [14,25,26,27,28,29,30,31,32,33,34,35,36]:
            entries.append(Entry(ultimate))
        elif i in [17,18,39]:
            entries.append(Entry(residencia))
        else:
            entries.append(Entry(ocupacion))

        if i in [0,5,7,8,12,13,14,15,21,25,26,28,35,43]:
            entries[i].insert(0,-1)
        elif i in [19,20]:
            entries[i].insert(0,-1.0)
        elif i == 4:
            entries[i].insert(0,"dd/mm/aaaa")
        else:
            entries[i].insert(0,"-")
        
    #Falta crear el layout de ventana y agregar las cajas de entrada de acuerdo con el orden de los encabezados para hacerlo más fácil de leer 
    #Puede que sea más largo de acomodar pero me lo voy a agradecer luego.
    #Puede interar los widget Entry en ese orden, no lo olvide.

    #Panel Datos
    datos.grid(row=0,column=0,sticky="nsew")

    lblnombre=Label(datos,text="Nombres")
    lblapellido=Label(datos,text="Apellidos")
    lbldocumento=Label(datos,text="Documento")
    lblcelular=Label(datos,text="Celular")
    lblcorreo=Label(datos,text="Correo")
    lblnacim=Label(datos,text="Fecha de nacimiento")
    lblciudad=Label(datos,text="Ciudad")
    lblcontacto=Label(datos,text="Contacto")
    lblncont=Label(datos,text="Número de contacto")
    
    varDoc=StringVar()
    def doct():
        entries[6].delete(0,END)
        entries[6].insert(0,varDoc.get())
    doc1=Radiobutton(datos,variable=varDoc,value="TI",command=doct)
    doc2=Radiobutton(datos,variable=varDoc,value="CC",command=doct)
    doc3=Radiobutton(datos,variable=varDoc,value="Otro",command=doct)
    lbld1=Label(datos,text="TI")
    lbld2=Label(datos,text="CC")
    lbld3=Label(datos,text="Otro")
    
    lblnombre.grid(row=0,column=0,sticky=W)
    lblapellido.grid(row=0,column=1,sticky=W)
    lbldocumento.grid(row=0,column=2,sticky=W)
    lbld1.grid(row=0,column=3,sticky=W)
    lbld2.grid(row=0,column=4,sticky=W)
    lbld3.grid(row=0,column=5,sticky=W)

    entries[1].grid(row=1,column=0,sticky=W)
    entries[2].grid(row=1,column=1,sticky=W)
    entries[7].grid(row=1,column=2,sticky=W)
    doc1.grid(row=1,column=3,sticky=W)
    doc2.grid(row=1,column=4,sticky=W)
    doc3.grid(row=1,column=5,sticky=W)

    lblcelular.grid(row=2,column=0,sticky=W)
    lblcorreo.grid(row=2,column=1,sticky=W)
    lblnacim.grid(row=2,column=2,sticky=W)

    entries[5].grid(row=3,column=0,sticky=W)
    entries[3].grid(row=3,column=1,sticky=W)
    entries[4].grid(row=3,column=2,sticky=W)

    lblciudad.grid(row=4,column=0,sticky=W)
    lblcontacto.grid(row=4,column=1,sticky=W)
    lblncont.grid(row=4,column=2,sticky=W)

    entries[40].grid(row=5,column=0,sticky=W)
    entries[42].grid(row=5,column=1,sticky=W)
    entries[43].grid(row=5,column=2,sticky=W)
    
    #Panel Varios
    varios.grid(row=0,column=1,sticky="nsew")

    pasvar=IntVar()
    visvar=IntVar()
    alimvar=IntVar()

    lblapodo=Label(varios,text="Apodo")
    lblingreso=Label(varios,text="Año de ingreso")
    lblpas=Label(varios,text="Pasaporte")
    lblnpas=Label(varios,text="Número")
    lblvis=Label(varios,text="Visa")
    lblalim=Label(varios,text="Alimentación")
    chpas=Checkbutton(varios,variable=pasvar,onvalue=1,offvalue=0)
    chvis=Checkbutton(varios,variable=visvar,onvalue=1,offvalue=0)

    menAlim=Menubutton(varios,text="Opciones",relief=RAISED)
    menAlim.menu=Menu(menAlim)
    menAlim["menu"]=menAlim.menu
    menAlim.menu.add_checkbutton(label="Normal",variable=alimvar,onvalue=0)
    menAlim.menu.add_checkbutton(label="Vegetariano",variable=alimvar,onvalue=1)

    entries[9].config(state="disabled")
    chvis.config(state="disabled")
    def def_pas():
        if int(pasvar.get())==1:
            entries[9].config(state="normal")
            chvis.config(state="normal")
        else:
            entries[9].config(state="disabled")
            chvis.config(state="disabled")
    chpas.config(command=def_pas)

    lblapodo.grid(row=0,column=0,sticky=W)
    lblpas.grid(row=0,column=1,sticky=W)
    lblnpas.grid(row=0,column=2,sticky=W)
    lblvis.grid(row=0,column=3,sticky=W)

    entries[11].grid(row=1,column=0,sticky=W)
    chpas.grid(row=1,column=1,sticky=W)
    entries[9].grid(row=1,column=2,sticky=W)
    chvis.grid(row=1,column=3,sticky=W)

    lblingreso.grid(row=2,column=0,sticky=W)

    entries[12].grid(row=3,column=0,sticky=W)

    lblalim.grid(row=4,column=0,sticky=W)

    menAlim.grid(row=5,column=0,sticky=W)

    
    # Panel Numero
    numero.grid(row=0,column=2,sticky="nsew")

    nums=Spinbox(numero,from_=0,to=99,font=font.Font(size=24))
    lblEN1=Label(numero)
    lblEN2=Label(numero)
    lblNum=Label(numero,text="El número está disponible.")

    def def_num():
        n=int(nums.get())
        if n in numeros:
            lblNum.configure(text="El número no está disponible.")
        else:
            lblNum.configure(text="El número está disponible.")
    nums.config(command=def_num)

    nums.grid(row=0,sticky=NSEW)
    lblEN1.grid(row=2)
    lblNum.grid(row=3)
    lblEN2.grid(row=4)

    # Panel Salud
    salud.grid(row=1,column=0,sticky="nsew")
    rhs=["A+","A-","AB+","AB-","B+","B-","O+","O-"]
    rhvar=StringVar()
    epsvar=StringVar()
    enfvar=IntVar()

    lbltalla=Label(salud,text="Talla [m]")
    lblpeso=Label(salud,text="Peso [kg]")
    lblrh=Label(salud,text="Rh")
    lbleps=Label(salud,text="EPS")
    lblenf=Label(salud,text="¿Existe alguna condición de salúd?")
    lblenfer=Label(salud,text="Enfermdedad")
    lblmedi=Label(salud,text="Medicamentos")
    lblreco=Label(salud,text="Recomendaciones")

    menRh=Menubutton(salud,text="tipos",relief=RAISED)
    menRh.menu=Menu(menRh)
    menRh["menu"]=menRh.menu
    for tip in rhs:
        menRh.menu.add_checkbutton(label=tip,variable=rhvar,onvalue=tip)

    menEps=Menubutton(salud,text="Entidad",relief=RAISED)
    menEps.menu=Menu(menEps)
    menEps["menu"]=menEps.menu
    for ent in eps:
        menEps.menu.add_checkbutton(label=ent,variable=epsvar,onvalue=ent)
    def otra_eps():
        nom="-"
        while nom=="-" or nom=="":
            nom=simpledialog.askstring("Agregar jugador","Ingrese el nombre de la EPS",parent=ven)
            epsvar.set(nom)
    menEps.menu.add_checkbutton(label="Otra",command=otra_eps)

    chenf=Checkbutton(salud,variable=enfvar,onvalue=1,offvalue=0)
    entries[22].config(state='disabled')
    entries[23].config(state='disabled')
    entries[24].config(state='disabled')
    def def_enf():
        if int(enfvar.get())==1:
            entries[22].config(state='normal')
            entries[23].config(state='normal')
            entries[24].config(state='normal')
        else:
            entries[22].config(state='disabled')
            entries[23].config(state='disabled')
            entries[24].config(state='disabled')
    chenf.config(command=def_enf)

    lbltalla.grid(row=0,column=0,sticky=W)
    lblpeso.grid(row=0,column=1,sticky=W)
    lblrh.grid(row=0,column=2,sticky=W)

    entries[19].grid(row=1,column=0,sticky=W)
    entries[20].grid(row=1,column=1,sticky=W)
    menRh.grid(row=1,column=2,sticky=W)

    lbleps.grid(row=2,column=0,sticky=W)

    menEps.grid(row=3,column=0,sticky=W)

    lblenf.grid(row=4,column=0,sticky=W)

    chenf.grid(row=5,column=0,sticky=W)

    lblenfer.grid(row=6,column=0,sticky=W)
    lblreco.grid(row=6,column=1,sticky=W)

    entries[22].grid(row=7,column=0,sticky=W)
    entries[24].grid(row=7,column=1,sticky=W)

    lblmedi.grid(row=8,column=0,sticky=W)

    entries[23].grid(row=9,column=0,sticky=W)

    # Panel Ultimate
    ultimate.grid(row=1,column=1,columnspan=2,sticky="nsew")

    lblAct=Label(ultimate,text="Activo")
    lblanio=Label(ultimate,text="Año de inicio")
    lbllin=Label(ultimate,text="Línea")
    lblpos=Label(ultimate,text="Posisición")
    lblscol=Label(ultimate,text="Selección Colombia")
    lbldcol=Label(ultimate,text="Participaciones")
    lblsu=Label(ultimate,text="Selección Universitaria")
    lbldu=Label(ultimate,text="Universidad")
    lblotros=Label(ultimate,text="Otros equipos")
    lblint=Label(ultimate,text="Intensidad horaria con otros")
    lblprev=Label(ultimate,text="Equipos previos")
    lbllog=Label(ultimate,text="Logros en ultimate")
    lblvis=Label(ultimate,text="Visión del ultimate")

    varact=IntVar()
    varcol=IntVar()
    varu=IntVar()

    entries[29].config(state="disabled")
    entries[27].config(state="disabled")

    def def_col():
        if int(varcol.get())==1:
            entries[27].config(state="normal")
        else:
            entries[27].config(state="disabled")
    
    def def_u():
        if int(varu.get())==1:
            entries[29].config(state="normal")
        else:
            entries[29].config(state="disabled")

    chact=Checkbutton(ultimate,variable=varact,onvalue=1,offvalue=0)
    chcol=Checkbutton(ultimate,variable=varcol,onvalue=1,offvalue=0,command=def_col)
    chu=Checkbutton(ultimate,variable=varu,onvalue=1,offvalue=0,command=def_u)

    lblAct.grid(row=0,column=0,sticky=W)
    lblscol.grid(row=0,column=1,sticky=W)
    lblotros.grid(row=0,column=2,sticky=W)
    lblprev.grid(row=0,column=3,sticky=W)

    chact.grid(row=1,column=0,sticky=W)
    chcol.grid(row=1,column=1,sticky=W)
    entries[34].grid(row=1,column=2,sticky=W)
    entries[30].grid(row=1,column=3,sticky=W)

    lblanio.grid(row=2,column=0,sticky=W)
    lbldcol.grid(row=2,column=1,sticky=W)
    lblint.grid(row=2,column=2,sticky=W)
    lbllog.grid(row=2,column=3,sticky=W)

    entries[25].grid(row=3,column=0,sticky=W)
    entries[27].grid(row=3,column=1,sticky=W)
    entries[35].grid(row=3,column=2,sticky=W)
    entries[31].grid(row=3,column=3,sticky=W)

    lbllin.grid(row=4,column=0,sticky=W)
    lblsu.grid(row=4,column=1,sticky=W)
    lblvis.grid(row=4,column=3,sticky=W)

    entries[32].grid(row=5,column=0,sticky=W)
    chu.grid(row=5,column=1,sticky=W)
    entries[36].grid(row=5,column=3,sticky=W)

    lblpos.grid(row=6,column=0,sticky=W)
    lbldu.grid(row=6,column=1,sticky=W)
    
    entries[33].grid(row=7,column=0,sticky=W)
    entries[29].grid(row=7,column=1,sticky=W)

    # Panel residencia
    residencia.grid(row=2,column=0,sticky="nsew")

    lblciur=Label(residencia,text="Ciudad")
    lblbar=Label(residencia,text="Barrio")
    lbldir=Label(residencia,text="Direccón")

    lblciur.grid(row=0,column=0,sticky=W)
    lblbar.grid(row=0,column=1,sticky=W)
    lbldir.grid(row=0,column=2,sticky=W)

    entries[39].grid(row=1,column=0,sticky=W)
    entries[17].grid(row=1,column=1,sticky=W)
    entries[18].grid(row=1,column=2,sticky=W)

    # Panel ocupacion
    ocupacion.grid(row=2,column=1,sticky="nsew")

    ocup={"Estudiante":0,"Independiente":1,"Empleado":2,"Desempleado":3,"Otro":4}
    menOc=Menubutton(ocupacion,text="Opciones",relief=RAISED)
    menOc.menu=Menu(menOc)
    menOc['menu']=menOc.menu
    varoc=IntVar()
    for k,v in ocup.items():
        menOc.menu.add_checkbutton(label=str(k),variable=varoc,onvalue=int(v))

    nivED = ["Ninguno","Primaria","Bachillerato","Técnico","Pregrado","Posgrado"]
    menEd=Menubutton(ocupacion,text="Nivel",relief=RAISED)
    menEd.menu=Menu(menEd)
    menEd['menu']=menEd.menu
    vared=StringVar()
    for niv in nivED:
        menEd.menu.add_checkbutton(label=niv,variable=vared,onvalue=niv)

    lblocup=Label(ocupacion,text="Ocupación")
    lblinsti=Label(ocupacion,text="Institución")
    lbled=Label(ocupacion,text="Nivel educativo")

    lblocup.grid(row=0,column=0,sticky=W)
    lblinsti.grid(row=0,column=1,sticky=W)
    lbled.grid(row=0,column=2,sticky=W)

    menOc.grid(row=1,column=0,sticky=W)
    entries[37].grid(row=1,column=1,sticky=W)
    menEd.grid(row=1,column=2,sticky=W)

    # Métodos de botones
    
    def get_input(*args):
        entries[0].delete(0,END)
        entries[0].insert(0,nums.get())
        entries[8].delete(0,END)
        entries[8].insert(0,pasvar.get())
        entries[10].delete(0,END)
        entries[10].insert(0,visvar.get())
        entries[13].delete(0,END)
        entries[13].insert(0,alimvar.get())
        entries[14].delete(0,END)
        entries[14].insert(0,varact.get())
        entries[15].delete(0,END)
        entries[15].insert(0,varoc.get())
        entries[16].delete(0,END)
        entries[16].insert(0,vared.get())
        entries[21].delete(0,END)
        entries[21].insert(0,enfvar.get())
        entries[26].delete(0,END)
        entries[26].insert(0,varcol.get())
        entries[28].delete(0,END)
        entries[28].insert(0,varu.get())
        entries[38].delete(0,END)
        entries[38].insert(0,epsvar.get())
        entries[41].delete(0,END)
        entries[41].insert(0,rhvar.get())
        for i in range(len(entries)):
            if i in [0,5,7,8,12,13,14,15,21,25,26,28,35,43]:
                nuevo[heads[i]]=int(entries[i].get())
            elif i in [19,20]:
                nuevo[heads[i]]=float(entries[i].get())
            else:
                nuevo[heads[i]]=entries[i].get()
        if nuevo["numero"] in numeros:
            messagebox.showwarning("Agregar Jugador","El número {} ya lo tiene un jugador activo.".format(str(nuevo["numero"])),parent=ven)
        else:
            ven.destroy()

    def reiniciar():
        for i in range(len(heads)):
            if i in [0,5,7,8,12,13,14,15,21,25,26,28,35,43]:
                entries[i].delete(0,END)
                entries[i].insert(0,-1)
            elif i in [19,20]:
                entries[i].delete(0,END)
                entries[i].insert(0,-1.0)
            elif i == 4:
                entries[i].delete(0,END)
                entries[i].insert(0,"dd/mm/aaaa")
            else:
                entries[i].delete(0,END)
                entries[i].insert(0,"-")

    def cancelar():
        nuevo["cancelado"]=True
        ven.destroy()

    #Panel Acciones
    acciones.grid(row=3,column=1,sticky="nsew")

    butAg=Button(acciones,text="Agregar",command=get_input)
    butRe=Button(acciones,text="Reiniciar",command=reiniciar)
    butCa=Button(acciones,text="Cancelar",command=cancelar)

    butAg.grid(row=1,column=0,sticky=E)
    butRe.grid(row=1,column=1,sticky=N)
    butCa.grid(row=1,column=2,sticky=W)

    ven.wait_window()
    return nuevo
    
def ventana_dir_formato(padre):
    ven=Toplevel(padre)
    ven.filename = filedialog.askopenfilename(title="Seleccione formato de jugadores", filetypes=(("Hoja de Excel","*.xlsx"),("Todos los archivos","*.*")))
    return ven.filename 

def ventana_borrar_id(padre):
    idd=-1
    ven=Toplevel(padre)
    ven.title("Introducir id")
    lbl=Label(ven,text="Introduzca la id del jugador que desea borrar:")
    svar=StringVar()
    ent=Entry(ven,textvariable=svar)
    fr=Frame(ven)
    def butA_m():
        nonlocal idd
        idd=int(svar.get())
        ven.destroy()
    def butC_m():
        nonlocal idd
        idd=-1
        ven.destroy()
    butA=Button(fr,text="Aceptar",command=butA_m,relief=RAISED)
    butC=Button(fr,text="Cancelar",command=butC_m,relief=RAISED)

    lbl.grid(row=0,sticky="nswe")
    ent.grid(row=1,sticky="nswe")
    fr.grid(row=2,sticky="nswe")
    butA.pack(side=LEFT,fill=BOTH)
    butC.pack(side=RIGHT,fill=BOTH)

    ven.wait_window()
    return idd

