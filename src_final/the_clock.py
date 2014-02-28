# the clock class
from Tkinter import *
from time import *
from math import *
import re,threading
from std_time import *#self_defined
from winsound import *
#------------------------------------------------------------
'''
sth learned:
1.different threads --- mainloop and toplevel
2.different threads --- modify the same Tkinter or create new widget
3.menu.tk_popup --- cause mainloop stop
'''
#------------------------------------------------------------
def count_time(x,Ala):
    x = int(x)
    sleep(x)
    if Ala.question_left:
        Ala.cover_question()
def delay_count(date,time,h_f,m_f):#delay within a day
    minute=time[1]+m_f
    hour_p=minute/60
    minute=minute%60
    hour=time[0]+hour_p+h_f
    day_p=hour/24
    hour=hour%24
    if day_p!=0: # ==1 just foward one day
        date=forward_oneday(date)
    time=[hour,minute]
    return date,time
#----------------------------------------------------------
# the alarm clock class and other classes
class Ala:
    '''
    style:
    c:common e:everyday
    '''
    def __init__(self,clo,hour,minute,music,date,style,repeat,wide):
        self.questioned=0
        self.live=1
        self.time = [hour,minute]
        self.date = date
        self.music = music
        self.clock = clo
        self.style = style
        self.repeat = repeat
        self.wide=wide
        #self.rmenu=Menu(self.clock.alarm_map,tearoff=0)
        #self.rmenu.add_command(label="delete",command=self.get_remove)
        #self.rmenu.add_command(label="modify",command=self.get_modify)
        if self.style == 'c':
            self.label = Label(text=formal1(self.time[0])+':'+\
                               formal1(self.time[1])\
                               +'  '+formal1(self.date[0])+' '+\
                               formal1(self.date[1])+' '\
                               +formal1(self.date[2]),width=self.wide,\
                               bg="lightblue")
        elif self.style == 'e':
            self.label = Label(text=formal1(self.time[0])+':'+\
                               formal1(self.time[1])+'  '+'e',\
                               bg='lightgreen',width=self.wide)
        self.label.bind('<Button-1>',self.choice_out)
        self.label.bind('<Button-2>',self.choice_out)
        self.label.bind('<Button-3>',self.choice_out)
        self.label.bind('<Double-Button-1>',self.choice_out)
    def choice_out(self,but):
        self.top=Toplevel()
        b1=Button(self.top,text="delete",command=self.get_remove)
        b2=Button(self.top,text="modify",command=self.get_modify)
        b1.grid()
        b2.grid()
        self.top.mainloop()
    def get_remove(self):
        self.top.quit()
        self.top.destroy()
        self.clock.alarm_map.remove_one(self)
        self.clock.alarm_map.sweeping()
    def get_modify(self):
        self.top.quit()
        self.top.destroy()
        x = Ala_box(0,None,self)
        if x.value:
            date_list=[formal2(x.out[i]) for i in [3,4,5]]
            self._modify(formal2(x.out[0]),formal2(x.out[1]),x.out[2],\
                           date_list,x.out[6],eval(x.out[7]))
        else:
            pass
    def _modify(self,hour,minute,music,date_list,style,repeat):
        self.live=1
        self.time = [hour,minute]
        self.date = date_list
        self.music = music
        self.style = style
        self.repeat = repeat
        self.update_label()
    def get_label(self):
        return self.label
    def add_order(self,number):
        self.label["text"] = "%-3d"%(number)+self.label["text"]
    def get_tag(self):
        return self.tag
    def set_tag(self,x):
        self.tag='Is'+x
        self.update_label()
    def ring(self):
        another=threading.Thread(target=self._ring,args=())
        another.setDaemon(True)
        another.start()
        self.question()
        while 1:
            if self.questioned:
                self.clock.alarm_map.update_one(self)
                break
        self.questioned=0
    def _ring(self):
        try:
            PlaySound(self.music+'.wav',SND_ASYNC)
        except:
            PlaySound("I'm Yours.wav",SND_ASYNC)
    def question(self):
        self.question_left=1
        self.clock.create_window(self.clock.unit*5,self.clock.unit*12.5,\
                                 window=Label(text="It's time!!!"),\
                                 tags="question")
        self.clock.create_window(self.clock.unit*5,self.clock.unit*14,\
                                 window=Label(text="repeat or not?"),\
                                 tags="question")
        self.clock.create_window(self.clock.unit*5,self.clock.unit*15.5,window\
                                 =Label(text="%d times left."%(self.repeat)),\
                                 tags="question")
        self.clock.create_window(self.clock.unit*5,self.clock.unit*17,window=\
                                 Button(text="quit(not cancel)",\
                                        command=self.get_quit),tags="question")
        self.clock.create_window(self.clock.unit*5,self.clock.unit*18.5,window=\
                                 Button(text="quit and cancel",command\
                                        =self.get_cancel),tags="question")
        new_one=threading.Thread(target=count_time,args=(60,self))
        new_one.setDaemon(True)
        new_one.start()
    def cover_question(self):
        self.clock.move('question',0,1000*self.clock.unit) #move (like delete)
        self.repeat -= 1
        self.questioned=1
        self.question_left=0
        PlaySound('ALARM8',SND_PURGE) 
    def get_quit(self):
        self.clock.delete("question")
        self.repeat = self.repeat - 1
        self.questioned=1
        self.question_left=0
        PlaySound('ALARM8',SND_PURGE) 
    def get_cancel(self):
        self.clock.delete("question")
        self.repeat = -1
        self.questioned=1
        self.question_left=0
        PlaySound('ALARM8',SND_PURGE)
    def dying(self):
        self.live=0
    def living(self):
        self.live=1
    def get_delay(self,hour_f=0,minute_f=0):
        self.date=delay_count(self.date,self.time,hour_f,minute_f)[0]
        self.time=delay_count(self.date,self.time,hour_f,minute_f)[1]
        #print self.time
        self.update_label()
    def update_label(self):
        if self.style == 'c':
            self.label["text"]="%-3d"%(eval(self.tag[2:]))+\
                                formal1(self.time[0])+':'+formal1(self.time[1])\
                               +'  '+formal1(self.date[0])+' '+\
                               formal1(self.date[1])+' '\
                               +formal1(self.date[2])
        elif self.style == 'e':
            self.label["text"]="%-3d"%(eval(self.tag[2:]))+\
                                formal1(self.time[0])+':'+foraml1(self.time[1])\
                               +'  '+'e'

