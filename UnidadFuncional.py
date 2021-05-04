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

    def toString(self):
        return ('uso: ' + str(self.uso) + ' cont_ciclos: ' + str(self.cont_ciclos) + ' TAG_ROB: ' + str(
            self.TAG_ROB) + ' opa: ' + str(
            self.opa) + ' opb: ' + str(self.opb) + ' operacion: ' + str(self.operacion) + ' res: ' + str(
            self.res) + ' res_ok: ' + str(self.res_ok) + ' clk_tick_ok: ' + str(self.clk_tick_ok))
