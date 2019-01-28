# Importing Libraries- Tkinter, CSV, numpy and pandas
from tkinter import *
from tkinter import filedialog
import csv
from tables import createStandardTable as cst
import numpy as np
import pandas as pd

# Declaring Variables of list datastructure for sorting.
pr, tim, air, depart, arrival, source, destination, duration, stopage, prgo = [], [], [], [], [], [], [], [], [], []
timgo, airgo, sourcegp, destgo, dash, flightnumgo, airname = [], [], [], [], [], [], []
departgo, arrivego, airname, flynum, finalgo, stopage2, final, airname1, flight1 = [], [], [], [], [], [], [], [], []


#Creating TK() object
window = Tk()

# Declaring all the functions
# Functions for taking inputs
def inputFrom():
    mText=fromCity.get()
    #mlabel1 = Label(tableFrame3,text=mText).grid()
def inputTo():
    mText=toCity.get()
    #mlabel1 = Label(tableFrame3,text=mText).grid()
def inputDepDate():
    mText=departDate.get()
    #mlabel1 = Label(tableFrame3,text=mText).grid()

def inputDepMon():
    mText=departMonth.get()
    #mlabel1 = Label(tableFrame3,text=mText).grid()
def mAbout():
    messagebox.showinfo(title="About",message="This is the about box")
def mQuit():
    mExit = messagebox.askyesno(title="Quit", message="Are you sure")
    if mExit > 0:
        window.destroy()

# Functions For Sorting       
def price_sort_increase(final):
    s=sorted(final,key=lambda x:x[7], reverse=False)   
    return s
def price_sort_decrease(final):
    s=sorted(final,key=lambda x:x[7], reverse=True)
    return s 
def sort_durationInc(flist):
    s=sorted(flist,key=lambda x:int(str(x[5][0])+str(x[5][3])+str(x[5][4])), reverse=False)
    return s 
def sort_durationDec(flist):
    s=sorted(flist,key=lambda x:int(str(x[5][0])+str(x[5][3])+str(x[5][4])), reverse=True)
    return s     

MMT = ["HYD", "MAA","BOM", "DEL", "CCU", "AMD", "BLR", "NAG", "CCJ", "PNQ"]
Ptm= ["HYD-Hyderabad","MAA-Chennai","BOM-Mumbai","DEL-Delhi","CCU-Kolkata","AMD-Ahmedabad","BLR-Bengaluru","NAG-Nagpur","CCJ-Kozhikode","PNQ-Pune"]

