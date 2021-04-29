from Instruccion import Instruccion


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
class Memoria:

    def cargar_datos(fichero):
        archivo = open(fichero, "r")
        lectura = []
        for count, value in enumerate(archivo.readlines()):
            list = decodificar(value)
            lectura.append(Instruccion(list[0],list[1],list[2],list[3],list[4]))

        archivo.close()
        for e in lectura:
            print(e.toString())


    if __name__ == '__main__':
        cargar_datos('instrucciones.txt')
