# CODIGOS DE OPERACION
from Memoria import Memoria
from UnidadFuncional import UnidadFuncional
from EstacionReserva import EstacionReserva
from Registro import Registro
from ROB import ROB
from Instruccion import Instruccion

# DECLARACIÓN DE LAS VARIABLES QUE SIMULAN LA MEMORIA DE DATOS, DE INSTRUCCIONES Y BANCO DE REGISTROS

size_REG = 16
size_DAT = 32
size_INS = 32

banco_registros = []
memoria_datos = []
memoria_instrucciones = []

# CODIGOS UNIDADES FUNCIONALES

TOTAL_UF = 3
ALU = 0
MEM = 1
MULT = 2


UF = [[],[],[]]              #UF[0] --> ALU, UF[1] --> LW/SW, UF[2] --> MULT
ER = [[],[],[]]            #ER[0] --> ALU, ER[1] --> MEM, ER[2] --> MULT
Rob = []

# total instrucciones programa
inst_prog = Memoria.cargar_datos("instrucciones.txt")
# instrucciones en rob
inst_rob = 0

# puntero a las posiciones de rob para introducir (cola)
#global p_rob_cabeza         # o retirar instrucciones (cabeza)
p_rob_cola = 0
p_rob_cabeza = 0
# puntero a memoria de intrucciones, siguiente instruccion a IF
PC = 0

# vector de punteros que apuntan a la cola de cada una de las UF
p_er_cola = [0,0,0]

cod_ADD = 1
cod_SUB = 2
cod_LW = 3
cod_SW = 4
cod_MULT = 5


# CICLOS DE EJECUCION POR TIPO DE INSTRUCCION

ciclos_MEM = 2
ciclos_ALU = 1
ciclos_MULT = 5

# ETAPAS DE PROCESAMIENTO DE LAS INSTRUCCIONES EN ROB

rob_ISS = 1
rob_EX = 2
rob_WB = 3

def Etapa_commit():
    print('Etapa commit')
    global p_rob_cabeza
    global inst_rob
    global Rob
    global banco_registros

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
    global UF
    global ciclo
    global Rob
    global memoria_datos
    global TOTAL_UF
    global p_er_cola
    global ER

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

            for i in (range(TOTAL_UF)):
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
            indice = indice + 1


def Etapa_EX():
    print('Etapa EX')
    indice = 0
    ejecutando = False
    global TOTAL_UF
    global ciclos_ALU
    global ciclos_MULT
    global ciclos_MEM
    global ciclo
    global UF
    global ER
    global Rob
    global p_er_cola



    while indice < TOTAL_UF:
        aux = UF[indice]
        maximo = 0

        if indice == 0:
            maximo = ciclos_ALU
        elif indice == 1:
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

                j = j + 1
        indice = indice + 1

def Etapa_ID_ISS():
    print('Etapa ID_ISS')
    global inst_prog
    global memoria_instrucciones
    global ciclos_ALU
    global ciclos_MULT
    global ciclos_MEM
    global p_er_cola
    global p_rob_cola
    global p_rob_cabeza
    global Rob
    global ER
    global rob_ISS
    global banco_registros
    global PC
    if (inst_prog > 0):

        # Leemos instruccion directamente de la memoria
        inst = memoria_instrucciones[PC]
        PC = PC +1
        #Creamos su linea en la ER
        linea_aux = EstacionReserva(0,0,0,0,0,0,0,0,0,0)

        # Obtenemos el código para determinar la ER correspondiente
        cod_ins = inst.getCod()
        cod_uf = 0
        ciclos_ex = ciclos_ALU

        if (cod_ins == 3 or cod_ins == 4): #carga almacenamiento
            cod_uf = 1
            ciclos_ex = ciclos_MEM
        if (cod_ins == 5): #mult
            cod_uf = 2
            ciclos_ex = ciclos_MULT
        # Puntero de la ER

        puntero_er = p_er_cola[cod_uf]


        #Actualizar linea
        linea_aux.linea_valida = 1
        linea_aux.operacion = cod_ins
        #Buscar operando A

        opA = buscarRegistro(inst.rs)
        if ( opA.getOk() == 1 ):                # Si está disponible
            linea_aux.opa = opA.contenido       # cargar op en opA
            linea_aux.opa_ok = 1                 # y validar en opA_ok y clk_tick_ok_a
            linea_aux.clk_tick_ok_a += 1
        else: #poner linea ROB que proporciona el operando
            linea_aux.opa = opA.TAG_ROB
            linea_aux.opa_ok = 0
            linea_aux.clk_tick_ok_a = Rob[opA.TAG_ROB].clk_tick_ok
        #Buscar operando B

        opB = buscarRegistro(inst.getRt())
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
        linea_rob = ROB(p_rob_cola, 0, inst.getRd(), 0, 0, ciclos_ex, rob_ISS)
        if (cod_ins == 4):
            linea_rob.destino = 0
        Rob[p_rob_cola] = linea_rob

        #Actualizamos banco de registros
        regD= buscarRegistro(inst.getRd()) #TODO Revisar
       # regD = banco_registros[posR]
        regD.ok = 0
        regD.TAG_ROB = p_rob_cola
        p_rob_cola += 1
        inst_prog -= 1


def buscarRegistro(reg):
    a = str(reg)
    if(len(a)>2):
        num = (a[:-1])

        print (num)
        return banco_registros[num]
    return Registro(0,0,0,0)


if __name__ == '__main__':



    #TODO miralo diego, no se como inicializarlo
    #iniciamos simulador
    #leemos las instrucciones y las codificamos
    memoria_instrucciones = Memoria.instrucciones
    print ('\nInstrucciones')
    for i in memoria_instrucciones:
        print (i.toString())
    print ('\n')
    # Inicializamos ER [3][32] y UF
    for i in range(TOTAL_UF):
        UF[i] = UnidadFuncional(0,0,0,0,0,0,0,0,0)
        for j in range(32):
            ER[i].append(EstacionReserva(0,0,0,0,0,0,0,0,0,0))

    # Inicializamos ROB

    for i in range(32):
        a = ROB(0,0,0,0,0,0,0)
        Rob.append(a)

    # Ini Banco Registros
    for i in range(16):
        banco_registros.append(Registro(i,1,1,-1))

    # Ini Mem. Datos
    for i in range(32):
        memoria_datos.append(i*2)

    ciclo = 1

    while((inst_rob > 0) or (inst_prog > 0)):
            Etapa_commit()
            Etapa_WB()
            Etapa_EX()
            Etapa_ID_ISS()
            ciclo = ciclo +1
            # imprimir las distintas estructuras
            print('\nCICLO N: '+str(ciclo))
            #print Mostrar ER
            print('\nER')
            for i in range(len(ER)):
                for j in range(len(ER[0])):
                    print('[i'+str(i)+' j'+str(j)+'] : '+str(ER[i][j].toString()))


            #print Mostrar ROB
            print('\nROB')
            for i in range(len(Rob)):
                print(Rob[i].toString())

            #print Banco de registros
            print('\nRegistros')
            for i in range(len(banco_registros)):
                print(banco_registros[i].toString())

            print('\nUnidad Funcional')
            for i in range(len(UF)):
                print(UF[i].toString())

            print('\nMemoria de datos')
            for i in range(32):
                print ('Memoria: '+str(i)+' -> '+str(memoria_datos[i]))

            print('\n-----------------CICLO N: '+str(ciclo)+'-----------------')

