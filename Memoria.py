from Instruccion import Instruccion
class Memoria:

    def cargar_datos(fichero):
        archivo = open(fichero, "r")
        lectura = []
        for count, value in enumerate(archivo.readlines()):

            lectura.append(Instruccion(decodificar(value)))

        archivo.close()
        for e in lectura:
            print(e)
    def decodificar(value):
        datos = value.split()
        cod=0
        inm=0
        rd = datos[1]
        rs = datos[2]
        rt = datos[3]
        inm= -1
        op = datos[0]
        if (op == 'add') :
            cod = 1
        elif(op == 'sub'):
            cod = 2
        elif (op == 'lw'):
            inm = datos[2]
            cod = 3
            rs = -1
        elif (op == 'sw'):
            inm = datos[2]
            rs = -1
            cod = 4
        else :
            cod = 5
        return [cod, rd, rs, rt, inm]


