import tkinter as tk
import tkinter.font as tkf

class ventana_inicio(tk.Frame):
    def __init__(self,parent,controller,dbs):
        tk.Frame.__init__(self,controller)
        self.pack()
        self.controller=controller
        self.db_state=dbs

        lblmuc=tk.Label(self,text="MAMOOTS ULTIMATE CLUB",font=tkf.Font(family="Arial Black",size="20"))
        lbl98=tk.Label(self,text="Alive since 1998",font=tkf.Font(family="Segoe Script",slant="italic"))
        lblbla=tk.Label(self,text="Version 1.0 // 2020",font=tkf.Font(family="Arial Black",size="8"),width=20)
        
        lbfDB=tk.LabelFrame(self,text="SQL")
        btnIDB=tk.Button(lbfDB,text="Iniciar")
        btnCDB=tk.Button(lbfDB,text="Cargar")
        btnBDB=tk.Button(lbfDB,text="Borrar")

        lbfinf=tk.LabelFrame(self,text="Aplicación")
        btnIAP=tk.Button(lbfinf,text="Iniciar")
        btnLAP=tk.Button(lbfinf,text="Ver Log")

        lbfst=tk.LabelFrame(self,text="Revisión")
        btnst=tk.Button(lbfst,text="Estado")
        btnlb=tk.Button(lbfst,text="Librerías")

        lblmuc.grid(row=0,column=0,columnspan=7)
        lbl98.grid(row=1,column=0,columnspan=7)
        lblbla.grid(row=2,column=0,columnspan=7)
        lbfDB.grid(row=3,column=0,columnspan=3)
        lbfinf.grid(row=3,column=3,columnspan=2)
        lbfst.grid(row=3,column=5,columnspan=2)

        btnIDB.grid(row=0,column=0)
        btnCDB.grid(row=0,column=1)
        btnBDB.grid(row=0,column=2)

        btnIAP.grid(row=0,column=0)
        btnLAP.grid(row=0,column=1)

        btnst.grid(row=0,column=0)
        btnlb.grid(row=0,column=1)
