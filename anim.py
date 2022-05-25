from tkinter import *
from tkinter import ttk
import math as mt
import csv
from tkinter import filedialog

root = Tk()
root.title('Simulador paginación bajo demanda')
root.geometry("1000x800")
root.resizable(False,False)

speed = 810
anim_speed = 5
anim_speed2 = 5
true_speed = 20
file_name = None

def select_file():
    global file_name

    filetypes = (
        ('CSV Files', '*.csv'),
    )


    filename = filedialog.askopenfilename(
        title='Seleccione el archivo csv con las instrucciones',
        initialdir='./',
        filetypes=filetypes
    )

    file_name = filename
    l = None
    for widget in root.winfo_children():
        if widget.winfo_name() == '!label7':
            l = widget
    l['text'] = f'Ruta seleccionada: {file_name}'

def incrementarVI():
    global speed
    if speed > 10:
        speed -= 100
    # print(speed)

def disminuirVI():
    global speed
    if speed < 1310:
        speed += 100
    # print(speed)

def incrementarAN():
    global true_speed
    if true_speed < 50:
        true_speed += 5
    # print(true_speed)

def disminuirAN():
    global true_speed
    if true_speed > 10:
        true_speed -= 5
    # print(true_speed)

def print_tablapag(tabla_pagina):
    i = 0
    s = 'Tabla de página\n\n'
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

