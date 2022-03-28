#There's a serious problem with audio blocksize probably,some bits go missing sometimes, consequently, for longer record,last few seconds are rendered audioless.
#Also, the synchronization is not held for larger records
#Try to use sounddevice.rec()#Link-runtime.py
#Meanwhile, use the Icecream recorder, VidCon.py and Adobe Premiere Pro.
#Improvements:
#if the ix or iy is negetive, it should be zero
#if the selected area is 98% of the monitor, it should capture fullscreen
#Alternatively, there maybe is a problem selecting the fullscreen window- at the top left corner the cursor changes from tcross to others
#After pressing Alt+Tab moving/resizing the selection becomes difficult
#In icecream recorder, the connection to microphone is established right when the program is launched. Not right before recording.
import Cetrion
x=Cetrion.Animator()
x.start()
from tkinter import *
from ctypes import windll
from tkinter import filedialog,messagebox
from PIL import Image,ImageGrab
from win10toast_click import ToastNotifier
import keyboard,os,win32ui,win32gui,numpy,cv2,threading,subprocess,time
import sounddevice as sd
import soundfile as sf
import moviepy.editor as me
from scipy.io.wavfile import write
from tkinter import ttk
x.stop()
user32 = windll.user32#These are for setting the High DPI behaviour of this application, so that I can select areas perfectly
user32.SetProcessDPIAware()#These also changes the texture of my tkinter window
top=Tk()
global var,c,n,s,w,e,e1,br,l2,ne,nw,se,sw,wor,phei,pey,pwid,pex,f1,psd,ding,bcol,lim,cncld
global lof,loaf,stream
c=m=sel=ra=inst=n=s=w=e=e1=br=l2=ne=nw=se=f1=sw=Label(top)
php,phv=PhotoImage(file='D:/Python/SR/paused.png'),PhotoImage(file='D:/Python/SR/played.png')
var,ding,bcol,lim=IntVar(),0,top['background'],php
var.set(1)
ix=iy=hei=wid=xdif=ydif=-1
redraw=rsz=cncld=False
def callback(indata,frames,time,status):
    global file,psd
    if psd==0:
        file.write(indata)
stream=sd.InputStream(samplerate=44100,device=18,channels=2,callback=callback)
def setgem(sh,sw):
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x_cordinate = int((screen_width/2) -sw/2)
    y_cordinate = int((screen_height/2) -sh/2-30)
    top.geometry('%dx%d+%d+%d'%(sw,sh,x_cordinate,y_cordinate))
def bff():
    tfn=filedialog.askdirectory()
    if tfn!='':
        e1.delete(0,END)
        e1.insert(0,tfn)
        e1.select_range(0,'end')
def main():
    destroyer()
    global sel,ra,inst,f1,c,e1,psd,lof,loaf,var
    psd,lof,loaf=False,[],[]
    top.overrideredirect(0)
    top.wm_attributes('-transparentcolor','green','-alpha',1,'-fullscreen',0,'-topmost',0)
    top['cursor']='arrow'
    top.deiconify()
    c=Canvas(top)
    f1=Frame(top,borderwidth=5)
    f2=Frame(f1)
    f3=Frame(f2)
    f1.pack()
    setgem(160,360)
    e1=Entry(f3)
    e1.insert(0,os.getcwd())
    br=Button(f3,text='Browse',command=bff)
    l2=Label(f3,text='Save to:')
    ra=Checkbutton(f2,text='Record Internal Audio',variable=var,onvalue=1,offvalue=0)
    l2.pack(side=LEFT)
    e1.pack(side=LEFT)
    br.pack(side=RIGHT)
    ra.pack(side=BOTTOM,anchor='w')
    sel=Button(f1,text='Start',command=select,height=2,width=7)
    sel.pack(side=LEFT)
    f2.pack(side=RIGHT)
    f3.pack(side=TOP)
    c.create_line(0,25,359,25)
    inst=Label(top,text='Click Start to select area. Once selected, press F1 to\n start/pause recording. Press F2 to stop and save your\n recording.',fg='grey')
    inst.pack(side=BOTTOM,pady=10)
    sel.focus()
    sel.bind('<Return>',lambda e:sel.invoke())
    c.place(x=0,y=56)
def destroyer():
    global c,m,sel,ra,inst,e1,br,l2,n,s,w,e,ne,nw,se,sw,f1
    for i in [c,m,sel,ra,inst,e1,br,l2,n,s,e,w,ne,nw,se,f1,sw]:
        i.destroy()
    top.unbind('<B1-Motion>')
    top.unbind('<ButtonRelease-1>')
    top.unbind('<F1>')
    top.unbind('<Escape>')
def complete():#this function is callback to win10toast-click
    global fname
    subprocess.call(fname,shell=True)
