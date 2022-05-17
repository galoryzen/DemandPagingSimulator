from tkinter import *
from tkinter import ttk
import math as mt

from pyparsing import col

root = Tk()
root.title('Simulador paginacion bajo demanda')
root.geometry("1000x700")
root.resizable(False,False)

speed = 500
anim_speed = 5
anim_speed2 = 5
true_speed = 15

def print_tablapag(tabla_pagina):
    i = 0
    s = 'Tabla de pagina\n\n'
    s+='i | m | bv | bs |\n'
    for row in tabla_pagina:
        s+= f'{i} | {row[0] if row[0] != None else "-"} | {row[1]}  | {row[2]}  |\n'
        i+=1
    return s

def move(button, buttondest, content):
    root.update()
    content.update()
    x = button.winfo_x()
    y = button.winfo_y()

    xd = buttondest.winfo_x()
    yd = buttondest.winfo_y()
    # print(x, y, xd, yd)

    sp_x = true_speed if x < xd else -true_speed
    sp_y = true_speed if y < yd else -true_speed

    if x != xd or y != yd:

        x += sp_x
        y += sp_y

        if sp_x < 0:
            if x < xd:
                x = xd
        else:
            if x > xd:
                x = xd
        
        if sp_y < 0:
            if y < yd:
                y = yd
        else:
            if y > yd:
                y = yd

        button.place(x=x, y=y, relx=0, rely=0, bordermode='outside')