class Ala_Mapping(Canvas):
    def __init__(self,root,height,width,unit,clo=None):
        self.root=root
        self.h=height
        self.w=width
        self.unit=unit
        self.clo=clo
        Canvas.__init__(self,self.root,height=self.h,width=self.w)
        self.list=[]
    def add_one(self,a):
        #print self.list
        self.sweeping()
        self.clo.delete("question")
        a.add_order(len(self.list))
        a.set_tag(str(len(self.list)))
        self.list.append(a)
        self["scrollregion"]=(0,0,self.w,self.unit*len(self.list))
        self.create_window(self.w/2.0,len(self.list)*self.unit,anchor=S,\
                           window=a.get_label(),tags=a.get_tag())
    def remove_one(self,a):
        self.list.remove(self.list[eval(a.get_tag()[2:])])
        self.move(a.get_tag(),0,100)
        self.delete(a.get_tag())
        self["scrollregion"]=(0,0,self.w,self.unit*len(self.list))
    def remove_one_s(self,a):
        self.list.remove(self.list[eval(a.get_tag()[2:])])
        self.move(a.get_tag(),self.unit*1000,0)
        self["scrollregion"]=(0,0,self.w,self.unit*len(self.list))
    def update_one(self,i):
        if i.style=='c':
            if i.repeat<0:
                i.dying()
                self.remove_one_s(i)
            else:#5 minutes delayed
                i.living()
                i.get_delay(minute_f=5)
        elif i.style=='e':
            if i.repeat<0:
                i.dying()
            else:
                i.living()
                i.get_delay(minute_f=5)
    def sweeping(self):
        self.delete('all')
        for i,j in enumerate(self.list):
            j.set_tag(str(i))
            self.create_window(self.w/2.0,(i+1)*self.unit,anchor=S,\
                           window=j.get_label(),tags=j.get_tag())
