from tkinter import *
from tkinter import ttk
import asyncio

import time
# relief="ridge"
root = Tk()
root.title('Simulador paginacion bajo demanda')
root.geometry("800x700")
root.resizable(False,False)
content = ttk.Frame(root, padding=40)

paginas = list(range(7))
marcos = [0, 1, 2, 3, 5, 9, 10, 12]

def hhh():
    for i in range(10000):
        print(i)

def move(button, buttondest):
    root.update()
    content.update()
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

def start():
    root.update()
    content.update()
    # for widget in content.winfo_children():
    #     if widget.widgetName == 'button':
    #         print(widget.winfo_x(), widget.winfo_y(), widget.widgetName)

    # for widget in content.winfo_children():
    #     if widget.widgetName == 'button':
    #         # if widget.grid_info()['row']
    #         print(widget.grid_info())
    bt = content.winfo_children()[3:7]
    bd = content.winfo_children()[-1]
    bd.configure(background='red')

    move(bt[0], bd)
    move(bt[1], bd)

    # for button in bt:
    #     move(button, bd)
    #     content.after(700)
    #     print('hola')
    #     content.after(700)
    #     print('hola2')

pady=70/len(paginas)
pady2=70/len(marcos)

firstlbl = ttk.Label(content, text="Paginas del proceso")
framemedio = ttk.Frame(content, width=400, height=600, relief="ridge")
secondlbl = ttk.Label(content, text="Marcos en Memoria Principal")
bs = [Button(content, text=f'Pagina {pagina}', command=start, width=10, pady=pady) for pagina in paginas]
ms = [Button(content, text=f'Marco {marco}', command=start, width=10, pady=pady2) for marco in marcos]

# button = Button(content, text='Iniciar', command=start, pady=20)
# button2 = Button(content, text='Terminar', command=start)


content.grid(column=0, row=0)
firstlbl.grid(column=0, row=0)
secondlbl.grid(column=2, row=0)
for pagina in paginas:
    bs[pagina].grid(column=0, row=pagina+1)

framemedio.grid(column=1 , row=0, rowspan=len(paginas)+4)

for i in range(len(marcos)):
    ms[i].grid(column=2, row=i+1)

root.update()

root.mainloop()

# if __name__ == '__main__':
#     main()