class UnidadFuncional:
    def __init__(self, uso, cont_ciclos, TAG_ROB, opa, opb,operacion,res, res_ok, clk_tick_ok):
        self.uso = uso
        self.cont_ciclos = cont_ciclos
        self.TAG_ROB  = TAG_ROB
        self.opa = opa
        self.opb = opb
        self.operacion = operacion
        self.res = res
        self.res_ok = res_ok
        self.clk_tick_ok = clk_tick_ok