def plpa():
    global php,phv,psd,ding,lim,l2
    top.deiconify()
    top.wm_attributes('-alpha',0)
    if ding!=0:
        return
        #l2.destroy()
        #ding=0
    ding+=1
    omg=False
    if psd:
        omg=True
        lim=phv
    else:
        lim=php
        psd=True
    l2=Label(top,image=lim,bg='black')
    l2.pack(fill='both',expand=1)
    def chalpha(cnt):
        nonlocal omg
        global ding,l2,psd
        if cnt<0:
            l2.destroy()
            top.withdraw()
            ding=0
            if omg==True:
                psd=False
            return
        cnt-=0.1
        top.wm_attributes('-alpha',cnt)
        top.after(20,chalpha,cnt)
    chalpha(1)
def setprocess():
    global c,sel,l2,fname,e1
    fname=e1.get()
    if fname[len(fname)-4:]!='.mp4':
        fname+='.mp4'
    if os.path.isfile(fname):
        messagebox.showerror('Error','File Already Exists.')
        return
    destroyer()
    #set the progressbar
    c=ttk.Progressbar(top,orient=HORIZONTAL,length=300,mode='determinate')
    sel=Button(top,text='Cancel')
    l2=Label(top,text='Packing...')
    l2.place(relx=.08,rely=.05,anchor='nw')
    c.place(relx=.08,rely=.35,anchor='w')
    sel.place(relx=.9,rely=.8,anchor='se')
    sel.focus()
    xf=threading.Thread(target=process)
    xf.start()
def stop():
    global bcol,f2,e1,sel,c,l2,cncld,tcount,total
    total+=time.mktime(time.localtime())-tcount
    cncld=True
    top['bg']=bcol
    top.overrideredirect(0)
    top.wm_attributes('-transparentcolor','green','-alpha',1,'-fullscreen',0,'-topmost',0)
    top['cursor']='arrow'
    setgem(160,360)#120,300
    keyboard.unhook_all()
    destroyer()
    f2=Frame(top)
    l2=Label(top,text='Save as:')
    l2.place(relx=.1,rely=.1,anchor='nw')
    e1=Entry(top,width=35)
    e1.place(relx=.5,rely=.4,anchor='c')
    fname,ind='',1
    if os.path.isfile('Record.mp4'):
        fname='Record.mp4'
    else:
        while 1:
            fname='Record'+str(ind)+'.mp4'
            if os.path.isfile(fname):
                ind+=1
            else:
                break
    e1.insert(0,fname)
    sel=Button(f2,text='Save',command=setprocess)#Add Edit Button in the future
    c=Button(f2,text='Cancel',command=main)
    sel.pack(side=LEFT)
    c.pack(side=RIGHT)
    sel.focus()
    sel.bind('<Return>',lambda e:sel.invoke())
    c.bind('<Return>',lambda e:c.invoke())
    sel.bind('<Left>',lambda e:c.focus())
    c.bind('<Right>',lambda e:sel.focus())
    f2.place(relx=.9,rely=.8,anchor='se')
    top.deiconify()
def process():
    global lof,fname,total,c,hei,wid,ix,iy,var
    print(total)
    fcc=cv2.VideoWriter_fourcc('m','p','4','v')
    if var.get():
        output=cv2.VideoWriter('temp.mp4',fcc,len(lof)/total,(wid,hei))
    else:
        output=cv2.VideoWriter(fname,fcc,len(lof)/total,(wid,hei))
    for i in range(len(lof)):
        img,hcursor,(x,y)=lof[i][0],lof[i][1],lof[i][2]
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 35, 35)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0,0), hcursor)
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        hdc.DeleteDC()
        im = Image.frombuffer('RGB',(bmpinfo['bmWidth'], bmpinfo['bmHeight']),bmpstr, 'raw', 'BGRX', 0, 1)
        im=im.convert('RGBA')
        datas = im.getdata()
        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        im.putdata(newData)
        img.paste(im,(x-ix,y-iy),im)
        imn=numpy.array(img)
        #imn=cv2.resize(imn,vsiz
        imf=cv2.cvtColor(imn,cv2.COLOR_BGR2RGB)
        #cv2.imshow('something',imf)
        output.write(imf)
        c['value']=int((i+1)*300/len(lof))
    output.release()
    if var.get():
        c.start(25)
        l2['text']='Packing Audio...'
        clip1=me.VideoFileClip('temp.mp4')
        clip2=clip1.set_audio(me.AudioFileClip('temp.wav'))
        clip2.write_videofile(fname)
        os.remove('temp.mp4')
        os.remove('temp.wav')
    toast=ToastNotifier()
    toast.show_toast('ScreenRecorder','Video Saved! Click to play.',icon_path='D:/Python/logox.ico',
    duration=5,threaded=True,callback_on_click=complete)
    main()
