# CODIGOS DE OPERACION
import Memoria
import ROB
import UnidadFuncional
from EstacionReserva import EstacionReserva
from Registro import Registro
# DECLARACIÓN DE LAS VARIABLES QUE SIMULAN LA MEMORIA DE DATOS, DE INSTRUCCIONES Y BANCO DE REGISTROS

global banco_registros
global memoria_datos
global memoria_instrucciones
banco_registros = [size_REG]
memoria_datos = [size_DAT]
memoria_instrucciones = [size_INS]

global UF
global ER
global Rob
UF = [TOTAL_UF]              #UF[0] --> ALU, UF[1] --> LW/SW, UF[2] --> MULT
ER = [TOTAL_UF][size_INS]    #ER[0] --> ALU, ER[1] --> MEM, ER[2] --> MULT
Rob = [size_INS]

global inst_prog           # total instrucciones programa
inst_prog = Memoria.cargar_datos("instrucciones.txt")
global  inst_rob             # instrucciones en rob
inst_rob = 0

global p_rob_cola           # puntero a las posiciones de rob para introducir (cola)
global p_rob_cabeza         # o retirar instrucciones (cabeza)
p_rob_cola = 0
p_rob_cabeza = 0
global PC                   # puntero a memoria de intrucciones, siguiente instruccion a IF
PC = 0

global p_er_cola  # vector de punteros que apuntan a la cola de cada una de las UF
p_er_cola = [0,0,0]
global cod_ADD
global cod_SUB
global cod_LW
global cod_SW
global cod_MULT

cod_ADD = 1
cod_SUB = 2
cod_LW = 3
cod_SW = 4
cod_MULT = 5

global size_REG # NUMERO REGISTROS
global size_DAT # TAMAÑO MEMORIA DATOS
global size_INS # TAMAÑO MEMORIA INSTRUCCIONES

size_REG = 16
size_DAT = 32
size_INS = 32

# CODIGOS UNIDADES FUNCIONALES
global TOTAL_UF
global ALU
global MEM
global MULT

TOTAL_UF = 3
ALU = 0
MEM = 1
MULT = 2

# CICLOS DE EJECUCION POR TIPO DE INSTRUCCION
global ciclos_MEM
global ciclos_ALU
global ciclos_MULT

ciclos_MEM = 2
ciclos_ALU = 1
ciclos_MULT = 5

# ETAPAS DE PROCESAMIENTO DE LAS INSTRUCCIONES EN ROB
global rob_ISS
global rob_EX
global rob_WB

rob_ISS = 1
rob_EX = 2
rob_WB = 3

def Etapa_commit():
    print('Etapa commit')
    if((Rob[p_rob_cabeza].linea_valida == -1) and (Rob[p_rob_cabeza].etapa == 3)):
        if(Rob[p_rob_cabeza].destino != -1):
            registro_Id = Rob[p_rob_cabeza].destino
            if((Rob[p_rob_cabeza].TAG_ROB) == (banco_registros[registro_Id].TAG_ROB)):
                banco_registros[registro_Id].contenido = Rob[p_rob_cabeza].valor
                banco_registros[registro_Id].ok = 1
                banco_registros[registro_Id].clk_tick_ok = banco_registros[registro_Id].clk_tick_ok +1

        Rob[p_rob_cabeza] = ROB(-1,0,0,0,1,0,0)
        p_rob_cabeza = p_rob_cabeza +1
        inst_rob = inst_rob - 1



