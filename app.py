"""
This application is for getting wifi password  which is present on your system
"""

from tkinter import *
from tkinter.ttk import Combobox, Treeview
import tkinter.messagebox
import subprocess
import threading


#  creating instance
class WifiPassword:
    
    def __init__(self, root):
        self.root=root
        self.root.title("Wifi & password")
        self.root.geometry("500x405")
        self.root.iconbitmap("favicon.ico")
        self.root.resizable(0,0)

        
        # clearing data
        def clear():
             contact_trees.delete(*contact_trees.get_children())
             
 
       
        #  this will show password
        def searching_password():

            try:

                clear()
                
                data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
                profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
                
                for i in profiles:
                    result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
                    results = [b.split(":")[1][1:-1] for b in result if "Key Content" in b]
                    
                    try:
                         contact_trees.insert('', END, values=(str(i), results[0]))
                    except Exception as e:
                         print(e)
                         
            except Exception as e:
                    tkinter.messagebox.showerror('Error',"Something goes wrong")
             


        #   threading for function
        def thread_search():
            t = threading.Thread(target=searching_password)
            t.start()


                
        #   This is for hovering button
        def on_enter1(e):
            but_search['background']="black"
            but_search['foreground']="cyan"
  
        def on_leave1(e):
            but_search['background']="SystemButtonFace"
            but_search['foreground']="SystemButtonText"

        def on_enter2(e):
            but_clear['background']="black"
            but_clear['foreground']="cyan"
  
        def on_leave2(e):
            but_clear['background']="SystemButtonFace"
            but_clear['foreground']="SystemButtonText"
            
            
        
         #  frame
        mainframe = Frame(self.root, width=500, height=405, bd=3, relief="ridge")
        mainframe.place(x=0,y=0)

        firstframe = Frame(mainframe, width=494, height=100, bd=3, relief="ridge")
        firstframe.place(x=0,y=0)

        secondframe = Frame(mainframe, width=494, height=297, bd=3, relief="ridge")
        secondframe.place(x=0,y=100)

        lab_frame = LabelFrame(firstframe, width=488, height=95, text="Wifi and password", bg="#89b0ae", fg="white")
        lab_frame.place(x=0,y=0)

     
         # button
        but_search = Button(lab_frame, width=13, text="Wifi", font=('times new roman', 12), cursor="hand2", command=thread_search)
        but_search.place(x=50,y=30)
        but_search.bind("<Enter>",on_enter1)
        but_search.bind("<Leave>",on_leave1)

        but_clear=Button(lab_frame,width=13,text="Clear",font=('times new roman',12),cursor="hand2",command=clear)
        but_clear.place(x=300,y=30)
        but_clear.bind("<Enter>",on_enter2)
        but_clear.bind("<Leave>",on_leave2)

      
        # scrollbar for 
        scrol = Scrollbar(secondframe,orient="vertical")
        scrol.place(relx=1, rely=0, relheight=1, anchor='ne')

        contact_trees = Treeview(secondframe, columns=("Username", "Password"), height=13, yscrollcommand=scrol.set)
        contact_trees.heading("Username", text="UserName")
        contact_trees.heading("Password", text="Password")
        contact_trees['show']="headings"
        contact_trees.column("Username", width=233, minwidth=10)
        contact_trees.column("Password", width=233, minwidth=40)
        contact_trees.place(x=0,y=0)

        scrol.config( command = contact_trees.yview )  

        

if __name__ == "__main__":
    root=Tk()
    app=WifiPassword(root)
    root.mainloop()
