from tkinter import *
from tkinter import ttk
import math as mt

root = Tk()
root.title('Simulador paginacion bajo demanda')
root.geometry("900x700")
root.resizable(False,False)

def move(button, buttondest):
    x = button.winfo_x()
    y = button.winfo_y()

    xd = buttondest.winfo_x()
    yd = buttondest.winfo_y()
    # print(x, y, xd, yd)

    sp_x = 5
    sp_y = 5 if y < yd else -5

    if x != xd or y != yd:

        x += sp_x
        y += sp_y

        if x > xd:
            x=xd
        
        if sp_y < 0:
            if y < yd:
                y = yd
        else:
            if y > yd:
                y = yd

        button.place(x=x, y=y, relx=0, rely=0, bordermode='outside')
        content.after(15, move, button, buttondest)

def start_iterations(tam_marco, so, proc, marcos):
    with open(f"{__file__.rstrip('main.py')}input.txt", "r") as f:
        instrucciones = [line.strip().split(' ') for line in f]
    
    paginas_proc = list(range(mt.ceil(proc/tam_marco)))
    instrucciones = [(int(tuple[0]), tuple[1]) for tuple in instrucciones]
    tabla_pagina = [[None, 0, 0] for pagina in paginas_proc]
    pilacola = []




def tomar_datos():
    clear()

    frame = ttk.Frame(content, width=800, height=100).pack()

    tam_marco = Entry(root, width = 60)
    so = Entry(root, width = 60)
    proc = Entry(root, width = 60)
    marcos = Entry(root, width = 60)

    Label(root, text="Tamaño del marco").pack()

    tam_marco.pack(pady=10)
    tam_marco.insert(0, 'EJ: 16')
    tam_marco.configure(state='disabled')

    Label(root, text="Tamaño del SO").pack()

    so.pack(pady=10)
    so.insert(0, 'EJ: 60')
    so.configure(state='disabled')

    Label(root, text="Tamaño del proceso").pack()

    proc.pack(pady=10)
    proc.insert(0, 'EJ: 40')
    proc.configure(state='disabled')

    Label(root, text="Marcos disponibles separados por espacio").pack()

    marcos.pack(pady=10)
    marcos.insert(0, 'EJ: 7 9 10, que no entren en conflicto con los marcos del SO')
    marcos.configure(state='disabled')

    frame = ttk.Frame(content, width=800, height=100).pack()
    my_button2 = Button(root, text="Ingresar", command=check_values, font=("Helvetica", 24), fg="#DDDDDD", bg="#FF4C29").pack()

    warn = Label(root, text="-", font=("Helvetica", 12), pady=30).pack()
    
    tam_marco_focus_in = tam_marco.bind('<Button-1>', lambda x: on_focus_in(tam_marco))
    tam_marco_focus_out = tam_marco.bind(
        '<FocusOut>', lambda x: on_focus_out(tam_marco, 'EJ: 16'))

    so_focus_in = so.bind('<Button-1>', lambda x: on_focus_in(so))
    so_focus_out = so.bind(
        '<FocusOut>', lambda x: on_focus_out(so, 'EJ: 60'))

    proc_focus_in = proc.bind('<Button-1>', lambda x: on_focus_in(proc))
    proc_focus_out = proc.bind(
        '<FocusOut>', lambda x: on_focus_out(proc, 'EJ: 40'))

    marcos_focus_in = marcos.bind('<Button-1>', lambda x: on_focus_in(marcos))
    marcos_focus_out = marcos.bind(
        '<FocusOut>', lambda x: on_focus_out(marcos, 'EJ: 7 9 10, que no entren en conflicto con los marcos del SO'))

def check_values():
    l = []
    for widget in root.winfo_children():
        if widget.widgetName == 'entry':
            l.append(widget)
    tam_marco, so, proc, marcos = [widget.get() for widget in l]

    wlabel = root.winfo_children()[-1]
    
    try:
        tam_marco = int(tam_marco)
    except Exception as e:
        wlabel.config(text="Debe ingresar un numero en el campo del tamaño del marco")
        return
    
    if tam_marco <= 0:
        wlabel.config(text="Debe ingresar un numero positivo en el campo del tamaño del marco")
        tam_marco = None
        return

    try:
        so = int(so)
    except Exception as e:
        wlabel.config(text="Debe ingresar un numero en el campo del tamaño del SO")
        return
        
    if so <= 0:
        wlabel.config(text="Debe ingresar un numero positivo en el campo del tamaño del SO")
        return

    try:
        proc = int(proc)
    except Exception as e:
        wlabel.config(text="Debe ingresar un numero en el campo del tamaño del proceso")
        return
    
    if proc <= 0:
        wlabel.config(text="Debe ingresar un numero positivo en el campo del tamaño del proceso")
        return

    start_iterations(tam_marco, so, proc, marcos)

    marcos_so = list(range(mt.ceil(so/tam_marco)))
    paginas_proc = list(range(mt.ceil(proc/tam_marco)))

    try:
        temp = marcos.split(' ')
        marcos = [int(s) for s in temp]
        if len(set(marcos)) != len(marcos):
            raise Exception
    except Exception as e:
        wlabel.config(text="Debe ingresar numeros enteros diferentes separados por espacio, EJ: 7 9 10")
        return
    
    a = set(marcos_so)
    b = set(marcos)
    
    if not all(n >= 0 for n in marcos):
        wlabel.config(text="El numero del marco debe ser positivo")
        return
    
    if a & b:
        wlabel.config(text=f'Los marcos libres estan en conflictos con los marcos que utilizará el SO que son: {" ".join(temp)}\n')
        return

def on_focus_in(entry):
    if entry.cget('state') == 'disabled':
        entry.configure(state='normal')
        entry.delete(0, 'end')

def on_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.configure(state='disabled')

def clear():
    for widget in root.winfo_children():
        widget.destroy()

content = ttk.Frame(root, padding=40).pack()
frame = ttk.Frame(content, width=800, height=200).pack()
text = ttk.Label(content, text=" Simulación de paginación bajo demanda controlada por contador", padding=5, font=("Helvetica", 16)).pack()
frame2 = ttk.Frame(content, width=800, height=100).pack()
my_button = Button(content, text="Iniciar", command=tomar_datos, font=("Helvetica", 24), fg="#DDDDDD", bg="#FF4C29").pack()

root.update()
root.mainloop()

# if __name__ == '__main__':
#     main()