# Python program to illustrate a stop watch 
# using Tkinter 
#importing the required libraries 
import tkinter as Tkinter 
import tkinter.font as font
from datetime import datetime
import time
import numpy as np
import pandas as pd

year=2005
df = pd.read_csv('grade7_solutions.csv')
answers = df[df['Year']==year].to_numpy()[0][1:].astype(str)

counter = 28800
counter_max = counter+60
out_of_time = False
qn = 0
answering = False
correct_answer = True

def counter_label(label, q_label): 
    def count(): 
        if running: 
            global counter
            global counter_max
            global out_of_time
            global answering
            global qn
            global correct_answer


            tt = datetime.fromtimestamp(counter)
            string = tt.strftime("%H:%M:%S")
            display=string 
    
            label['text']=display   # Or label.config(text=display) 
            q_label['text'] = 'Question {}'.format(int(qn+1))
    
            # label.after(arg1, arg2) delays by  
            # first argument given in milliseconds 
            # and then calls the function given as second argument. 
            
            if answering:
                answering = False
                if correct_answer:
                    label['text']='Correct!'
                else:
                    label['text']='Incorrect!'
                label.after(5000, count)
            
            elif counter==counter_max:
                out_of_time = True
                label['text']='Times up!'
                Next()
                out_of_time = False
                label.after(5000, count)  
                
            else:
                label.after(1000, count)  
                counter += 1
  
    # Triggering the start of the counter. 
    count()      
    
# start function of the stopwatch 
def Start(label, q_label): 
    global running 
    running=True
    counter_label(label, q_label) 
    start['state']='disabled'
    nexta['state']='normal'
    back['state']='normal'
    
# Next function of the stopwatch 
def Next(): 
    global counter 
    global out_of_time
    global qn
    global answering
    global correct_answer
    counter=28800
    
    if not out_of_time:
        answering = True
        if str(e1.get())==answers[qn]:
            correct_answer = True
        else:
            correct_answer = False
    qn+=1
    
def Back():
    global qn
    global counter
    qn-=1
    counter = 28800

def evaluate(event):
    print(str(e1.get()))

root = Tkinter.Tk() 
root.title("Stopwatch") 
# Fixing the window size. 
root.minsize(width=500, height=140) 
label = Tkinter.Label(root, text="Lets do it...", fg="black", font="Verdana 50 bold") 
label.pack()
q_label = Tkinter.Label(root, text="Question #.", fg="black", font="Verdana 35 bold") 
q_label.pack()
f = Tkinter.Frame(root)
start = Tkinter.Button(f, text='Start', width=12, command=lambda:Start(label, q_label), font="Verdana 20") 
nexta = Tkinter.Button(f, text='Next',width=12, state='disabled', command=lambda:Next(), font="Verdana 20") 
back = Tkinter.Button(f, text='Back',width=12, state='disabled', command=lambda:Back(), font="Verdana 20") 
# Entry
e1 = Tkinter.Entry(f, font="Verdana 20")
e1.pack()
f.pack(anchor = 'center',pady=5)
start.pack(side="left") 
nexta.pack(side="left") 
back.pack(side="left") 
root.mainloop()