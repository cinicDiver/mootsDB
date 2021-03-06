import os.path
import tkinter as tk
import tkinter.font as tkf
import datetime as dt
import inicio as pgi
import principal as pgp

class mootsApp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title("MootsApp 2020")
        
        self.log_path=os.path.join(os.path.dirname(__file__),'./log/app_log.txt')

        container=tk.Frame(self)
        container.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.add_to_log("Ingreso a la app. ({})".format(dt.datetime.strftime(dt.datetime.today(),format="%d/%m/%Y %H:%M:%S")))

        self.frames={}
        self.frames['PgInicio']=pgi.ventana_inicio(container,self,self.check_for_db())
        self.frames['PgPrinc']= pgp.ventana_principal(container,self,self.check_for_db())

        self.show_frame('PgInicio')
    
    def show_frame(self, page_nm):
        for frame in self.frames.values():
            frame.grid_remove()
        frame=self.frames[page_nm]
        frame.grid()
        frame.winfo_toplevel().geometry("")
    
    def commit_txt(self,container):
        self.frames['PgInicio'].destroy()
        self.frames['PgInicio']=pgi.ventana_inicio(container,self,self.check_for_db())
    
    def check_for_db(self):
        check=os.path.isfile(".\DBs\mootsRost.sqlite")
        if(check):
            check="OK"
        else:
            check="Not Set"
        return check

    def send_log_path(self):
        return self.log_path
    
    def add_to_log(self,record):
        log_file=open(self.send_log_path(),"a")
        log_file.write(record.strip())
        log_file.write("\n")
        log_file.close()

if __name__=="__main__":
    app=mootsApp()
    app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))
    app.mainloop()