def Etapa_WB():
    print('Etapa WB')
    indice = 0
    siguiente = True

    while(siguiente and  indice < TOTAL_UF):
        if (UF[indice].uso == 1 and UF[indice].res_ok == 1 and UF[indice].clk_tick_ok <= ciclo):
            res = UF[indice].res
            if (UF[indice].operacion == 3): #LW
                Rob[UF[indice].TAG_ROB].valor = memoria_datos[res]
            else:
                Rob[UF[indice].TAG_ROB].valor = res

            Rob[UF[indice].TAG_ROB].valor_ok = 1
            Rob[UF[indice].TAG_ROB].linea_valida = 1
            Rob[UF[indice].TAG_ROB].clk_tick_ok = 1
            identificador = UF[indice].TAG_ROB

            Rob[identificador].etapa = 3 # WB
            siguiente = False

            for i in (TOTAL_UF):
                fin = p_er_cola[i]
                for j in range(fin):
                    if ER[i][j].linea_valida == 1:
                        if ER[i][j].opa_ok == 0 and ER[i][j].opa == identificador:
                            ER[i][j].opa = Rob[UF[indice]].TAG_ROB.valor
                            ER[i][j].opa_ok = 1
                            ER[i][j].clk_tick_ok_a = ciclo + 1
                        if ER[i][j].opb_ok == 0 and ER[i][j].opb == identificador:
                            ER[i][j].opb = Rob[UF[indice]].TAG_ROB.valor
                            ER[i][j].opb_ok = 1
                            ER[i][j].clk_tick_ok_b = ciclo + 1

            UF[indice] = UnidadFuncional(0,0,0,0,0,0,0,0,0)
        else:
            indice = indice +1


def Etapa_EX():
    print('Etapa EX')
    indice = 0
    ejecutando = False

    while indice < TOTAL_UF:
        aux = UF[ciclo]
        maximo = 0
        if ciclo == 0:
            maximo = ciclos_ALU
        elif ciclo == 1:
            maximo = ciclos_MEM
        else:
            maximo = ciclos_MULT
        if aux.uso == 1:
            if aux.cont_ciclos < maximo:
                aux.cont_ciclos = aux.cont_ciclos + 1
                if aux.cont_ciclos == maximo:
                    operacion = aux.operacion
                    if operacion == 4 or operacion == 3:  # SW LW
                        aux.res = aux.opa + aux.opb
                        aux.res_ok = 1
                        aux.clk_tick_ok = aux.clk_tick_ok + 1
                    if operacion == 1:  # SUB
                        aux.res = aux.opa - aux.opb
                        aux.res_ok = 1
                        aux.clk_tick_ok = aux.clk_tick_ok + 1
                    if operacion == 1:  # ADD
                        aux.res = aux.opa + aux.opb
                        aux.res_ok = 1
                        aux.clk_tick_ok = aux.clk_tick_ok + 1

                    if operacion == 5:  # Mult
                        aux.res = aux.opa * aux.opb
                        aux.res_ok = 1
                        aux.clk_tick_ok = aux.clk_tick_ok + 1
        elif ejecutando == False:
            aux_er = ER[indice]
            fin = p_er_cola[indice]
            j = 0
            while ejecutando == False and j < fin:
                if(Rob[aux_er[j].TAG_ROB].valor != 1):
                    if aux_er[j].linea_valida == 1:
                        if aux_er[j].opa_ok and aux_er[j].clk_tick_ok_a <= ciclo and aux_er[j].opb_ok and aux_er[j].clk_tick_ok_b <= ciclo:
                            penaliza = 0
                            usado = True
                            op = aux_er[j].operacion
                            if op == 5:  # Mult
                                pen = ciclos_MULT
                            if op == 1 or op == 2 :  # ADD SUB
                                pen = ciclos_ALU
                            if op == 3 or op == 4:  # LW SW
                                pen = ciclos_MEM

                            if usado:
                                UF[indice] = UnidadFuncional(1,0,aux_er.TAG_ROB,aux_er.opa,aux_er.opb,aux_er.operacion,0,0,ciclo)
                            else:
                                UF[indice] = UnidadFuncional(1,0,aux_er.TAG_ROB,aux_er.opa,aux_er.inmediato,aux_er.operacion,0,0,ciclo)
                            Rob[aux_er[j].TAG_ROB].etapa = 2
                            ejecutando = True
                            indice = indice -1
                j = j +1

