import tkinter as tk
import datetime
import time

class ventana_principal(tk.Frame):

    def __init__(self,parent,controller,dbs):
        tk.Frame.__init__(self,parent)
        
        self.controller=controller
        self.db_state=dbs

        generalData=tk.LabelFrame(self,text="Generales:")
        activeList=tk.LabelFrame(self,text="Jugadores activos:")
        actions=tk.LabelFrame(self,text="Acciones:")

        lblJug=tk.Label(generalData,text="Jugadores del club: ")
        lblAct=tk.Label(generalData,text="Jugadores activos: ")
        lblJug.grid(row=1,column=0)
        lblAct.grid(row=2,column=0,sticky='w')

        left_bar=tk.Scrollbar(activeList)
        left_bar.pack(side=tk.RIGHT, fill=tk.Y)
        idList=tk.Listbox(activeList,yscrollcommand=left_bar.set,width=16)
        playList=tk.Listbox(activeList,yscrollcommand=left_bar.set,width=40)
        idList.pack(side=tk.LEFT,fill=tk.BOTH)
        playList.pack(side=tk.RIGHT,fill=tk.BOTH)
        def metodoRaro(*args):
            idList.yview(*args)
            playList.yview(*args)
        left_bar.config(command=metodoRaro)

        btnIni=tk.Button(actions,text="Inicio",command=lambda: controller.show_frame('PgInicio'))

        generalData.grid(row=0,column=0,columnspan=3)
        activeList.grid(row=1,column=0,rowspan=2,columnspan=2)
        actions.grid(row=3,column=0,columnspan=3)

        btnIni.grid(row=0,column=9)

        
