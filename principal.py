import tkinter as tk
import datetime
import time

class ventana_principal(tk.Frame):

    def __init__(self,parent,controller,dbs):
        tk.Frame.__init__(self,controller)
        self.pack()
        self.controller=controller
        self.db_state=dbs

        generalData=tk.LabelFrame(self,text="Generales:")
        activeList=tk.LabelFrame(self,text="Jugadores activos:")
        actions=tk.LabelFrame(self,text="Acciones:")

        btnIni=tk.Button(actions,text="Inicio",command=lambda: self.controller.show_frame('PgInicio'))

        generalData.grid(row=0,column=0,columnspan=3)
        activeList.grid(row=1,column=0,rowspan=2,columnspan=2)
        actions.grid(row=3,column=0,columnspan=3)

        btnIni.grid(row=0,column=9)

        