def Etapa_ID_ISS():
    print('Etapa ID_ISS')
    if (inst_prog > 0):

        # Leemos instruccion directamente de la memoria
        inst = memoria_instrucciones[PC]

        #Creamos su linea en la ER
        linea_aux = EstacionReserva()

        # Obtenemos el código para determinar la ER correspondiente
        cod_ins = inst.getCod()
        cod_uf = 0
        ciclos_ex = ciclos_ALU
        if (cod_ins == 3 or cod_ins == 4):
            cod_uf = 1
            ciclos_ex = ciclos_MEM
        if (cod_ins == 5):
            cod_uf = 2
            ciclos_ex = ciclos_MULT

        # Puntero de la ER
        puntero_er = p_er_cola[cod_uf]

        #Actualizar linea
        linea_aux.linea_valida = 1
        linea_aux.operacion = cod_ins
        #Buscar operando A
        opA = buscarRegistro(inst.getRs)
        if ( opA.getOk() == 1 ):                # Si está disponible
            linea_aux.opa = opA.contenido       # cargar op en opA
            linea_aux.opa_ok = 1                 # y validar en opA_ok y clk_tick_ok_a
            linea_aux.clk_tick_ok_a += 1
        else: #poner linea ROB que proporciona el operando
            linea_aux.opa = opA.TAG_ROB
            linea_aux.opa_ok = 0
            linea_aux.clk_tick_ok_a = Rob[opA.TAG_ROB].clk_tick_ok
        #Buscar operando B
        opB = buscarRegistro(inst.getRt)
        if (opB.getOk() == 1):  # Si está disponible
            linea_aux.opb = opB.contenido  # cargar op en opB
            linea_aux.opb_ok = 1  # y validar en opB_ok y clk_tick_ok_b
            linea_aux.clk_tick_ok_b += 1
        else:  # poner linea ROB que proporciona el operando
            linea_aux.opb = opB.TAG_ROB
            linea_aux.opb_ok = 0
            linea_aux.clk_tick_ok_b = Rob[opB.TAG_ROB].clk_tick_ok

        linea_aux.inmediato = inst.getinm()

        # Introducimos en ER correspondiente
        ER[cod_uf][puntero_er] = linea_aux
        p_er_cola[cod_uf] += 1

        # Introducir instrucción en ROB y actualizar campos
        linea_rob = ROB(p_rob_cola, 0, inst.getRd, 0, 0, ciclos_ex, rob_ISS)
        if (cod_ins == 4):
            linea_rob.destino = 0
        Rob[p_rob_cola] = linea_rob

        #Actualizamos banco de registros
        regD = banco_registros[inst.getRd]
        regD.ok = 0
        regD.TAG_ROB = p_rob_cola
        p_rob_cola += 1
        inst_prog -= 1


def buscarRegistro(self, reg):
    num = int(reg[:-1])
    return banco_registros[num]


if __name__ == '__main__':



    #TODO miralo diego, no se como inicializarlo
    #iniciamos simulador
    #leemos las instrucciones y las codificamos
    memoria_instrucciones = Memoria.instrucciones

    # Inicializamos ER [3][32]
    for i in range(TOTAL_UF):
        for j in range(32):
            ER[i][j] = None

    # Inicializamos ROB
    for i in range(32):
         Rob[i] = ROB()

    # Ini Banco Registros
    for i in range(16):
        banco_registros[i] = Registro(0,1,1,-1)

    # Ini Mem. Datos
    for i in range(32):
        memoria_datos[i] = i

    global ciclo
    ciclo = 1

    while((inst_rob > 0) or (inst_prog > 0)):
            Etapa_commit()
            Etapa_WB()
            Etapa_EX()
            Etapa_ID_ISS()
            ciclo = ciclo +1
            # imprimir las distintas estructuras
            print('CICLO N: '+ciclo)
            #print Mostrar ER
            print('ER')
            for i in range(len(ER)):
                for j in range(len(ER[0])):
                    print('i'+str(i)+' j'+str(j)+': '+str(ER[i][j]))


            #print Mostrar ROB
            print('ROB')
            for i in range(len(ROB)):
                print(ROB[i])

            #print Banco de registros
            print('Registros')
            for i in range(len(banco_registros)):
                print(banco_registros[i])