def run():
    global psd,cncld,lof,ix,iy,wid,hei,tcount,total,stream,file,var
    while 1:
        if psd:
            if tcount:
                total+=time.mktime(time.localtime())-tcount
                tcount=0
            cv2.waitKey(10)
            continue
        if tcount==0:
            tcount=time.mktime(time.localtime())
        if cncld:#if the length of the audio codec does not match the length of video,try setting the final value of tcount here
            cncld=psd=False
            if var.get():
                stream.stop()
                file.close()
            break
        try:
            img=ImageGrab.grab(bbox=(ix,iy,ix+wid,iy+hei))
            flags, hcursor, (x,y) = win32gui.GetCursorInfo()
            lof.append([img,hcursor,(x,y)])
        except:
            pass
def record(event):
    global output,wid,hei,vsize,psd,tcount,p,stream,file,var
    if hei<100 or wid<100:
        messagebox.showerror('Error!','Selected Area is Too Small.')
        return
    destroyer()
    top['cursor']='none'
    setgem(300,300)
    top['bg']='black'
    top.wm_attributes('-alpha',0,'-fullscreen',0)
    l2=Label(top,bg='black',font=('Calibri',200),fg='white',text='3')
    l2.pack(fill='both',expand=1)
    def chalpha(cnt,disp):
        global psd,total,streamm,var
        if cnt<0:
            cnt=1
            disp-=1
            l2['text']=str(disp)
        else:
            if disp==0:
                keyboard.hook_key('F1',lambda e:plpa(),suppress=True)
                keyboard.hook_key('F2',lambda e:stop(),suppress=True)
                l2.destroy()
                top.withdraw()
                total=0
                psd=False
                if var.get():
                    stream.start()
                return
            cnt-=0.1
            top.wm_attributes('-alpha',cnt)
        top.after(50,chalpha,cnt,disp)
    xf=threading.Thread(target=run)
    if os.path.isfile('temp.wav'):
        os.remove('temp.wav')
    if var.get():
        file=sf.SoundFile('temp.wav',mode='x',samplerate=44100,channels=2)
    psd,tcount=True,0
    xf.start()
    chalpha(1,3)
    pass
def select():
    global c,m,n,s,w,e,ne,nw,se,sw,wor,e1
    fpath=e1.get()
    if os.path.isdir(fpath)!=1:
        messagebox.showerror('Error!','The Given Directory Does Not Exist.')
        return
    os.chdir(fpath)
    destroyer()
    top.wm_attributes('-transparentcolor','black','-alpha',0.3,'-fullscreen',1,'-topmost',1)#topmost
    top.overrideredirect(1)
    top['cursor']='tcross'
    c=Canvas(top,bg='black')
    m=Toplevel(top)
    m.wm_attributes('-alpha',0.002,'-topmost',1)
    m.overrideredirect(1)
    m.withdraw()
    wor=False
    n=Label(m,bg='red',cursor='size_ns')
    s=Label(m,bg='red',cursor='size_ns')
    w=Label(m,bg='red',cursor='size_we')
    e=Label(m,bg='red',cursor='size_we')
    nw=Label(m,bg='blue',cursor='size_nw_se')
    sw=Label(m,bg='blue',cursor='size_ne_sw')
    ne=Label(m,bg='blue',cursor='size_ne_sw')
    se=Label(m,bg='blue',cursor='size_nw_se')
    top.bind('<B1-Motion>',printco)
    top.bind('<ButtonRelease-1>',setn)#The problem is because of this
    top.bind('<F1>',record)
    top.bind('<Escape>',lambda e:main())
    m.bind('<B1-Motion>',move)
    for i in [m,n,s,e,w,ne,nw,se,sw]:
        i.bind('<Button-1>',sm)
        i.bind('<ButtonRelease-1>',release)
    n.bind('<B1-Motion>',lambda e:resize(e,'n'))
    s.bind('<B1-Motion>',lambda e:resize(e,'s'))
    e.bind('<B1-Motion>',lambda e:resize(e,'e'))
    w.bind('<B1-Motion>',lambda e:resize(e,'w'))
    ne.bind('<B1-Motion>',lambda e:resize(e,'ne'))
    nw.bind('<B1-Motion>',lambda e:resize(e,'nw'))
    se.bind('<B1-Motion>',lambda e:resize(e,'se'))
    sw.bind('<B1-Motion>',lambda e:resize(e,'sw'))
def drawgrips():
    global hei,wid,ix,iy,n,s,e,w,ne,se,nw,sw
    n.place(x=10,y=0,height=10,width=wid-20)
    s.place(x=10,y=hei-10,height=10,width=wid-20)
    w.place(y=10,x=0,height=hei-20,width=10)
    e.place(y=10,x=wid-10,width=10,height=hei-20)
    nw.place(x=0,y=0,height=10,width=10)
    sw.place(x=0,y=hei-10,height=10,width=10)
    ne.place(x=wid-10,y=0,height=10,width=10)
    se.place(x=wid-10,y=hei-10,height=10,width=10)
