# the cal class
'''
the calendar
origin one
function:
1.show the days of a month
2.show the front and the next month
nedd adding:
1.set time
2.select date
3.add "what-to-do"
'''
from Tkinter import *
#----------------------------------------------------------
#calculate the date
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
#--------------------------------------------------------------------------
#class the Tag
class Tag:
    def __init__(self,can,string,length,x,y,ta):
        self.can=can
        self.id=can.create_text(x,y,text=string,tags=ta)
        self.idn=can.create_rectangle(x-float(length)/2,y-float(length)/2,\
                                      x+float(length)/2,y+float(length)/2,\
                                      width=0,tags=ta)
    def setFill(self,color):
        self.can.itemconfigure(self.idn,fill=color)
#---------------------------------------------------------------------------
#the calculations
def outx(x):
    if (x%7):
        return x%7+1
    else: return 8
def outy(x):
    return 3+(x-1)/7
#---------------------------------------------------------------------------
#the calendar class
class Cal:
    def __init__(self,can,year,month): #canvas --- square
        self.change=0
        self.year=year
        self.month=month
        self.days_num=monthdays(self.month,self.year)
        self.can=can
        self.m = which_day(self.month,self.year)
        self.l = eval(self.can["width"])/10.0
        self.label=str(self.year)+'  '+['Jan','Feb','Mar','Apr','May','Jun',\
                                        'Jul','Aug','Sep','Oct','Nov',\
                                        'Dec'][self.month-1]
        self.list=[]
        self.buttona=Button(command=self.changem,text='<')
        self.buttonb=Button(command=self.changep,text='>')
        self.draw()
    def changep(self):
        self.change = 1
        self.update()
        self.change = 0
    def changem(self):
        self.change = -1
        self.update()
        self.change = 0
    def update(self,year=0,month=0):
        if self.change:
            if self.month+self.change==0:
                self.year -= 1
                self.month = 12
            elif self.month+self.change==13:
                self.year += 1
                self.month = 1
            else:
                self.month += self.change
        else:
            if year and month:
                self.year=year
                self.month=month
            else: pass
        self.days_num=monthdays(self.month,self.year)
        self.m = which_day(self.month,self.year)
        self.label=str(self.year)+'  '+['Jan','Feb','Mar','Apr','May','Jun',\
                                        'Jul','Aug','Sep','Oct','Nov',\
                                        'Dec'][self.month-1]
        self.list=[]
        self.can.delete('tag')
        self.draw()
    def draw(self):
        self.can.create_window(self.l*2,self.l,window=self.buttona,\
                               height=self.l,width=self.l,tags='tag')
        self.can.create_window(self.l*8,self.l,window=self.buttonb,\
                               height=self.l,width=self.l,tags='tag')
        self.can.create_text(self.l*5,self.l,text=self.label,tags='tag')
        for i in range(1,8):
            Tag(self.can,['Mo','Tu','We','Th','Fr','Sa','Su'][i-1],\
                self.l,outx(i)*self.l,2*self.l,ta='tag')
        for i in range(1,self.m):
            Tag(self.can,"",self.l,outx(i)*self.l,outy(i)*self.l,ta='tag')
        for i in range(self.m,self.m+self.days_num):
            self.list.append(Tag(self.can,str(i-self.m+1),self.l,\
                                 outx(i)*self.l,outy(i)*self.l,ta='tag'))

#-----------------------------------------------------------------------------
def test():
    root=Tk()
    c=Canvas(root,width=400,height=400)
    new=Cal(c,1900,1)
    c.grid()
    root.mainloop()
if __name__ == "__main__":
    test()