# Main Function where all the process happens
def run1():
    mtext1 = fromCity.get()
    mtext2 = toCity.get()
    mtext3 = departDate.get()
    mtext4 = departMonth.get()
    ptext1 = Ptm[MMT.index(mtext1)]
    ptext2 = Ptm[MMT.index(mtext2)]
    url = "https://flights.makemytrip.com/makemytrip/search/O/O/E/1/0/0/S/V0/"+mtext1+"_"+mtext2+"_"+mtext3+"-"+mtext4+"-2018?contains=false&remove="
    url2= "https://paytm.com/flights/flightSearch/"+ptext1+"/"+ptext2+"/1/0/0/E/2018-"+mtext4+"-"+mtext3
    from selenium import webdriver
    chrome_path = r"C:\Python27\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)
    driver2= webdriver.Chrome(chrome_path)
    driver.get(url)   
    driver2.get(url2)
    
    ##Getting data for make my trip
    airline_info = driver.find_elements_by_class_name("airline_info_detls")
    price = driver.find_elements_by_class_name("num")
    time = driver.find_elements_by_class_name("time_info")
    for post in price:      
        price=post.text
        price=price.replace(',','')
        price=int(price)
        pr.append(price)
        dash.append("-")        
    for post in airline_info:
        airline=post.text
        airline=airline.replace('\n',' ')
        air.append(airline)        
    for post in time :
        t=post.text
        tim.append(post.text)    
    conarray=[i+"\n"+j+"\n"+k for i,j,k in zip(tim[::3], tim[1::3],tim[2::3])]
    for element in conarray:
       parts = element.split('\n')
       depart.append(parts[0])
       source.append(parts[1])
       arrival.append(parts[2])
       destination.append(parts[3])
       duration.append(parts[4])
       stopage.append(parts[5])
    for k in range(0,len(pr)):
        final.append([air[k],source[k],depart[k],destination[k],arrival[k],duration[k],stopage[k],pr[k],dash[k]])
    newlist=sorted(final,key=lambda x:x[7], reverse=False) 
    
    ##Getting data for Paytm

    airline_info2 = driver2.find_elements_by_class_name("_3H-S")
    price2 = driver2.find_elements_by_class_name("_2gMo")
    fly=driver2.find_elements_by_class_name("NqXj")
    time2 = driver2.find_elements_by_class_name("vY4t")
    stopgo=driver2.find_elements_by_class_name("_7BOG")
    for post in price2:
        pri=post.text
        pri=pri.replace(',','')
        pri=int(pri)
        prgo.append(pri)    
    for post in stopgo:
        stopage2.append(post.text)        
    for post in airline_info2:
        airgo.append(post.text)        
    for post in time2 :
        timgo.append(post.text)   
    for post in fly :
        flynum.append(post.text)
    
    airname=airgo[::3]
    departgo=airgo[1::3]
    arrivego=airgo[2::3]
    flightnumgo=flynum[::4]
    flightnumgo = [w.replace(' ', '') for w in flightnumgo]
    sourcego=flynum[1::4]
    destgo=flynum[2::4]
    
    conarray2=[i+" "+j for i,j in zip(airname, flightnumgo)]
    for i in range(0,len(prgo)):         
      finalgo.append([conarray2[i],sourcego[i], departgo[i],destgo[i],arrivego[i],timgo[i],stopage2[i],prgo[i]])   
      newlist2=sorted(finalgo,key=lambda x:x[7], reverse=False)
       
    ##Checking and storing price for flights in Paytm into the array
    for j in range(0,len(newlist)):
        for i in range(0,len(newlist2)):
            if(newlist2[i][0]==newlist[j][0]):
                newlist[j][8]=(newlist2[i][7])
                break
    
    ## Exporting all the values into individual CSV files                
    finallist = newlist[:15]
    
    
    my_df1 = pd.DataFrame(finallist)
    my_df1.to_csv('finallist.csv', index=False, header=False)
    
    price_sort_increase1 = price_sort_increase(finallist)
    
    my_df2 = pd.DataFrame(price_sort_increase1)
    my_df2.to_csv('priceSortIncrease.csv', index=False, header=False)
    
    price_sort_decrease1 = price_sort_decrease(finallist)
    
    my_df3 = pd.DataFrame(price_sort_decrease1)
    my_df3.to_csv('priceSortDecrease.csv', index=False, header=False)
    
    sortDurationInc1 = sort_durationInc(finallist)
    
    my_df4 = pd.DataFrame(sortDurationInc1)
    my_df4.to_csv('sort_durationInc.csv', index=False, header=False)
    
    sortDurationDec1 = sort_durationDec(finallist)
    
    my_df5 = pd.DataFrame(sortDurationDec1)
    my_df5.to_csv('sort_durationDec.csv', index=False, header=False)


## Creating Frames for input, Sorting buttons and output
tableFrame = Frame(window, bg='cyan', width=450, height=50, pady=10)
tableFrame2 = Frame(window, bg='gray2', width=450, height=40, padx=50, pady=20)
tableFrame3 = Frame(window, bg = 'red', width = 450, height = 300, padx= 50, pady = 20)

# Creating the Variables for Inputs
fromCity = StringVar()
toCity = StringVar()
departDate = StringVar()
departMonth = StringVar()

