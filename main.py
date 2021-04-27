# CODIGOS DE OPERACION
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
    print("Hello")
