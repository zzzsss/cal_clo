# the clock class
'''
the clock (origin one)
function:
1.run like a clock
2.set time
3.add alarms(just add labels)
need adding:
1.finish the alarms and sth about it
'''

from Tkinter import *
from time import *
from math import *
import re,threading
#------------------------------------------------------------
def formal1(x):
    x = str(x)
    if len(x)==1:
        x = '0'+x
    return x
def formal2(x):     
    if x[0]=='0':
        f=eval(x[1])
    else:
        f = eval(x)
    return f
#----------------------------------------------------------
# the alarm clock class and other classes
class Ala:
    '''
    style:
    c:common e:everyday
    '''
    def __init__(self,clo,hour,minute,music,date,style,wide,repeat=0):
        self.time = [hour,minute]
        self.date = date
        self.music = music
        self.clock = clo
        self.style = style
        self.repeat = repeat
        self.wide=wide
        if self.style == 'c':
            self.label = Label(text=self.time[0]+':'+self.time[1]\
                               +'  '+formal1(self.date[0])+' '+\
                               formal1(self.date[1])+' '\
                               +formal1(self.date[2]),width=self.wide,\
                               bg="lightblue")
        elif self.style == 'e':
            self.label = Label(text=self.time[0]+':'+self.time[1]\
                               +'  '+'e',bg='lightgreen',width=self.wide)
    def get_label(self):
        return self.label
    def add_order(self,number):
        self.label["text"] = "%-3d"%(number)+self.label["text"]
class Ala_Mapping(Canvas):
    def __init__(self,root,height,width,unit):
        self.root=root
        self.h=height
        self.w=width
        self.unit=unit
        Canvas.__init__(self,self.root,height=self.h,width=self.w)
        self.list=[]
    def add_one(self,a):
        a.add_order(len(self.list))
        self.list.append(a)
        self["scrollregion"]=(0,0,self.w,self.unit*len(self.list))
        self.create_window(self.w/2.0,len(self.list)*self.unit,anchor=S,\
                           window=a.get_label())

class Ala_box:
    def __init__(self,date):
        self.t = Toplevel()
        self.date=date
        another = self.t
        self.t_l=[Label(another,text="hour"),Label(another,text="minute")
             ,Label(another,text="music"),Label(another,text="year")
             ,Label(another,text="month"),Label(another,text="day")
             ,Label(another,text="style"),Label(another,text="repeat")
             ,Entry(another),Entry(another),Entry(another),Entry(another)
             ,Entry(another),Entry(another),Entry(another),Entry(another)]
        self.t_l[11].insert(0,str(self.date[0]))
        self.t_l[12].insert(0,str(self.date[1]))
        self.t_l[13].insert(0,str(self.date[2]))
        self.t_l[14].insert(0,'c')
        self.t_l[15].insert(0,0)
        for i in range(8):
            self.t_l[i].grid(column=0,row=i)
            self.t_l[i+8].grid(column=1,row=i)
        self.b1 = Button(self.t,text='sure',command=self.sure)
        self.b2 = Button(self.t,text='cancel',command=self.cancel)
        self.b1.grid(column=0,row=16)
        self.b2.grid(column=1,row=16)
        self.t.mainloop()
    def cancel(self):
        self.value=0
        self.t.quit()
        self.t.destroy()
    def sure(self):
        self.value=1
        self.out=[self.t_l[i].get() for i in range(8,16)]
        self.t.quit()
        self.t.destroy()
class T_box:
    def __init__(self):
        self.t = Toplevel()
        self.l1=Label(self.t,text=" Hour :")
        self.l2=Label(self.t,text="Minute:")
        self.l3=Label(self.t,text="Second:")
        self.e1=Entry(self.t)
        self.e2=Entry(self.t)
        self.e3=Entry(self.t)
        self.l1.grid(column=0,row=0)
        self.l2.grid(column=0,row=1)
        self.l3.grid(column=0,row=2)
        self.e1.grid(column=1,row=0)
        self.e2.grid(column=1,row=1)
        self.e3.grid(column=1,row=2)
        self.b1 = Button(self.t,text='sure',command=self.sure)
        self.b2 = Button(self.t,text='cancel',command=self.cancel)
        self.b1.grid(column=0,row=3)
        self.b2.grid(column=1,row=3)
        self.t.mainloop()
    def cancel(self):
        self.value=0
        self.t.quit()
        self.t.destroy()
    def sure(self):
        self.value=1
        self.out=[self.e1.get(),self.e2.get(),self.e3.get()]
        self.t.quit()
        self.t.destroy()