def start_iterations(tam_marco, so, proc, marcos, marcos_so, instrucciones):
    clear()
    global anim_speed
    reemplazos = 0
    fallos = 0
    content = ttk.Frame(root, padding=40)

    
    
    paginas_proc = list(range(mt.ceil(proc/tam_marco)))
    tabla_pagina = [[None, 0, 0] for pagina in paginas_proc]
    pilacola = []

    memoria = marcos_so + marcos
    pady=10
    # pady2=70/len(memoria)

    labelinstruccion = ttk.Label(content, text=" ", font=('Helvetica', 12))
    firstlbl = ttk.Label(content, text="Páginas del proceso")
    tabla = ttk.Label(content, text=print_tablapag(tabla_pagina), font=('Helvetica', 14))
    framemedio = ttk.Frame(content, width=600, height=30, relief="ridge")
    secondlbl = ttk.Label(content, text="Marcos en Memoria Principal")
    bitacora = ttk.Label(content, text="", font=('Helvetica', 12))

    labelsPaginas = [ttk.Label(content, text=f'{pagina*tam_marco}-{(pagina*tam_marco + (tam_marco-1))}') for pagina in paginas_proc]
    labelsMP = [ttk.Label(content, text=f'{marco*tam_marco}-{(marco*tam_marco + (tam_marco-1))}') for marco in memoria]
    labelsDirLogica = [ttk.Label(content, text='         ') for marco in memoria]

    bs = [Button(content, text=f'Página {pagina}', width=10, pady=pady, bg='white') for pagina in paginas_proc]
    ms = [Button(content, text=f'Marco {marco}', width=10, pady=pady, bg='yellow') if marco in marcos_so else Button(content, text=f'Marco {marco}', width=10, pady=pady, bg='white') for marco in memoria]

    incrementarVIbt = Button(content, text=f'+ Velocidad Proceso', width=20, pady=pady, bg='#082032', fg='#DDDDDD', command=incrementarVI)
    incrementarANbt = Button(content, text=f'+ Velocidad Animaciones', width=20, pady=pady, bg='#082032',fg='#DDDDDD', command=incrementarAN)
    disminuirVIbt = Button(content, text=f'- Velocidad Proceso', width=20, pady=pady, bg='#FF4C29', command=disminuirVI)
    disminuirANbt = Button(content, text=f'- Velocidad Animaciones', width=20, pady=pady, bg='#FF4C29', command=disminuirAN)

    framebt1 = ttk.Frame(content, width=80, height=25)
    framebt2 = ttk.Frame(content, width=80, height=25)


    last_row = max(len(paginas_proc),len(marcos)) + 2
    
    framebt1.grid(column=0, columnspan=2, row=last_row-1)

    incrementarVIbt.grid(column=0, row=last_row, columnspan=2)
    incrementarANbt.grid(column=0, row=last_row+1, columnspan=2)
    framebt2.grid(column=0, columnspan=2, row=last_row+2)
    disminuirVIbt.grid(column=0, row=last_row+3, columnspan=2)
    disminuirANbt.grid(column=0, row=last_row+4, columnspan=2)

    labelinstruccion.grid(row=0, column=2)
    content.grid(column=0, row=0)
    firstlbl.grid(column=0, row=0, columnspan=2)
    secondlbl.grid(column=3, row=0, columnspan=3)
    for pagina in paginas_proc:
        labelsPaginas[pagina].grid(column=0, row=pagina+1)
        bs[pagina].grid(column=1, row=pagina+1)
    
    tabla.grid(column=2, row=3, rowspan=max(len(paginas_proc),len(marcos)))
    framemedio.grid(column=2 , row=2)
    bitacora.grid(column=2, row=1)

    for i in range(len(memoria)):
        labelsMP[i].grid(column=3, row=i+1)
        ms[i].grid(column=4, row=i+1)
        labelsDirLogica[i].grid(column=5, row=i+1)

    salida_archivo = ''

    for instruccion in instrucciones:
        pag = instruccion[0]//tam_marco
        tipo = "Lectura" if instruccion[1]=='L' else "Escritura"
        salida_archivo += f'Instrucción:      Dirección {instruccion[0]} {tipo}\n'
        labelinstruccion.config(text=f'Instrucción:      Dirección {instruccion[0]} {tipo}   >>>   Pagina {pag}')
        bitacora.config(text=f'La página solicitada es la {pag}')
        salida_archivo += f'La página solicitada es la {pag}\n'

        content.after(speed)
        root.update()
        content.update()

        bitacora.config(text='Ingresando a la tabla de página')
        salida_archivo += f'Ingresando a la tabla de página\n'
        content.after(speed)
        root.update()
        content.update()

        
        try:
            info = tabla_pagina[pag]
        except Exception as e:
            bitacora.config(text='El programa trató acceder a una dirección que no correspondía dentro de las de el')
            salida_archivo += f'El programa trató acceder a una dirección que no correspondía dentro de las de el\n\n'
            content.after(speed)
            root.update()
            content.update()
            continue
        
        #INSERTAR EN MARCO VACIO
        if info[1] == 0:
            fallos +=1
            bitacora.config(text='Fallo de página, no se encontraba cargada')
            salida_archivo += f'Fallo de página, no se encontraba cargada\n'
            content.after(speed)
            root.update()
            content.update()
            if len(marcos)!=0:
                m = marcos.pop(0)

                bitacora.config(text=f'Ingresando la página {pag} al marco {m}')
                salida_archivo += f'Ingresando la página {pag} al marco {m}\n'
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

                rowDestino = bd.grid_info()['row']
                targetLabel = labelsDirLogica[rowDestino-1]
                targetLabel.config(text=f'Página {pag}')

                bo_copy = Button(content, text=bo['text'], width=10, pady=pady, bg='blue')
                bo_copy.grid(row=ro, column=1)
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
                salida_archivo += f'Cambiando el bit de valido/invalido a 1\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][1] = 1
                tabla.config(text=print_tablapag(tabla_pagina))

                tabla_pagina[pag][0] = m
                tabla.config(text=print_tablapag(tabla_pagina))

                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'

            else:
                reemplazos +=1
                LRU = pilacola.pop(0)
                m = tabla_pagina[LRU][0]

                bitacora.config(text=f'La página menos usada recientemente es la página {LRU}, liberando asi el marco {m}')
                salida_archivo += f'La página menos usada recientemente es la página {LRU}, liberando asi el marco {m}\n'
                content.after(speed)
                root.update()
                content.update()

                # SWAP OUT
                if tabla_pagina[LRU][2] == 1:
                    bitacora.config(text='El bit sucio es 1, por tanto hay swap out')
                    salida_archivo += f'El bit sucio es 1, por tanto hay swap out\n'
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
                    bo_copy.grid(row=ro, column=4)

                    while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                        root.update()
                        content.update()

                        content.after(anim_speed2, move, bo_copy, bd, content)
                        content.after(anim_speed)
                    
                    targetLabel = labelsDirLogica[ro-1]
                    targetLabel.config(text=f'         ')
                    bo.configure(background='white')
                    bd.configure(background='white')


                    root.update()
                    content.update()
                    bo_copy.destroy()

  
                else:
                    bitacora.config(text='El bit sucio es 0, por tanto NO hay swap out')
                    salida_archivo += f'El bit sucio es 0, por tanto NO hay swap out\n'
                    content.after(speed)
                    root.update()
                    content.update()
                
                #SWAP IN
                bitacora.config(text=f'Swap in de la página {pag} al marco {m}')
                salida_archivo += f'Swap in de la página {pag} al marco {m}\n'
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
                bo_copy.grid(row=ro, column=1)

                bd.configure(background='red')

                while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                    root.update()
                    content.update()

                    content.after(anim_speed2, move, bo_copy, bd, content)
                    content.after(anim_speed)

                rowDestino = bd.grid_info()['row']
                targetLabel = labelsDirLogica[rowDestino-1]
                targetLabel.config(text=f'Página {pag}')

                root.update()
                content.update()
                bo_copy.destroy()

                bitacora.config(text=f'Borrando la fila de la página {LRU} en la tabla de página')
                salida_archivo += f'Borrando la fila de la página {LRU} en la tabla de página\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[LRU] = [None, 0, 0]
                tabla.config(text=print_tablapag(tabla_pagina))

                tabla_pagina[pag][1] = 1
                tabla_pagina[pag][0] = m
                tabla.config(text=print_tablapag(tabla_pagina))

                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'
                
            if instruccion[1] == 'E':
                bitacora.config(text=f'Escritura en la página {pag}')
                salida_archivo += f'Escritura en la página {pag}\n'
                content.after(speed)
                root.update()
                content.update()

                bitacora.config(text=f'Cambiando el bit sucio de la página {pag} a 1')
                salida_archivo += f'Cambiando el bit sucio de la página {pag} a 1\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][2] = 1
                tabla.config(text=print_tablapag(tabla_pagina))
                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'
            else:
                bitacora.config(text=f'Lectura en la página {pag}')
                salida_archivo += f'Lectura en la página {pag}\n'
                content.after(speed)
                root.update()
                content.update()
        else:
            bitacora.config(text=f'La página se encontraba ya cargada, especificamente en el marco {tabla_pagina[pag][0]}')
            salida_archivo += f'La página se encontraba ya cargada, especificamente en el marco {tabla_pagina[pag][0]}\n'
            content.after(speed)
            root.update()
            content.update()

            if instruccion[1] == 'E':
                bitacora.config(text=f'Escritura en la página {pag}')
                salida_archivo += f'Escritura en la página {pag}\n'
                content.after(speed)
                root.update()
                content.update()

                bitacora.config(text=f'Cambiando el bit sucio de la página {pag} a 1')
                salida_archivo += f'Cambiando el bit sucio de la página {pag} a 1\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][2] = 1
                tabla.config(text=print_tablapag(tabla_pagina))
                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'
            else:
                bitacora.config(text=f'Lectura en la página {pag}')
                salida_archivo += f'Lectura en la página {pag}\n'
                content.after(speed)
                root.update()
                content.update()
                
        if pag in pilacola:
            pilacola.remove(pag)
            pilacola.append(pag)
            salida_archivo += f'Borrando de la pilacola la página {pag} e ingresandola al final\n'
            salida_archivo += f'Pilacola: {str(pilacola)}'
        else:
            pilacola.append(pag)
            salida_archivo += f'Ingresando a la pilacola la página {pag}\n'
            salida_archivo += f'Pilacola: {str(pilacola)}'
        salida_archivo+= f'\n{"-"*30+"//"+"-"*30}\n\n'

    bitacora.config(text=f'Fin de la ejecución, Su bitacora se encuentra en el archivo bitacora.txt')
    salida_archivo += f'Fin de la ejecución\n'
    labelinstruccion.config(text=f'No. Fallos de página: {fallos},   No. reemplazos: {reemplazos}')
    salida_archivo += f'No. Fallos de página: {fallos},   No. reemplazos: {reemplazos}'

    content.after(speed)
    root.update()
    content.update()
        # input('Presione cualquier tecla para seguir a la proxima iteracion')
    
    with open('bitacora.txt', 'w') as f:
        print(salida_archivo, file=f)