def hidegrips():
    global n,s,e,w,ne,se,nw,sw
    for i in [n,e,s,w,ne,se,nw,sw]:
        i.place_forget()
def resize(event,mode):#the fuckin event.y is relative to the fuckin Label
    global xdif,ydif,hei,wid,ix,iy,wor,phei,pey,pwid,pex
    if wor==False:wor=True
    c.place_forget()
    if mode=='n':
        if phei>=event.y:
            iy=pey+event.y
        else:
            if iy!=pey+phei:iy=pey+phei
        hei=phei-event.y
        c.place(x=ix,y=iy,height=abs(hei),width=wid)
    elif mode=='s':
        if phei+event.y>=0:
            if iy!=pey:iy=pey
        else:
            iy=pey+phei+event.y
        hei=phei+event.y
        c.place(x=ix,y=iy,height=abs(hei),width=wid)
    elif mode=='w':
        if pwid>=event.x:
            ix=pex+event.x
        else:
            if ix!=pex+pwid:ix=pex+pwid
        wid=pwid-event.x
        c.place(x=ix,y=iy,height=hei,width=abs(wid))
    elif mode=='e':
        if pwid+event.x>=0:
            if ix!=pex:ix=pex
        else:
            ix=pex+pwid+event.x
        wid=pwid+event.x
        c.place(x=ix,y=iy,height=hei,width=abs(wid))
    elif mode=='nw':
        if phei>=event.y:
            iy=pey+event.y
        else:
            if iy!=pey+phei:iy=pey+phei
        if pwid>=event.x:
            ix=pex+event.x
        else:
            if ix!=pex+pwid:ix=pex+pwid
        hei=phei-event.y
        wid=pwid-event.x
        c.place(x=ix,y=iy,height=abs(hei),width=abs(wid))
    elif mode=='ne':
        if phei>=event.y:
            iy=pey+event.y
        else:
            if iy!=pey+phei:iy=pey+phei
        if pwid+event.x>=0:
            if ix!=pex:ix=pex
        else:
            ix=pex+pwid+event.x
        hei=phei-event.y
        wid=pwid+event.x
        c.place(x=ix,y=iy,height=abs(hei),width=abs(wid))
    elif mode=='sw':
        if phei+event.y>=0:
            if iy!=pey:iy=pey
        else:
            iy=pey+phei+event.y
        if pwid>=event.x:
            ix=pex+event.x
        else:
            if ix!=pex+pwid:ix=pex+pwid
        hei=phei+event.y
        wid=pwid-event.x
        c.place(x=ix,y=iy,height=abs(hei),width=abs(wid))
    elif mode=='se':
        if phei+event.y>=0:
            if iy!=pey:iy=pey
        else:
            iy=pey+phei+event.y
        if pwid+event.x>=0:
            if ix!=pex:ix=pex
        else:
            ix=pex+pwid+event.x
        hei=phei+event.y
        wid=pwid+event.x
        c.place(x=ix,y=iy,height=abs(hei),width=abs(wid))
def sm(event):
    global xdif,ydif,ix,iy,phei,pey,pwid,pex
    m.withdraw()
    xdif=event.x-ix;ydif=event.y-iy;phei=hei;pey=iy;pwid=wid;pex=ix
def move(event):
    global xdif,ydif,hei,wid,ix,iy,wor
    if wor==True:
        return
    c.place_forget()
    ix=event.x-xdif
    iy=event.y-ydif
    c.place(x=ix,y=iy,height=hei,width=wid)
def release(event):
    global xdif,ydif,ix,iy,wor,hei,wid
    wor=False;hei=abs(hei);wid=abs(wid)
    m.geometry('%dx%d+%d+%d'%(wid,hei,ix,iy))
    drawgrips()
    m.deiconify()
def retcoord(event):
    global ix,iy
    px,py=ix,iy
    if event.y<iy:
        py=event.y
    if event.x<ix:
        px=event.x
    return px,py,abs(event.y-iy),abs(event.x-ix)
def setn(event):
    global ix,iy,hei,wid,redraw
    if redraw==False:
        return
    px,py,h,w=retcoord(event)
    m.geometry('%dx%d+%d+%d'%(w,h,px,py))
    m.deiconify()
    redraw=False
    ix=px;iy=py;hei=h;wid=w
    drawgrips()
def printco(event):
    global ix,iy,c,redraw
    if redraw==False:
        hidegrips()
        m.withdraw()
        ix=event.x
        iy=event.y
        redraw=True
        return
    px,py,h,w=retcoord(event)
    c.place_forget()
    c.place(x=px,y=py,height=h,width=w)
main()
top.mainloop()