class Ala_box:
    def __init__(self,date,default=None,*modify):
        #modify (Ala,) default[music,repeat](str)
        self.t = Toplevel()
        self.t.resizable(0,0)
        self.date=date
        self.value=0
        another = self.t
        self.t_l=[Label(another,text="hour"),Label(another,text="minute")
             ,Label(another,text="music"),Label(another,text="year")
             ,Label(another,text="month"),Label(another,text="day")
             ,Label(another,text="style"),Label(another,text="repeat")
             ,Entry(another),Entry(another),Entry(another),Entry(another)
             ,Entry(another),Entry(another),Entry(another),Entry(another)]
        if modify:
            self.t_l[8].insert(0,str(modify[0].time[0]))
            self.t_l[9].insert(0,str(modify[0].time[1]))
            self.t_l[10].insert(0,modify[0].music)
            self.t_l[11].insert(0,str(modify[0].date[0]))
            self.t_l[12].insert(0,str(modify[0].date[1]))
            self.t_l[13].insert(0,str(modify[0].date[2]))
            self.t_l[14].insert(0,modify[0].style)
            self.t_l[15].insert(0,str(modify[0].repeat))
        else:
            if default:
                self.t_l[10].insert(0,default[0])
                self.t_l[15].insert(0,default[1])
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
        self.value=0
        self.t = Toplevel()
        self.t.resizable(0,0)
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
    def __init__(self,root,length,cal=None): #canvas -- rectangle 1:2 #date [#,#,#,#]
        Canvas.__init__(self,root,height=length*2,width=length)
        self.calendar=cal
        self.alarm_default=["I'm Yours",'5']
        self.alive=1
        self.date=std_date() 
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
                                   int(self.unit*8),unit=self.unit,clo=self)
        self.create_window(self.unit*5,self.unit*15.5,window=self.alarm_map,\
                           tags="Ala_map")
        self.scrollY = Scrollbar(orient=VERTICAL,command=self.alarm_map.yview)
        self.create_window(self.unit*9,self.unit*15.5,window=self.scrollY,\
                           tags="origin",height=int(self.unit*7))
        self.alarm_map["yscrollcommand"]=self.scrollY.set
        self.update_run()
    def set_alarm_default(self):
        top=Toplevel()
        _l1=Label(top,text=" music:")
        _2l=Label(top,text="repeat:")
        self.e1=Entry(top)
        self.e2=Entry(top)
        b1=Button(top,text="OK",command=self.d_ok)
        b2=Button(top,text="Cancel",command=self.d_cancel)
        _1l.grid(column=0,row=0)
        _2l.grid(column=0,row=1)
        self.e1.grid(column=1,row=0)
        self.e2.grid(column=1,row=1)
        b1.grid(column=0,row=2)
        b2.grid(column=1,row=2)
        self.another_top=top
        self.another_top.mainloop()
    def d_ok(self):
        self.another_top.quit()
        self.another_top.destroy()
        self.default=[]
        self.default.append(self.e1.get())
        self.default.append(self.e1.get())
    def d_cancel(self):
        self.another_top.quit()
        self.another_top.destroy()
    def set_date(self,date):
        self.date=date
    def add_alarm(self,hour,minute,music,date,style,repeat):
        self.alarm_map.add_one(Ala(self,hour,minute,music,date,\
                                   style,repeat,wide=20))
    def alarm(self):
        x = Ala_box(self.date,self.alarm_default)
        if x.value:
            date_list=[formal2(x.out[i]) for i in [3,4,5]]
            self.add_alarm(formal2(x.out[0]),formal2(x.out[1]),x.out[2],\
                           date_list,x.out[6],eval(x.out[7]))
        else:
            pass
    def set_time(self,hour,minute,second):
        self.hour=formal2(hour)
        self.minute=formal2(minute)
        self.second=formal2(second)
        self.update_run()
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
    def update_run(self):
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
            self.update_run()
        else: pass
    def run_clock(self):
        while self.alive:
            if self.hour==0 and self.minute==0 and self.second==0:
                self.calendar.calculate_one()
                self.date=forward_oneday(self.date)
            sleep(0.99875) #80min 6s later so(1-1/800)
            self.go_one()
    def dying(self):
        self.alive=0
    def run_alarm(self):
        while self.alive:
            for i in self.alarm_map.list:
                if self.hour==0 and self.minute==0 and self.second==0:
                    i.living()
                if self.is_time(i) and i.live:
                    i.ring()
    def is_time(self,i): # i is the Ala class
        if i.style=='c':
            if i.time[0]==self.hour and i.time[1]==self.minute and \
               self.date[:3]==i.date:
                return 1
            else:
                return 0
        elif i.style=='e':
            if i.time[0]==self.hour and i.time[1]==self.minute:
                return 1
            else:
                return 0
#----------------------------------------------------------------------
def test():
    root=Tk()
    root.resizable(0,0)
    c = Clo(root,200)
    c.grid()
    t=threading.Thread(target=c.run_clock,args=())
    t.setDaemon(True)
    t.start()
    t2=threading.Thread(target=c.run_alarm)
    t2.setDaemon(True)
    t2.start()
    root.mainloop()
    c.dying()
if __name__ == "__main__":
    test()
    
        