#--------------------------------------------------------------------
class Clo(Canvas): 
    def __init__(self,root,length,date): #canvas -- rectangle 1:2 #date [#,#,#]
        Canvas.__init__(self,root,height=length*2,width=length)
        self.alive=1
        self.date=date 
        self.stdtime()
        self.time=[self.hour,self.minute,self.second]
        self.label=formal1(self.time[0])+':'+formal1(self.time[1])+':'\
                    +formal1(self.time[2])
        self.unit = length/10.0
        self.c=self.create_oval(self.coords_x(1),self.coords_y(1),\
                                self.coords_x(9),self.coords_y(9),\
                                width=2,tags="origin")
        self.create_oval(self.coords_x(5)-self.unit/10,\
                         self.coords_y(5)-self.unit/10,\
                         self.coords_x(5)+self.unit/10,\
                         self.coords_y(5)+self.unit/10,\
                         fill='blue',tags="origin")
        for i in range(1,13):
            self.create_oval(self.coords_x(5+3*sin(pi*i/6))-self.unit/10,\
                             self.coords_y(5+3*cos(pi*i/6))-self.unit/10,\
                             self.coords_x(5+3*sin(pi*i/6))+self.unit/10,\
                             self.coords_y(5+3*cos(pi*i/6))+self.unit/10,\
                             fill='blue',tags="origin")
            self.create_text(self.coords_x(5+3.5*sin(pi*i/6.0)),\
                             self.coords_y(5+3.5*cos(pi*i/6.0)),\
                             text=str(i),tags="origin")
        self.button_set=Button(text='Set',command=self.sett)
        self.button_alarm=Button(text='Alarm',command=self.alarm)
        self.create_window(self.unit*3,self.unit*11,height=int(self.unit),\
                           width=int(self.unit*2.5),window=self.button_set,\
                           tags="origin")
        self.create_window(self.unit*7,self.unit*11,height=int(self.unit),\
                           width=int(self.unit*2.5),window=self.button_alarm,\
                           tags="origin")
        self.alarm_map=Ala_Mapping(None,height=int(self.unit*7),width=\
                                   int(self.unit*8),unit=self.unit)
        self.create_window(self.unit*5,self.unit*15.5,window=self.alarm_map,\
                           tags="origin")
        self.scrollY = Scrollbar(orient=VERTICAL,command=self.alarm_map.yview)
        self.create_window(self.unit*9,self.unit*15.5,window=self.scrollY,\
                           tags="origin",height=int(self.unit*7))
        self.alarm_map["yscrollcommand"]=self.scrollY.set
        self.update()
       
    def add_alarm(self,hour,minute,music,date,style,repeat=0):
        self.alarm_map.add_one(Ala(self,hour,minute,music,date,\
                                   style,repeat=0,wide=20))
    def alarm(self):
        x = Ala_box(self.date)
        if x.value:
            date_list=[formal2(x.out[i]) for i in [3,4,5]]
            self.add_alarm(x.out[0],x.out[1],x.out[2],date_list,x.out[6],\
                           eval(x.out[7]))
        else:
            pass
    def set_time(self,hour,minute,second):
        self.hour=formal2(hour)
        self.minute=formal2(minute)
        self.second=formal2(second)
        self.update()
    def sett(self):
        x = T_box()
        if x.value:
            self.set_time(x.out[0],x.out[1],x.out[2])
        else: pass
    def stdtime(self):
        t = re.search("([0-9]+):([0-9]+):([0-9]+)",ctime()).groups()
        self.hour=formal2(t[0])
        self.minute=formal2(t[1])
        self.second=formal2(t[2])
    def coords_y(self,y): # -10<y<10
        return (10-y)*self.unit
    def coords_x(self,x): # x<=10
        return self.unit*x
    def update(self):
        self.delete('change')
        self.create_line(self.unit*5,self.unit*5,\
                                     self.coords_x(5+2*sin(pi*self.hour/6+pi\
                                                           *self.minute/360)),\
                                     self.coords_y(5+2*cos(pi*self.hour/6+pi\
                                                           *self.minute/360)),\
                                     fill='red',width=3,tags='change')
        self.create_line(self.unit*5,self.unit*5,\
                                    self.coords_x(5+3*sin(pi*self.minute/30)),\
                                    self.coords_y(5+3*cos(pi*self.minute/30)),\
                                    width=2,tags='change')
        self.create_line(self.unit*5,self.unit*5,\
                                    self.coords_x(5+3*sin(pi*self.second/30)),\
                                    self.coords_y(5+3*cos(pi*self.second/30)),\
                                    width=1,fill='blue',tags='change')
        self.create_text(self.coords_x(5),self.coords_y(4),\
                                     text=formal1(self.hour)+':'\
                                     +formal1(self.minute)+\
                                     ':'+formal1(self.second),tags='change')
    #run the clock
    def go_one(self):
        if self.second==59:
            if self.minute==59:
                if self.hour==23:
                    self.hour=0
                    self.minute=0
                    self.second=0
                else:
                    self.hour += 1
                    self.minute=0
                    self.second=0
            else:
                self.minute += 1
                self.second = 0
        else:
            self.second += 1
        if self.alive:
            self.update()
        else: pass
    def run_clock(self):
        while self.alive:
            sleep(1)
            self.go_one()
    def dying(self):
        self.alive=0
#----------------------------------------------------------------------
def test():
    root=Tk()
    c = Clo(root,200,[2012,2,3])
    c.grid()
    t=threading.Thread(target=c.run_clock,args=())
    t.start()
    root.mainloop()
    c.dying()
if __name__ == "__main__":
    test()
    
        
