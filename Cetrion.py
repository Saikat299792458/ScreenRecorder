from tkinter import *
from threading import Thread
from PIL import Image,ImageTk
import time
class Animator:
    def __init__(self,ui=True,param=None,bg='green',fg='black',font='Calibri',image_location=(.5,.6,'s'),text_location=(.5,.6,'n'),image_size=None,text_size=None):
        self.bg=bg
        self.ui=ui
        self.param=param
        self.fg=fg
        self.tl=text_location
        self.il=image_location
        if param:
            mn=min(param[0],param[1])
        else:
            mn=500
        if text_size!=None:
            self.font=(font,text_size)
        else:
            self.font=(font,int(mn*7/100))#Change here
        self.img=Image.open('logo.png')
        if image_size!=None:
            self.img=self.img.resize(image_size,Image.LANCZOS)
        else:
            self.img=self.img.resize((int(mn*40/100),int(mn*40/100)),Image.LANCZOS)#Change here
    def iterate(self):
        tk=Tk()
        if self.param:
            tk.geometry(str(self.param[0])+'x'+str(self.param[1])+'+'+str(self.param[2])+'+'+str(self.param[3]))
        else:
            tk.geometry('500x500+'+str((tk.winfo_screenwidth()-500)//2)+'+'+str((tk.winfo_screenheight()-500)//2))
        tk.overrideredirect(1)
        mn=min(tk.winfo_width(),tk.winfo_height())
        tk['bg']=self.bg
        self.text='Loading'
        self.img=ImageTk.PhotoImage(self.img)
        label1=Label(tk,image=self.img,bg=self.bg)
        label2=Label(tk,text=self.text,bg=self.bg,fg=self.fg,font=self.font)#This is for image
        label1.place(relx=self.il[0],rely=self.il[1],anchor=self.il[2])
        label2.place(relx=self.tl[0],rely=self.tl[1],anchor=self.tl[2])
        self.running=True
        tk.deiconify()
        tk.update()
        while self.running:
            text=label2['text']
            if text=='Loading':
                label2['text']='Loading.'
            elif text=='Loading.':
                label2['text']='Loading..'
            elif text=='Loading..':
                label2['text']='Loading...'
            else:
                label2['text']='Loading'
            tk.update()
            time.sleep(.1)
        if self.ui:
            tk.destroy()
            tk.mainloop()
        else:
            import gc
            del tk#These lines are useful for non image programs without using .protocol(WM_DELETE_WINDOW)
            gc.collect()#In that case delete the destroy and mainloop lines above
    def start(self):
        self.threadid=Thread(target=self.iterate)
        self.threadid.start()
    def pquit(self):
        quit()
    def stop(self):
        self.running=False
        self.threadid.join()
        if self.ui:
            tm=Tk()
            tm.protocol('WM_DELETE_WINDOW',self.pquit)
            tm.focus_force()
            return tm
