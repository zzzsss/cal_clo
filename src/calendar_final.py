from Tkinter import *
from std_time import *#self_defined
import tkFont
#----------------------------------------------------------
#the calculations
def outx(x):
    if (x%7):
        return x%7+1
    else: return 8
def outy(x):
    return 3+(x-1)/7
#--------------------------------------------------------------------------
#class the tag
class sth_Tag(Label):
    def __init__(self,t,string):
        self.rstring=string
        self.string = "%-3s"%str(len(t.list)+1)+string
        self.t=t
        self.finish=0
        Label.__init__(self,None,text=self.string,bg='lightblue')
        self.bind('<Button-1>',self.choice_out)
        self.bind('<Button-2>',self.choice_out)
        self.bind('<Button-3>',self.choice_out)
        self.bind('<Double-Button-1>',self.choice_out)
    def choice_out(self,but):
        self.top=Toplevel()
        b1=Button(self.top,text="delete",command=self.get_remove)
        b2=Button(self.top,text="modify",command=self.get_modify)
        b3=Button(self.top,text="finish",command=self.get_finish)
        b1.grid()
        b2.grid()
        b3.grid()
        self.top.mainloop()
    def get_remove(self):
        self.top.quit()
        self.top.destroy()
        self.t.list.remove(self)
        self.t.show()
    def get_modify(self):
        self.top.quit()
        self.top.destroy()
        x=cal_box(1,self.t.f,self.rstring)
        if x.value:
            self.t.list.remove(self)
            old=self.t.f.show_date
            k=x.out[:3]
            k.append(what_day(x.out[0],x.out[1],x.out[2]))
            self.t.f.set_show_date(k)
            self.t.f.get_tag(k).got_sth(x.out[3])
            self.t.show()
            self.t.f.set_show_date(k)
            self.t.f.set_show_date(old)
    def get_finish(self):
        self.top.quit()
        self.top.destroy()
        self.finish=1
        self["bg"]='lightgreen'
        self.t.show()
class Tag(Label):
    def __init__(self,f,string,length,x,y,ta,date=None):
        self.f=f
        self.x=x
        self.y=y
        self.ta=ta
        self.date=date
        self.list=[]
        self.state=0 #0:no 1:yes unfinsh 2:yes finish
        Label.__init__(self,None,text=string,width=2,bg='white')
        if self.date==None:
            pass
        else:
            self.bind("<Button-1>",self.select)
        self.selected=0
        self.todayed=0
        self.draw()
    def tell_state(self):
        if self.state==0:
            self['fg']='black'
        elif self.state==1:
            self['fg']='red'
        elif self.state==2:
            self['fg']='blue'
    def draw(self):
        self.tell_state()
        self.id=self.f.can1.create_window(self.x,self.y,window=self,\
                                          tags=self.ta)
    def select(self,x):
        self.f.set_show_date(self.date)
    def got_sth(self,string):
        self.list.append(sth_Tag(self,string))
    def show(self):
        self.f.sth_can.delete("sth")
        for i,j in enumerate(self.list):
            self.f.sth_can.create_window(self.f.sth_can.w/2.0,(i+1)*self.f.\
                                         unit,anchor=S,window=j,tags="sth",\
                                         width=self.f.unit*7)
        if len(self.list)==0:
            self.state=0
        elif all([i.finish for i in self.list]):
            self.state=2
        else:
            self.state=1
        self.tell_state()
        self.f.sth_can["scrollregion"]=(0,0,self.f.unit*7,\
                                        self.f.unit*len(self.list))
class cal_box: #0.jump 1.add sth_to_do
    def __init__(self,number,cal,string=''):
        self.cal=cal
        self.number=number
        self.t=Toplevel()
        self.l1=Label(self.t,text=" Year:")
        self.l2=Label(self.t,text="Month:")
        self.l3=Label(self.t,text=" Date:")
        self.e1=Entry(self.t)
        self.e2=Entry(self.t)
        self.e3=Entry(self.t)
        self.e1.insert(0,str(cal.show_date[0]))
        self.e2.insert(0,str(cal.show_date[1]))
        self.e3.insert(0,str(cal.show_date[2]))
        self.l1.grid(column=0,row=0)
        self.l2.grid(column=0,row=1)
        self.l3.grid(column=0,row=2)
        self.e1.grid(column=1,row=0)
        self.e2.grid(column=1,row=1)
        self.e3.grid(column=1,row=2)
        self.l4=Label(self.t,text="tag:")
        self.e4=Entry(self.t)
        self.e4.insert(0,string)
        self.b1 = Button(self.t,text='sure',command=self.sure)
        self.b2 = Button(self.t,text='cancel',command=self.cancel)
        self.b3 = Button(self.t,text="jump to today",command=self.today)
        if self.number==0:
            self.b1.grid(column=0,row=3)
            self.b2.grid(column=1,row=3)
            self.b3.grid(column=0,row=4,columnspan=2)
        elif self.number==1:
            self.l4.grid(column=0,row=3)
            self.e4.grid(column=1,row=3)
            self.b1.grid(column=0,row=4)
            self.b2.grid(column=1,row=4)
        self.t.mainloop()
    def cancel(self):
        self.value=0
        self.t.quit()
        self.t.destroy()
    def today(self):
        self.value=1
        self.out=self.cal.date
        self.t.quit()
        self.t.destroy()
    def sure(self):
        self.value=1
        if self.number==0:
            self.out=[formal2(self.e1.get()),formal2(self.e2.get())\
                      ,formal2(self.e3.get())]
        elif self.number==1:
            self.out=[formal2(self.e1.get()),formal2(self.e2.get())\
                      ,formal2(self.e3.get()),self.e4.get()]
        self.t.quit()
        self.t.destroy()
