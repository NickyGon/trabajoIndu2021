import re
from tkinter import*
from tkinter import ttk
import random
import time
import io
import datetime
import base64
from tkinter import messagebox
import tkinter
import urllib.request
from PIL import Image, ImageTk

import os
import requests
from io import BytesIO
# instalarse para su ejecucion en otro lado
import mysql.connector

class Web:
    def __init__(self, root):
        self.root=root
        self.root.title("WikiCan")
        self.root.geometry("1300x800")
        self.root.resizable(0,0)
        self.root.configure(background="#f6f6f2")
        lblTitle=Label(self.root,bd=10,relief=RAISED,text="WikiCan: Sobre y para cada raza de can",fg="#388087",bg="#6fb3b8",font=("lucida sans unicode",30,"bold"))
        lblTitle.pack(side=TOP,anchor=CENTER)

        # ========================DataFrame=================================

        Dataframe=Frame(self.root,bd=5,relief=RIDGE,bg="#badfe7")
        Dataframe.place(x=0,y=80,width=1300,height=550)

        # ======================ScrollDB====================================

        WikiFrame=LabelFrame(Dataframe,relief=RIDGE,bd=5,bg="#badfe7",font=("lucida sans unicode",12,"bold"),text="Razas de Perros")
        WikiFrame.place(x=10,y=10,width=500,height=500)
        
        canvasScroll=Canvas(WikiFrame,bg="#f6f6f2")
        WikiFrame.update()
        self.setWiki(WikiFrame.winfo_width()-455)
        scroller=Scrollbar(WikiFrame,orient="vertical",command=canvasScroll.yview)
        self.scrollerFrame=Frame(canvasScroll)

        self.scrollerFrame.bind(
            "<Configure>",
            lambda e: canvasScroll.configure(
                scrollregion=canvasScroll.bbox("all")
            )
           
        )

        canvasScroll.create_window((0,0), window=self.scrollerFrame, anchor="nw")
        canvasScroll.configure(yscrollcommand=scroller.set)
        canvasScroll.pack(side="left",fill="both",expand=True)
        scroller.pack(side="right",fill="y")

        self.infoFrame=LabelFrame(Dataframe,bd=5,relief=RIDGE,bg="#badfe7",font=("lucida sans unicode",12,"bold"),text="Información")
        self.infoFrame.place(x=550,y=10,width=710,height=500)
        self.infoFrame.update()

        # =====================================Info title=======================================


       


        self.iB()
    
        

    attributes=[]
    photos=[]
    img=[]
    paths=[]
    buttonsList=[]
    wikiSize=0

    def getRid(self):
        for widgets in self.infoFrame.winfo_children():
            widgets.destroy()


    def show(self,name,photo):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        select="select * from dogbreeds where titulo= %(title)s"
        cursor.execute(select,{'title':name})
        rows=cursor.fetchall()
        self.getRid()
        TitAndEdit=Frame(self.infoFrame,relief=RIDGE,bg="blue",width=self.infoFrame.winfo_width())
        TitAndEdit.pack(fill=X)
        Title=Label(TitAndEdit,bg="red",text=rows[0][1])
        Title.pack(side=LEFT,expand=True,fill=BOTH)
        canvas = Canvas(TitAndEdit,width=100, height = 100,bg="#388087")  
        canvas.pack(side=RIGHT)  
        imgae=ImageTk.PhotoImage(Image.open(os.getcwd()+photo).resize((120,120)))
        self.imga=imgae
        canvas.create_image(0, 0, anchor=NW, image=imgae) 

    def setWiki(self,inte):
        self.wikiSize=inte
    
    
    def iB(self):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        cursor.execute("select titulo,foto from dogbreeds order by titulo")
        rows=cursor.fetchall()
       
        for i in rows:
            self.attributes.append(i[0])
            self.photos.append(i[1])

        FILE_PATH='images/'   
        for i in range(len(self.photos)):
          self.url_to_jpg(i,self.photos[i],FILE_PATH)

        for i in range(len(self.attributes)):
           pathe="\images\image-{}.jpg".format(i)
           self.paths.append(pathe)
           frame=Frame(self.scrollerFrame,height=3,width=100,bg="#c2edce")
           frame.pack()
           canvas = Canvas(frame,width=100, height = 100,bg="#388087")  
           canvas.pack(side=LEFT)  
           self.img.append(ImageTk.PhotoImage(Image.open(os.getcwd()+pathe).resize((100,100))))
           self.img[i]=self.img[i]
           canvas.create_image(0, 0, anchor=NW, image=self.img[i]) 
           frame.update()
           self.buttonsList.append(Button(frame,width=self.wikiSize-10,height=3,bg="#6fb3b8",text=self.attributes[i],font=("lucida sans unicode",12,"bold"),command=lambda c=i: self.show(self.buttonsList[c].cget("text"),self.paths[c])))
           self.buttonsList[i].pack(side=RIGHT)

        conn.commit()
        conn.close()

    def url_to_jpg(self,i,url,filepath):
        filename= 'image-{}.jpg'.format(i)
        full_path ='{}{}'.format(filepath,filename)
        urllib.request.urlretrieve(url,full_path)
        print('{} saved. '.format(filename))
  
root=Tk()
ob=Web(root)
root.mainloop()