def tomar_datos():
    clear()
    # a1,a2,a3,a4 = '5','15','70','8'

    frame = ttk.Frame(content, width=800, height=100).pack()

    tam_marco = Entry(root, width = 60, font=('Helvetica', 14))
    so = Entry(root, width = 60, font=('Helvetica', 14))
    proc = Entry(root, width = 60, font=('Helvetica', 14))
    marcos = Entry(root, width = 60, font=('Helvetica', 14))

    Label(root, text="Tamaño del marco", font=('Helvetica', 14)).pack()

    tam_marco.pack(pady=10)
    tam_marco.insert(0, 'EJ: 16')
    # tam_marco.insert(0, a1)

    tam_marco.configure(state='disabled')

    Label(root, text="Tamaño del SO", font=('Helvetica', 14)).pack()

    so.pack(pady=10)
    so.insert(0, 'EJ: 60')
    # so.insert(0, a2)
    so.configure(state='disabled')

    Label(root, text="Tamaño del proceso", font=('Helvetica', 14)).pack()

    proc.pack(pady=10)
    proc.insert(0, 'EJ: 40')
    # proc.insert(0, a3)
    proc.configure(state='disabled')

    Label(root, text="Marcos disponibles separados por espacio", font=('Helvetica', 14)).pack()

    marcos.pack(pady=10)
    marcos.insert(0, 'EJ: 7 9 10, que no entren en conflicto con los marcos del SO')
    # marcos.insert(0, a4)
    marcos.configure(state='disabled')

    ttk.Frame(content, width=800, height=50).pack()
    Label(root, text="Seleccione su archivo de instrucciones: ", font=('Helvetica', 14)).pack()

    select_file_button = Button(root, text="Seleccionar", command=select_file, pady=2, bg='darkorange', font=('Helvetica', 14)).pack()
    ttk.Frame(content, width=800, height=50).pack()
    ruta = Label(root, text=file_name, font=('Helvetica', 12))
    ruta.pack()    

    ttk.Frame(content, width=800, height=40).pack()
    my_button2 = Button(root, text="Ingresar", command=check_values, font=("Helvetica", 24), fg="#DDDDDD", bg="darkolivegreen").pack()
    


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
        wlabel.config(text="Debe ingresar un número en el campo del tamaño del marco")
        return
    
    if tam_marco <= 0:
        wlabel.config(text="Debe ingresar un número positivo en el campo del tamaño del marco")
        tam_marco = None
        return

    try:
        so = int(so)
    except Exception as e:
        wlabel.config(text="Debe ingresar un número en el campo del tamaño del SO")
        return
        
    if so <= 0:
        wlabel.config(text="Debe ingresar un número positivo en el campo del tamaño del SO")
        return

    try:
        proc = int(proc)
    except Exception as e:
        wlabel.config(text="Debe ingresar un número en el campo del tamaño del proceso")
        return
    
    if proc <= 0:
        wlabel.config(text="Debe ingresar un número positivo en el campo del tamaño del proceso")
        return

    marcos_so = list(range(mt.ceil(so/tam_marco)))
    paginas_proc = list(range(mt.ceil(proc/tam_marco)))

    try:
        temp = marcos.split(' ')
        marcos = [int(s) for s in temp]
        if len(set(marcos)) != len(marcos):
            raise Exception
    except Exception as e:
        wlabel.config(text="Debe ingresar números enteros diferentes separados por espacio, EJ: 7 9 10")
        return
    
    a = set(marcos_so)
    b = set(marcos)
    
    if not all(n >= 0 for n in marcos):
        wlabel.config(text="El número del marco debe ser positivo")
        return
    
    if a & b:
        wlabel.config(text=f'Los marcos libres están en conflictos con los marcos que utilizará el SO que son: {str(marcos_so)}\n')
        return
    
    instrucciones = []

    try:
        with open(file_name, encoding='utf-8-sig') as f:
            opened_file = csv.reader(f, delimiter=',')
            for row in opened_file:
                instrucciones.append(row)
                
        instrucciones = tuple(zip(instrucciones[0], instrucciones[1]))
        instrucciones = [(int(tuple[0]), tuple[1]) for tuple in instrucciones]
    except Exception as e:
        wlabel.config(text=f'Hubo un problema con su archivo, por favor carguelo de nuevo')
        return
    
    marcos = sorted(marcos)
    start_iterations(tam_marco, so, proc, marcos, marcos_so, instrucciones)


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