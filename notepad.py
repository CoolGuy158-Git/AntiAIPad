# Yea I use AI sometimes and I feel guilty, so here's a text editor where you literally cannot copy paste
# Forked from https://github.com/notwld/notepad-gui btw

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
from base64 import b64encode,b64decode
from tkinter import font
import json

win=Tk()
win.title('AntiAiPad')
win.geometry("720x690")
def block_paste(event):
    return "break"
settings = {
    "font": "Arial",
    "bg": "white",
    "fg": "black"
}
if os.path.exists("settings.json"):
    with open("settings.json","r") as f:
        loaded = json.load(f)
        settings.update(loaded)
textarea = Text(win,font=(settings["font"], 15),bg=settings["bg"],fg=settings["fg"])
textarea.pack(expand=True, fill=BOTH)
textarea.bind("<<Paste>>",block_paste)
file=None
all_fonts = list(font.families())
menu=Menu(win)

def new_file():
    global file
    win.title('Saved File')
    file=None
    textarea.delete(1.0 ,'end')

def file_open():
    global file
    file = askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
    if file == "":
        file=None
    else:
        f=open(file,'r')
        win.title(os.path.basename(file) + " - Notepad")
        textarea.delete(1.0, 'end')
        textarea.insert(1.0, f.read())
        f.close()

def save():
    global file
    if file==None:
        file=asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
        if file =="":
            file = None

        else:
            f=open(file,'r')
            f.write(textarea.get(1.0, 'end'))
            f.close()

            win.title(os.path.basename(file) + " - Notepad")
            print("File Saved")
    else:
        f=open(file, "w")
        f.write(textarea.get(1.0,'end'))
        f.close()


def save_settings():
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def change_font():
    top = Toplevel(win)
    top.title('Change Font')
    listbox = Listbox(top)
    listbox.pack(expand=True, fill=BOTH)
    for f in font.families():
        listbox.insert(END, f)

    def apply_font():
        try:
            selectedf = listbox.get(listbox.curselection())
            textarea.config(font=(selectedf, 15))
            settings["font"] = selectedf
            save_settings()
            top.destroy()
        except:
            pass

    btn = Button(top, text="Apply Font", command=apply_font)
    btn.pack()

def change_bg():
    top = Toplevel(win)
    top.title('Change Background')
    colors = ["white", "black", "red", "green", "yellow", "blue"]
    listbox = Listbox(top)
    listbox.pack(expand=True, fill=BOTH)
    for c in colors:
        listbox.insert(END, c)

    def apply_bg():
        try:
            selectedb = listbox.get(listbox.curselection())
            textarea.config(bg=selectedb)
            settings["bg"] = selectedb
            save_settings()
            top.destroy()
        except:
            pass

    button = Button(top, text="Apply Background", command=apply_bg)
    button.pack()

def change_font_color():
    top = Toplevel(win)
    top.title('Change Font Color')
    colors = ["white", "black", "red", "green", "yellow", "blue"]
    listbox = Listbox(top)
    listbox.pack(expand=True, fill=BOTH)
    for c in colors:
        listbox.insert(END, c)

    def apply_font_color():
        try:
            selectedfc = listbox.get(listbox.curselection())
            textarea.config(fg=selectedfc)
            settings["fg"] = selectedfc
            save_settings()
            top.destroy()
        except:
            pass

    button1 = Button(top, text="Apply Font Color", command=apply_font_color)
    button1.pack()


Personalize=Menu(menu,tearoff=0)
Personalize.add_command(label='Font', command=change_font)
Personalize.add_command(label='Change BG', command=change_bg)
Personalize.add_command(label='Change FG', command=change_font_color)
menu.add_cascade(label='Personalize',menu=Personalize)
win.config(menu=menu)
file_menu=Menu(menu,tearoff=0)
file_menu.add_command(label='New File',command=new_file)
file_menu.add_command(label='Open File',command=file_open)
file_menu.add_command(label='Save File',command=save)
file_menu.add_separator()
file_menu.add_command(label='Exit',command=win.destroy)
menu.add_cascade(label='File',menu=file_menu)


def encr():
    a=textarea.get(1.0,'end')
    s=''
    for i in a:
        s=s+str(i)
    en=b64encode(s.encode())
    textarea.delete(1.0,'end')
    textarea.insert(1.0,en)

def dencr():
    a=textarea.get(1.0,'end')
    s=''
    for i in a:
        s=s+str(i)
    en=b64decode(s.encode())
    textarea.delete(1.0,'end')
    textarea.insert(1.0,en)


edit_menu=Menu(menu,tearoff=0)
edit_menu.add_command(label='Cut',accelerator="Ctrl+x",command=lambda:textarea.focus_get().event_generate('<<Cut>>'))
edit_menu.add_command(label='Copy',accelerator="Ctrl+c",command=lambda:textarea.focus_get().event_generate('<<Copy>>'))
edit_menu.add_command(label='Paste',accelerator="Ctrl+v",command=lambda:textarea.focus_get().event_generate('<<Paste>>'))
edit_menu.add_command(label='Select all',accelerator="Ctrl+a",command=lambda:textarea.focus_get().event_generate('<<Select>>'))
edit_menu.add_command(label='Encrypt text',command=encr)
edit_menu.add_command(label='Decrypt text',command=dencr)
menu.add_cascade(label='Edit',menu=edit_menu)

def about():
    messagebox.showinfo('About','Made by CoolGuy158 originally forked from this guy named notwld ')

About=Menu(menu,tearoff=0)
About.add_command(label='Credits',command=about)
menu.add_cascade(label='About',menu=About)

win.config(menu=menu)

def on_closing():
        if messagebox.askokcancel("Quit", "Unsaved Changes"):
            win.destroy()

win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()