class sth_c(Canvas):
    def __init__(self,cal,height,width):
        self.cal=cal
        self.h,self.w=height,width
        Canvas.__init__(self,height=self.h,width=self.w)
#--------------------------------------------------------------------------
class Cal(Frame):
    def __init__(self,root,l,clo=None): # two canvas
        self.calculate=0
        self.root=root
        Frame.__init__(self,root)
        self.clock=clo
        self.can1=Canvas(self,height=l*2,width=l*2)
        self.can2=Canvas(self,height=l*2,width=l)
        self.can1.grid(column=0,row=0)
        self.can2.grid(column=1,row=0)
        self.l = eval(self.can1["width"])/10.0
        self.l2= eval(self.can2["width"])/10.0
        self.unit=self.l2
        self.dictionary={}
        #can1
        self.buttona=Button(command=self.changem,text='<')
        self.buttonb=Button(command=self.changep,text='>')
        self.can1.create_window(self.l*2,self.l,window=self.buttona,\
                               height=self.l2,width=self.l2,tags='origin')
        self.can1.create_window(self.l*8,self.l,window=self.buttonb,\
                               height=self.l2,width=self.l2,tags='origin')
        #can2
        self.buttonc=Button(command=self.set_to_today,text='set_today')
        self.buttond=Button(command=self.jump,text="jump_to")
        self.buttone=Button(command=self.add_sth,text="add_sth_to_do")
        self.buttonf=Button(command=self.calculating,text="update_date")
        self.buttong=Button(command=self.standard,text="str_time&date",bg='red')
        self.can2.create_window(self.l2*3,self.l2*10,window=self.buttonc,\
                               height=self.l2,width=3*self.l2,tags='origin')
        self.can2.create_window(self.l2*7,self.l2*10,window=self.buttond,\
                               height=self.l2,width=3*self.l2,tags='origin')
        self.can2.create_window(self.l2*5,self.l2*11.5,window=self.buttone,\
                               height=self.l2,width=5*self.l2,tags='origin')
        self.can2.create_window(self.l2*5,self.l2*8.5,window=self.buttonf,\
                               height=self.l2,width=5*self.l2,tags='origin')
        self.can2.create_window(self.l2*5,self.l2*7,window=self.buttong,\
                               height=self.l2,width=5*self.l2,tags='origin')
        #show attribute:
        self._1=1
        self.set_show_date(std_date())
        self.set_date(std_date())
        
        #can2_continue
        self.f=tkFont.Font(size=20)
        self.label_y=Label(text=str(self.show_date[0]),font=self.f)
        self.label_m=Label(text=Month_names[self.show_date[1]-1],font=self.f)
        self.label_d=Label(text=str(self.show_date[2]),font=self.f)
        self.label_wd=Label(text=W_names[self.show_date[3]],font=self.f)
        self.can2.create_window(self.l2*5,self.l2*1.5,window=self.label_y,\
                               height=2*self.l2,width=5*self.l2,tags='origin')
        self.can2.create_window(self.l2*4,self.l2*3.5,window=self.label_m,\
                               height=2*self.l2,width=7*self.l2,tags='origin')
        self.can2.create_window(self.l2*8,self.l2*3.5,window=self.label_d,\
                               height=2*self.l2,width=2*self.l2,tags='origin')
        self.can2.create_window(self.l2*5,self.l2*5.5,window=self.label_wd,\
                               height=2*self.l2,width=8*self.l2,tags='origin')

        self._1=0
        #can2 -- manage the sth_to_do box(12.5~19.5)
        self.sth_can=sth_c(self,int(7*self.l2),int(8*self.l2))
        self.can2.create_window(self.l2*5,self.l2*16,window=self.sth_can,\
                               tags='origin')
        self.scrollY = Scrollbar(orient=VERTICAL,command=self.sth_can.yview)
        self.can2.create_window(self.unit*9,self.unit*16,window=self.scrollY,\
                           tags="origin",height=int(self.unit*7))
        self.sth_can["yscrollcommand"]=self.scrollY.set
    def get_clock(self,new):
        self.clock=new
    def standard(self):
        self.set_show_date(std_date())
        self.set_date(std_date())
    def calculate_one(self):
        self.calculate += 1
    def calculating(self):
        for i in range(self.calculate):
            self.move_oneday()
        self.calculate=0
    def move_oneday(self):
        new_d=forward_oneday(self.date)
        self.set_date(new_d)
        self.set_show_date(new_d)
    def set_to_today(self):
        self.set_date(self.show_date)
    def jump(self):
        x=cal_box(0,self)
        if x.value:
            k=x.out
            k.append(what_day(x.out[0],x.out[1],x.out[2]))
            self.set_show_date(k)
    def add_sth(self):
        x=cal_box(1,self)
        if x.value:
            old=self.show_date
            k=x.out[:3]
            k.append(what_day(x.out[0],x.out[1],x.out[2]))
            self.set_show_date(k)
            self.get_tag(k).got_sth(x.out[3])
            self.set_show_date(k)
            self.set_show_date(old)
    def get_tag(self,date):
        x = str(date[0])+'_'+str(date[1])
        if self.dictionary.has_key(x):
            return self.dictionary[x][date[2]-1]
        else:
            return None
    def change(self,date,y_f=0,m_f=0):
        if date:
            self.set_show_date(date)
        else:
            a = y_f + self.show_date[0]+(self.show_date[1]+m_f-1)/12
            b = (self.show_date[1]+m_f)%12
            if b==0:
                b=12
            if self.show_date[2]>Month_days[b]:
                c=Month_days[b]
            else:
                c=self.show_date[2]
            d=what_day(a,b,c)
            self.set_show_date([a,b,c,d])                      
    def set_date(self,date):
        if self._1==0:
            self.get_tag(self.date)["relief"]=FLAT
        self.date=date
        self.get_tag(self.date)["relief"]=RIDGE
        if self.clock:
            self.clock.set_date(self.date)
    def set_show_date(self,date):
        #can1
        if self._1==0:
            self.get_tag(self.show_date)["bg"]="white"
        self.show_date=date
        self.days_num=monthdays(self.show_date[1],self.show_date[0])
        self.m = which_day(self.show_date[1],self.show_date[0])
        self.show_list=[]
        self.label=str(self.show_date[0])+'  '+['Jan','Feb','Mar','Apr','May',\
                                                'Jun','Jul','Aug','Sep','Oct',\
                                                'Nov','Dec']\
                                                [self.show_date[1]-1]
        self.now_label=str(self.show_date[0])+'_'+str(self.show_date[1])
        self.update()
        self.get_tag(self.show_date)["bg"]='lightblue'
        #can2
        if self._1==0:
            self.label_y["text"]=str(self.show_date[0])
            self.label_m["text"]=Month_names[self.show_date[1]-1]
            self.label_d["text"]=str(self.show_date[2])
            self.label_wd["text"]=W_names[self.show_date[3]]
        #sth_tag
        if self._1==0:
            self.get_tag(self.show_date).show()
    def changep(self):
        self.change(None,m_f=1)
        self.update()
    def changem(self):
        self.change(None,m_f=-1)
        self.update()
    def update(self):
        self.can1.delete('tag')
        self.draw1()
    def draw1(self):
        self.can1.create_text(self.l*5,self.l,text=self.label,tags='tag')
        for i in range(1,8):
            Tag(self,['Mo','Tu','We','Th','Fr','Sa','Su'][i-1],\
                self.l,outx(i)*self.l,2*self.l,ta='tag')
        for i in range(1,self.m):
                Tag(self,"",self.l,outx(i)*self.l,outy(i)*self.l,ta='tag')
        if self.dictionary.has_key(self.now_label):
            for i in self.dictionary[self.now_label]:
                i.draw()
        else:
            for i in range(self.m,self.m+self.days_num):
                self.show_list.append(Tag(self,str(i-self.m+1),self.l,\
                                     outx(i)*self.l,outy(i)*self.l,ta='tag'\
                                          ,date=[self.show_date[0],\
                                                 self.show_date[1],i-self.m+1,\
                                                 what_day(self.show_date[0],\
                                                          self.show_date[1],\
                                                          i-self.m+1)]))
            self.dictionary[self.now_label]=self.show_list
#---------------------------------------------------------------
def test():
    x=Tk()
    c=Cal(x,200)
    c.grid()
    x.mainloop()
if __name__=="__main__":
    test()
    
