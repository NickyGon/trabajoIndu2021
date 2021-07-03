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
from PIL import Image

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
        lblTitle=Label(self.root,bd=10,relief=RAISED,text="WikiCan: Sobre y para cada raza de can",fg="#169bff",bg="#aad4ff",font=("lucida sans unicode",30,"bold"))
        lblTitle.pack(side=TOP,fill=X)

        # ========================DataFrame=================================

        Dataframe=Frame(self.root,bd=5,relief=RIDGE,bg="#f3fbff")
        Dataframe.place(x=0,y=80,width=1300,height=550)

        # ======================ScrollDB====================================

        WikiFrame=LabelFrame(Dataframe,relief=RIDGE,bd=5,bg="#f3fbff",font=("lucida sans unicode",12,"bold"),text="Razas de Perros")
        WikiFrame.place(x=10,y=10,width=500,height=500)
        
        canvasScroll=Canvas(WikiFrame,bg="cyan")
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

        infoFrame=LabelFrame(Dataframe,bd=5,relief=RIDGE,bg="#f3fbff",font=("lucida sans unicode",12,"bold"),text="Información")
        infoFrame.place(x=550,y=10,width=710,height=500)

        self.iB()
    
        

    attributes=[]
    photos=[]
    buttonsList=[]
    wikiSize=0

    def show(self,name):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        select="select * from dogbreeds where titulo= %(title)s"
        cursor.execute(select,{'title':name})
        rows=cursor.fetchall()
        print("SI!")

    def setWiki(self,inte):
        self.wikiSize=inte
    
    
    def iB(self):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        cursor.execute("select titulo,foto from dogbreeds")
        rows=cursor.fetchall()
       
        for i in rows:
            self.attributes.append(i[0])
            self.photos.append(i[1])

        FILE_PATH='images/'   
      #  for i in range(len(self.photos)):
       #     self.url_to_jpg(i,self.photos[i],FILE_PATH)

        for i in range(len(self.attributes)):
            self.buttonsList.append(Button(self.scrollerFrame,width=self.wikiSize,height=5,bg="blue",compound=LEFT,text=self.attributes[i],font=("lucida sans unicode",12,"bold"),command=lambda c=i: self.show(self.buttonsList[c].cget("text"))))
            self.buttonsList[i].pack() 
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