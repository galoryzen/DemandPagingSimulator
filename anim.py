from tkinter import *

root = Tk()
root.title('Simulador paginacion bajo demanda')
root.geometry("800x700")
root.resizable(False,False)
root.config(bg="#082032")


def start():
    my_button.destroy()
    my_button2.pack(pady=100)

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
    for widget in root.winfo_children():
        widget.destroy()
        

tam_marco = Entry(root, width = 60)
so = Entry(root, width = 60)
proc = Entry(root, width = 60)
marcos = Entry(root, width = 60)

text = Label(root, text=" Simulación de la paginación\nbajo demanda controlada por contador",bg="#FF4C29")
text.place(x=300,y=90)

my_button = Button(root, 
    text="Iniciar", 
    command=start,
    font=("Helvetica", 24),
    fg="#DDDDDD",
    bg="#FF4C29")
my_button.pack(pady=100)
my_button.place(x=350, y=525)

my_button2 = Button(root, 
    text="Ingresar", 
    command=check_values,
    font=("Helvetica", 24),
    fg="red")

def on_focus_in(entry):
    if entry.cget('state') == 'disabled':
        entry.configure(state='normal')
        entry.delete(0, 'end')


def on_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.configure(state='disabled')

root.mainloop()

# if __name__ == '__main__':
#     main()