# CODIGOS DE OPERACION
import ROB
import UnidadFuncional
from EstacionReserva import EstacionReserva
from Registro import Registro

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


if __name__ == '__main__':

    # DECLARACIÓN DE LAS VARIABLES QUE SIMULAN LA MEMORIA DE DATOS, DE INSTRUCCIONES Y BANCO DE REGISTROS

    global banco_registros
    global memoria_datos
    global memoria_instrucciones
    banco_registros = Registro[size_REG]
    memoria_datos = [size_DAT]
    memoria_instrucciones = [size_INS]

    global UF
    global ER
    global Rob
    UF = UnidadFuncional[TOTAL_UF]              #UF[0] --> ALU, UF[1] --> LW/SW, UF[2] --> MULT
    ER = EstacionReserva[TOTAL_UF][size_INS]    #ER[0] --> ALU, ER[1] --> MEM, ER[2] --> MULT
    Rob = ROB[size_INS]

    global inst_prog            # total instrucciones programa
    global inst_rob             # instrucciones en rob
    inst_rob = 0

    global p_rob_cola           # puntero a las posiciones de rob para introducir (cola)
    global p_rob_cabeza         # o retirar instrucciones (cabeza)
    p_rob_cola = 0

    global PC                   # puntero a memoria de intrucciones, siguiente instruccion a IF
    PC = 0

    global p_er_cola[TOTAL_UF]  # vector de punteros que apuntan a la cola de cada una de las UF
    p_er_cola = [0,0,0]

