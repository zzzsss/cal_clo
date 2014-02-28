#the standard time class
from Tkinter import *
import time

Month_days = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:31,12:31}
Month_names = ['January','Februry','March','April','May','June','July',\
               'August','September','October','November','December']
W_names = ['Monday','Tuesday','Wednesday','Thursday','Friday',\
           'Saturday','Sunday']
#formal
def formal1(x):
    x = str(x)
    if len(x)==1:
        x = '0'+x
    return x
def formal2(x):
    while x!="" and x[0]=='0':
        x = x[1:]
    if x=="":
        f=0
    else:
        f = eval(x)
    return f
#count days
def yeardecide(x):
    if (x%4==0 and x%100!=0) or x%400==0:
        return 1
    else: return 0
def monthdays(x,y): # x is the month and y is the year
    if x in [1,3,5,7,8,10,12]:
        return 31
    elif x==2:
        if yeardecide(y)==1:
            return 29
        else: return 28
    else: return 30
def yeardays(y): # y is the year
    m = 365 + yeardecide(y)
    return m
def which_day(x,y): # x is the month and y is the year
    m = 0
    if y>=1900:
        for i in range(1900,y):
            m = m + yeardays(i)
        for i in range(1,x):
            m = m + monthdays(i,y)
        m = (m % 7) + 1
    else:
        for i in range(y,1900):
            m = m + yeardays(i)
        for i in range(1,x):
            m = m - monthdays(i,y)
        m = 7-(m % 7) + 1
    return m
def what_day(x,y,z):
    k=which_day(y,x)+z-2
    if k<0:
        k=k+7
    return k%7
#moving days
def forward_oneday(date):
    year = date[0]
    month = date[1]
    day = date[2]
    wday = date[3]
    if month==12 and day==31:
        year += 1
        month,day=1,1
    elif month in [1,3,5,7,8,10,12]:
        if day==31:
            month += 1
            day = 1
        else:
            day += 1
    elif month == 2:
        if day==28+yeardecide(year):
            month,day=3,1
        else:
            day += 1
    else:
        if day==30:
            month += 1
            day = 1
        else:
            day += 1
    wday=(wday+1)%7
    return [year,month,day,wday]
#std date
def std_date():
    x=time.localtime()
    return [x.tm_year,x.tm_mon,x.tm_mday,x.tm_wday]
    
class std_T:
    #list1 year,month,date,day
    #list2 hour,minute,second
    def __init__(self,list1=[],list2=[]):
        self.date_l=list1
        self.time_l=list2
        if len(list1)==0:
            self.date_l=std_list1()
        if len(list2)==0:
            self.time_l=std_list2()
        
