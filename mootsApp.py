import os.path
import tkinter as tk
import tkinter.font as tkf
import datetime as dt
import inicio as pgi

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
        #self.frames['PgInfo']= --Ubicar la página principal de información--

        self.show_frame('PgInicio')
    
    def show_frame(self, page_nm):
        frame=self.frames[page_nm]
        frame.tkraise()
    
    def commit_txt(self,container):
        self.frames['PgInicio'].destroy()
        self.frames['PgInicio']=pgi.ventana_inicio(container,self,self.check_for_db())
    
    def check_for_db(self):
        check=os.path.exists(".\\mootsRost.sqlite")
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