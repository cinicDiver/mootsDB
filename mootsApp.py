import os.path
import tkinter as tk
import tkinter.font as tkf
import inicio as pgi

class mootsApp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        container=tk.Frame(self)
        container.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.frames={}
        self.frames['PgInicio']=pgi.ventana_inicio(container,self,self.check_for_db())
        #self.frames['PgInfo']= --Ubicar la página principal de información--

        self.show_frame('PgInicio')
    
    def show_frame(self, page_nm):
        frame=self.frames[page_nm]
        frame.tkraise()
    
    def check_for_db(self):
        check=os.path.exists(".\\mootsRost.sqlite")
        if(check):
            check=1
        else:
            check=0
        return check

if __name__=="__main__":
    app=mootsApp()
    app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))
    app.mainloop()