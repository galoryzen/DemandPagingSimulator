import math as mt

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

while not so:
    try:
        so = int(input("Ingrese el tamano del SO  "))
    except Exception as e:
        print('Debe ingresar un numero\n')
        continue
    
    if so <= 0:
        print('Ingrese un numero positivo\n')
        so = None

marcos_so = list(range(mt.ceil(so/tam_marco)))

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





# if __name__ == '__main__':
#     main()