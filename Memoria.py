from Instruccion import Instruccion

global instrucciones

def decodificar(value):
    datos = value.split()
    cod = 0
    inm = 0
    dades =datos[1].split(',')

    rd = dades[0]
    rs = dades[1]
    rt = dades[2]
    inm = -1
    op = datos[0]
    if (op == 'add'):
        cod = 1
    elif (op == 'sub'):
        cod = 2
    elif (op == 'lw'):
        inm = dades[1]
        cod = 3
        rs = -1
    elif (op == 'sw'):
        inm = dades[1]
        rs = -1
        cod = 4
    else:
        cod = 5
    return [cod, rd, rs, rt, inm]


def cargar_datos(fichero):
    archivo = open(fichero, "r")
    instrucciones = []
    for count, value in enumerate(archivo.readlines()):
        list = decodificar(value)
        instrucciones.append(Instruccion(list[0],list[1],list[2],list[3],list[4]))

    archivo.close()
    return len(instrucciones)

class Memoria:
    if __name__ == '__main__':
        cargar_datos('instrucciones.txt')