#Declaring the title for the window
window.title('Web Mining - WEB SCRAPING FOR MAKE-MY-TRIP and PAYTM')


def tableFrames():
    tableFrame3.grid()
    tableFrame2.grid()
    tableFrame.grid()    

#create a global newtable grid.
f = open("my_csv.csv")
newtable = cst(f,tableFrame)

def createTableFrame():
    f = open("sort_durationDec.csv")
    global newtable
    newtable = cst(f,tableFrame)
    newtable.grid()
    
def Header():
    f = open("my_csv.csv")
    global newtable
    newtable = cst(f,tableFrame)
    newtable.grid()

def createTableFrame2():
    f = open("my_csv.csv")
    global newtable
    newtable = cst(f,tableFrame)
    newtable.grid()

def createTableFrame3():
    f = open("priceSortIncrease.csv")
    global newtable
    newtable = cst(f,tableFrame)
    newtable.grid()
    
def createTableFrame4():
    f = open("priceSortDecrease.csv")
    global newtable
    newtable = cst(f,tableFrame)
    newtable.grid()
    
def createTableFrame5():
    f = open("sort_durationInc.csv")
    global newtable
    newtable = cst(f,tableFrame)
    newtable.grid()

def ct():
    global newtable
    newtable.destroy()
    createTableFrame3()
    tableFrame.grid()  
    
def th():
    global newtable
    newtable.destroy()
    createTableFrame()
    tableFrame.grid()
    
def t2h():
    global newtable
    newtable.destroy()
    createTableFrame4()
    tableFrame.grid()
    
def t3h():
    global newtable
    newtable.destroy()
    createTableFrame5()
    tableFrame.grid()

def sorting():  
    Button(tableFrame2,text="Show Price Sort Increase",command=ct).grid(row = 0,column = 0 , padx = 15, pady = 10)
    Button(tableFrame2,text = "Show Price Sort Decrease", command = t2h).grid(row = 0,column = 1 , padx = 15, pady = 10)
    Button(tableFrame2,text = "Show Sort Duration Increase", command = t3h).grid(row = 0,column = 2 , padx = 15, pady = 10)
    Button(tableFrame2,text = "Show Sort Duration Decrease", command = th).grid(row = 0,column = 3 , padx = 15, pady = 10)
    
    


# Input
mLabel1 = Label(tableFrame3,text='FROM') 
mLabel1.grid(row=0,column = 0,sticky = W )
mEntry1 = Entry(tableFrame3,textvariable=fromCity).grid(row = 0,column = 1 , padx = 20, pady = 10)
mButton1 = Button(tableFrame3,text ='OK', command = inputFrom).grid(row=0,column = 2)  

mLabel2 = Label(tableFrame3,text='TO').grid(row=1,column = 0, sticky = W)
mEntry2 = Entry(tableFrame3,textvariable=toCity).grid(row=1,column = 1 , pady = 10)
mButton2 = Button(tableFrame3,text ='OK', command = inputTo).grid(row=1,column = 2)

mLabel3 = Label(tableFrame3,text='DATE').grid(row=2,column = 0, sticky = W)
mEntry3 = Entry(tableFrame3,textvariable=departDate).grid(row=2,column = 1, pady = 10)
mButton3 = Button(tableFrame3,text ='OK', command = inputDepDate).grid(row=2,column = 2)

mLabel4 = Label(tableFrame3,text='MONTH').grid(row=3,column = 0, sticky = W)
mEntry4 = Entry(tableFrame3,textvariable=departMonth).grid(row=3,column = 1, pady = 10)
mButton4 = Button(tableFrame3,text ='OK', command = inputDepMon).grid(row=3,column = 2)
    
mRun = Button(tableFrame3,text ='RUN', command = run1).grid(row = 4, column = 0, sticky = W)
    

tableFrames()
sorting()
Header()
createTableFrame2()


window.mainloop()