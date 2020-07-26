import os.path
import tkinter as tk
import tkinter.font as tkf
from tkinter import simpledialog
import datetime as dt
import lib_check

class ventana_inicio(tk.Frame):

    def __init__(self,parent,controller,dbs):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        self.db_state=dbs
        self.lib_state=lib_check.check_lib_install()

        lblmuc=tk.Label(self,text="MAMOOTS ULTIMATE CLUB",font=tkf.Font(family="Arial Black",size="20"))
        lbl98=tk.Label(self,text="Alive since 1998",font=tkf.Font(family="Segoe Script",slant="italic"))
        lblbla=tk.Label(self,text="Version 1.0 // 2020",font=tkf.Font(family="Arial Black",size="8"),width=20)
        
        lbfDB=tk.LabelFrame(self,text="SQL")
        btnIDB=tk.Button(lbfDB,text="Iniciar",width=10)
        btnCDB=tk.Button(lbfDB,text="Cargar",width=10)
        btnBDB=tk.Button(lbfDB,text="Borrar",width=10)

        lbfinf=tk.LabelFrame(self,text="Aplicación")
        btnIAP=tk.Button(lbfinf,text="Iniciar",width=10,command=lambda:controller.show_frame('PgPrinc'))
        btnLAP=tk.Button(lbfinf,text="Ver Log",width=10,command=lambda:self.show_log())

        lbfst=tk.LabelFrame(self,text="Revisión")
        btnst=tk.Button(lbfst,text="Estado",width=10,command=lambda:self.show_state())
        btnlb=tk.Button(lbfst,text="Librerías",width=10,command=lambda:self.install_libs())

        lblmuc.grid(row=0,column=0,columnspan=7)
        lbl98.grid(row=1,column=0,columnspan=7)
        lblbla.grid(row=2,column=0,columnspan=7)
        lbfDB.grid(row=3,column=0,columnspan=3,sticky="we")
        lbfinf.grid(row=3,column=3,columnspan=2,sticky="we")
        lbfst.grid(row=3,column=5,columnspan=2,sticky="we")

        btnIDB.grid(row=0,column=0)
        btnCDB.grid(row=0,column=1)
        btnBDB.grid(row=0,column=2)

        btnIAP.grid(row=0,column=0)
        btnLAP.grid(row=0,column=1)

        btnst.grid(row=0,column=0)
        btnlb.grid(row=0,column=1)

    # Métodos

    def show_log(self):
        log_win=tk.Toplevel(self)
        x = self.controller.winfo_x()
        y = self.controller.winfo_y()
        log_win.geometry("+%d+%d" % (x+200, y+100))
        log_win.title("Log")
        log_scroll=tk.Scrollbar(log_win)
        log_scroll.pack(side=tk.RIGHT,fill=tk.Y)
        log_view=tk.Listbox(log_win,yscrollcommand=log_scroll,width=40)
        log_scroll.config(command=log_view.yview)
        log_file=open(self.controller.send_log_path(),"r")
        for line in log_file:
            log_view.insert(tk.END,line)
        log_file.close()
        log_view.pack(side=tk.TOP,fill=tk.BOTH)
        btnk=tk.Button(log_win,text="Cerrar",command=lambda:log_win.destroy())
        btnk.pack(side=tk.BOTTOM,fill=tk.BOTH)
    
    def show_state(self):
        state_win=tk.Toplevel(self)
        x = self.controller.winfo_x()
        y = self.controller.winfo_y()
        state_win.geometry("+%d+%d" % (x+200, y+100))
        state_win.title("Estado")
        state_scroll=tk.Scrollbar(state_win)
        state_scroll.pack(side=tk.RIGHT,fill=tk.Y)
        state_view=tk.Listbox(state_win,yscrollcommand=state_scroll,width=40)
        state_scroll.config(command=state_view.yview)
        state_view.insert(tk.END,"--Estado del SQL:-- \n")
        state_view.insert(tk.END,"mootsDB: "+self.db_state+"\n")
        state_view.insert(tk.END,"--Estado de los Módulos:-- \n")
        for k,v in self.lib_state.items():
            if v is not None or v != "":
                if(v):stt="OK"
                else:stt="Uninstalled"
                state_view.insert(tk.END,k+": "+stt+""+"\n")
        state_view.pack(side=tk.TOP,fill=tk.BOTH)
        btnk=tk.Button(state_win,text="Cerrar",command=lambda:state_win.destroy())
        btnk.pack(side=tk.BOTTOM,fill=tk.BOTH)
    
    def install_libs(self):
        libs_win=tk.Toplevel(self)
        x = self.controller.winfo_x()
        y = self.controller.winfo_y()
        libs_win.geometry("+%d+%d" % (x+200, y+100))
        libs_win.title("Librerias")
        libs_scroll=tk.Scrollbar(libs_win)
        libs_scroll.pack(side=tk.RIGHT,fill=tk.Y)
        libs_view=tk.Listbox(libs_win,yscrollcommand=libs_scroll,width=40)
        libs_scroll.config(command=libs_view.yview)
        self.controller.add_to_log("Se quiere utilizar la lista de instalación para actualizar los módulos disponibles. ({})".format(dt.datetime.strftime(dt.datetime.today(),format="%d/%m/%Y %H:%M:%S")))
        rsp=lib_check.install_libs(self.lib_state)
        if(len(rsp)==0):
            libs_view.insert(tk.END,"No hay módulos en lista de instalación.")
            self.controller.add_to_log("No hay módulos en la lista de instalación.")
        for msg in rsp:
            libs_view.insert(tk.END,"{}\n".format(msg))
            self.controller.add_to_log("{}".format(msg))
        libs_view.pack(side=tk.TOP,fill=tk.BOTH)
        lbf=tk.Frame(libs_win)
        lbf.pack(side=tk.BOTTOM,fill=tk.BOTH)
        btna=tk.Button(lbf,text="Agregar",command=lambda:self.add_lib(libs_view),width=20)
        btnk=tk.Button(lbf,text="Cerrar",command=lambda:self.commit_destroy(libs_win),width=20)
        btna.grid(row=0,column=0)
        btnk.grid(row=0,column=1)

    def commit_destroy(self,win):
        win.destroy()
        self.controller.commit_txt(self.controller)
    def add_lib(self,view):
        name=simpledialog.askstring(title="Agregar Módulo",prompt="Nombre del módulo:")
        if name is not None:
            self.controller.add_to_log("Se quiere agregar el módulo {} a la lista de instalación. ({})".format(name,dt.datetime.strftime(dt.datetime.today(),format="%d/%m/%Y %H:%M:%S")))
            lib_check.add_lib(name)
            view.insert(tk.END,name+" agregado a la lista de instalación.\n")