import math as mt
import os

def print_tablapag(tabla_pagina):
    i = 0
    print('i | m | bv | bs |')
    for row in tabla_pagina:
        print(f'{i} | {row[0] if row[0] != None else "-"} | {row[1]}  | {row[2]}  |')
        i+=1
        

tam_marco, so, proc, marcos = None, None, None, None

while not tam_marco:
    try:
        tam_marco = int(input("Ingrese el tamano del marco  "))
    except Exception as e:
        print('Debe ingresar un numero\n')
        continue
    if tam_marco <= 0:
        print('Ingrese un numero positivo\n')
        tam_marco = None
    
while not so:
    try:
        so = int(input("Ingrese el tamano del SO  "))
    except Exception as e:
        print('Debe ingresar un numero\n')
        continue
    
    if so <= 0:
        print('Ingrese un numero positivo\n')
        so = None

while not proc:
    try:
        proc = int(input("Ingrese el tamano del proceso  "))
    except Exception as e:
        print('Debe ingresar un numero\n')
        continue
    
    if proc <= 0:
        print('Ingrese un numero positivo\n')
        proc = None

marcos_so = list(range(mt.ceil(so/tam_marco)))
paginas_proc = list(range(mt.ceil(proc/tam_marco)))


while not marcos:
    try:
        temp = input("Ingrese la lista de marcos separados por espacio  ").split(' ')
        marcos = [int(s) for s in temp]
        if len(set(marcos)) != len(marcos):
            raise Exception
    except Exception as e:
        marcos = None
        temp = None
        print('Debe ingresar numeros enteros diferentes separados por espacio, EJ: 7 9 10\n')
        continue
    
    a = set(marcos_so)
    b = set(marcos)
    
    if not all(n >= 0 for n in marcos):
        print('El numero del marco debe ser positivo\n')
        temp = None
        marcos = None
        continue
    
    if a & b:
        print(f'Los marcos libres estan en conflictos con los marcos que utilizará el SO que son: {" ".join(temp)}\n')
        marcos = None
        temp = None
        continue
        
print(marcos)

with open(f"{__file__.rstrip('main.py')}input.txt", "r") as f:
    instrucciones = [line.strip().split(' ') for line in f]
    
instrucciones = [(int(tuple[0]), tuple[1]) for tuple in instrucciones]

# tam_marco, so, proc, marcos = 2, 4, 6, [5]
# paginas_proc = list(range(mt.ceil(proc/tam_marco)))

tabla_pagina = [[None, 0, 0] for pagina in paginas_proc]

pilacola = []

for instruccion in instrucciones:
    pag = instruccion[0]//tam_marco
    print(f'La pagina solicitada es la {pag}')
    print('Ingresando a la tabla de pagina')
    
    try:
        info = tabla_pagina[pag]
    except Exception as e:
        print('El programa trató acceder a una dirección que no correspondía dentro de las de el')
        continue
    
    if info[1] == 0:
        print('Fallo de pagina, no se encontraba cargada')
        if len(marcos)!=0:
            m = marcos.pop(0)
            print(f'Ingresando la pagina {pag} al marco {m}')
            print(f'Cambiando el bit de valido/invalido a 1')
            tabla_pagina[pag][1] = 1
            tabla_pagina[pag][0] = m
        else:
            LRU = pilacola.pop(0)
            m = tabla_pagina[LRU][0]
            print(f'La pagina menos usada recientemente es la pagina {LRU}, liberando asi el marco {m}')
            
            if tabla_pagina[LRU][2] == 1:
                print(f'El bit sucio es 1, por tanto hay swap out')
            else:
                print(f'El bit sucio es 0, por tanto NO hay swap out')
            
            print(f'Swap in de la pagina {pag} al marco {m}')
            tabla_pagina[LRU] = [None, 0, 0]
            print(f'Borrando la fila de la pagina {LRU} en la tabla de pagina')
            tabla_pagina[pag][1] = 1
            tabla_pagina[pag][0] = m
            
            
        if instruccion[1] == 'E':
            print(f'Escritura en la pagina {pag}')
            print(f'Cambiando el bit sucio de la pagina {pag} a 1')
            tabla_pagina[pag][2] = 1
        else:
            print(f'Lectura en la pagina {pag}')
    else:
        print(f'La pagina se encontraba ya cargada, especificamente en el marco {tabla_pagina[pag][0]}')
        if instruccion[1] == 'E':
            print(f'Escritura en la pagina {pag}')
            print(f'Cambiando el bit sucio de la pagina {pag} a 1')
            tabla_pagina[pag][2] = 1
        else:
            print(f'Lectura en la pagina {pag}')
            
    if pag in pilacola:
        pilacola.remove(pag)
        pilacola.append(pag)
        print(f'Borrando de la pilacola la pagina {pag} e ingresandola al final')
    else:
        pilacola.append(pag)
        print(f'Ingresandola a la pilacola la pagina {pag}')
        
    print()
    print_tablapag(tabla_pagina)
    print()
    print(pilacola)
    input('Presione cualquier tecla para seguir a la proxima iteracion')


# if __name__ == '__main__':
#     main()