def start_iterations(tam_marco, so, proc, marcos, marcos_so):
    clear()
    global anim_speed

    content = ttk.Frame(root, padding=40)

    

    with open(f"{__file__.rstrip('main.py')}input.txt", "r") as f:
        instrucciones = [line.strip().split(' ') for line in f]
    
    paginas_proc = list(range(mt.ceil(proc/tam_marco)))
    instrucciones = [(int(tuple[0]), tuple[1]) for tuple in instrucciones]
    tabla_pagina = [[None, 0, 0] for pagina in paginas_proc]
    pilacola = []

    memoria = marcos_so + marcos
    pady=70/len(paginas_proc)
    # pady2=70/len(memoria)

    labelinstruccion = ttk.Label(content, text=" ", font=('Helvetica', 12))
    firstlbl = ttk.Label(content, text="Paginas del proceso")
    tabla = ttk.Label(content, text=print_tablapag(tabla_pagina))
    framemedio = ttk.Frame(content, width=600, height=30, relief="ridge")
    secondlbl = ttk.Label(content, text="Marcos en Memoria Principal")
    bitacora = ttk.Label(content, text="", font=('Helvetica', 10))

    bs = [Button(content, text=f'Pagina {pagina}', width=10, pady=pady, bg='white') for pagina in paginas_proc]

    ms = [Button(content, text=f'Marco {marco}', width=10, pady=pady, bg='yellow') if marco in marcos_so else Button(content, text=f'Marco {marco}', width=10, pady=pady, bg='white') for marco in memoria]


    labelinstruccion.grid(row=0, column=1)
    content.grid(column=0, row=0)
    firstlbl.grid(column=0, row=0)
    secondlbl.grid(column=2, row=0)
    for pagina in paginas_proc:
        bs[pagina].grid(column=0, row=pagina+1)
    
    tabla.grid(column=1, row=3, rowspan=10)
    framemedio.grid(column=1 , row=2)
    bitacora.grid(column=1, row=1)

    for i in range(len(memoria)):
        ms[i].grid(column=2, row=i+1)

    # if len(bs)>len(ms):
    #     Button(content, text=f'... Memoria', width=10, pady=(len(bs)-len(ms))*20, bg='gray').grid(column=2, row=len(ms), rowspan=(len(bs)-len(ms)))

    for instruccion in instrucciones:
        pag = instruccion[0]//tam_marco
        tipo = "Lectura" if instruccion[1]=='L' else "Escritura"
        labelinstruccion.config(text=f'Instruccion:      Dirección {instruccion[0]} {tipo}   >>>   Pagina {pag}')
        bitacora.config(text=f'La pagina solicitada es la {pag}')
        content.after(speed)
        root.update()
        content.update()

        bitacora.config(text='Ingresando a la tabla de pagina')
        content.after(speed)
        root.update()
        content.update()

        
        try:
            info = tabla_pagina[pag]
        except Exception as e:
            bitacora.config(text='El programa trató acceder a una dirección que no correspondía dentro de las de el')
            content.after(speed)
            root.update()
            content.update()
            continue
        
        #INSERTAR EN MARCO VACIO
        if info[1] == 0:
            bitacora.config(text='Fallo de pagina, no se encontraba cargada')
            content.after(speed)
            root.update()
            content.update()
            if len(marcos)!=0:
                m = marcos.pop(0)

                bitacora.config(text=f'Ingresando la pagina {pag} al marco {m}')
                content.after(speed)
                root.update()
                content.update()

                buttons = [widget for widget in content.winfo_children() if widget.widgetName == 'button']
                bo = buttons[pag]
                
                bd = None
                for button in buttons:
                    if button['text'] == f'Marco {m}':
                        bd = button
                
                root.update()
                content.update()
                xo, yo = bo.winfo_x(), bo.winfo_y()
                ro = bo.grid_info()['row']

                bo_copy = Button(content, text=bo['text'], width=10, pady=pady, bg='blue')
                bo_copy.grid(row=ro, column=0)
                bd.configure(background='red')

                while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                    root.update()
                    content.update()

                    content.after(anim_speed2, move, bo_copy, bd, content)
                    content.after(anim_speed)
                
                root.update()
                content.update()

                bo_copy.destroy()

                bitacora.config(text=f'Cambiando el bit de valido/invalido a 1')
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][1] = 1
                tabla.config(text=print_tablapag(tabla_pagina))

                tabla_pagina[pag][0] = m
                tabla.config(text=print_tablapag(tabla_pagina))

            else:
                LRU = pilacola.pop(0)
                m = tabla_pagina[LRU][0]

                bitacora.config(text=f'La pagina menos usada recientemente es la pagina {LRU}, liberando asi el marco {m}')
                content.after(speed)
                root.update()
                content.update()

                # SWAP OUT
                if tabla_pagina[LRU][2] == 1:
                    bitacora.config(text='El bit sucio es 1, por tanto hay swap out')
                    content.after(speed)
                    root.update()
                    content.update()

                    buttons = [widget for widget in content.winfo_children() if widget.widgetName == 'button']
                    bd = buttons[LRU]
                    
                    bo = None
                    for button in buttons:
                        if button['text'] == f'Marco {tabla_pagina[LRU][0]}':
                            bo = button
                    
                    root.update()
                    content.update()

                    ro = bo.grid_info()['row']


                    bd.configure(background='red')

                    bo_copy = Button(content, text=bo['text'], width=10, pady=pady, bg='blue')
                    bo_copy.grid(row=ro, column=2)

                    while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                        root.update()
                        content.update()

                        content.after(anim_speed2, move, bo_copy, bd, content)
                        content.after(anim_speed)
                    
                    root.update()
                    content.update()
                    bo_copy.destroy()

                    bd.configure(background='white')
  
                else:
                    bitacora.config(text='El bit sucio es 0, por tanto NO hay swap out')
                    content.after(speed)
                    root.update()
                    content.update()
                
                #SWAP IN
                bitacora.config(text=f'Swap in de la pagina {pag} al marco {m}')
                content.after(speed)
                root.update()
                content.update()

                buttons = [widget for widget in content.winfo_children() if widget.widgetName == 'button']
                bo = buttons[pag]
                
                bd = None
                for button in buttons:
                    if button['text'] == f'Marco {m}':
                        bd = button

                ro = bo.grid_info()['row']

                bo_copy = Button(content, text=bo['text'], width=10, pady=pady, bg='blue')
                bo_copy.grid(row=ro, column=0)

                bd.configure(background='red')

                while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                    root.update()
                    content.update()

                    content.after(anim_speed2, move, bo_copy, bd, content)
                    content.after(anim_speed)
                
                root.update()
                content.update()
                bo_copy.destroy()

                bitacora.config(text=f'Borrando la fila de la pagina {LRU} en la tabla de pagina')
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[LRU] = [None, 0, 0]
                tabla.config(text=print_tablapag(tabla_pagina))

                tabla_pagina[pag][1] = 1
                tabla_pagina[pag][0] = m
                tabla.config(text=print_tablapag(tabla_pagina))

                
                
            if instruccion[1] == 'E':
                bitacora.config(text=f'Escritura en la pagina {pag}')
                content.after(speed)
                root.update()
                content.update()

                bitacora.config(text=f'Cambiando el bit sucio de la pagina {pag} a 1')
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][2] = 1
                tabla.config(text=print_tablapag(tabla_pagina))
            else:
                bitacora.config(text=f'Lectura en la pagina {pag}')
                content.after(speed)
                root.update()
                content.update()
        else:
            bitacora.config(text=f'La pagina se encontraba ya cargada, especificamente en el marco {tabla_pagina[pag][0]}')
            content.after(speed)
            root.update()
            content.update()

            if instruccion[1] == 'E':
                bitacora.config(text=f'Escritura en la pagina {pag}')
                content.after(speed)
                root.update()
                content.update()

                bitacora.config(text=f'Cambiando el bit sucio de la pagina {pag} a 1')
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][2] = 1
                tabla.config(text=print_tablapag(tabla_pagina))
            else:
                bitacora.config(text=f'Lectura en la pagina {pag}')
                content.after(speed)
                root.update()
                content.update()
                
        if pag in pilacola:
            pilacola.remove(pag)
            pilacola.append(pag)
            print(f'Borrando de la pilacola la pagina {pag} e ingresandola al final')
        else:
            pilacola.append(pag)
            print(f'Ingresandola a la pilacola la pagina {pag}')

    bitacora.config(text=f'Fin de la ejecucion')
    content.after(speed)
    root.update()
    content.update()
        # input('Presione cualquier tecla para seguir a la proxima iteracion')


def tomar_datos():
    clear()
    a1,a2,a3,a4 = '5','15','70','8'

    frame = ttk.Frame(content, width=800, height=100).pack()

    tam_marco = Entry(root, width = 60)
    so = Entry(root, width = 60)
    proc = Entry(root, width = 60)
    marcos = Entry(root, width = 60)

    Label(root, text="Tamaño del marco").pack()

    tam_marco.pack(pady=10)
    # tam_marco.insert(0, 'EJ: 16')
    tam_marco.insert(0, a1)

    tam_marco.configure(state='disabled')

    Label(root, text="Tamaño del SO").pack()

    so.pack(pady=10)
    # so.insert(0, 'EJ: 60')
    so.insert(0, a2)
    so.configure(state='disabled')

    Label(root, text="Tamaño del proceso").pack()

    proc.pack(pady=10)
    # proc.insert(0, 'EJ: 40')
    proc.insert(0, a3)
    proc.configure(state='disabled')

    Label(root, text="Marcos disponibles separados por espacio").pack()

    marcos.pack(pady=10)
    # marcos.insert(0, 'EJ: 7 9 10, que no entren en conflicto con los marcos del SO')
    marcos.insert(0, a4)
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
    
    start_iterations(tam_marco, so, proc, marcos, marcos_so)


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