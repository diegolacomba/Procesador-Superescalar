class EstacionReserva:
    def __init__(self, linea_valida, TAG_ROB, operacion, opa, opa_ok, clk_tick_ok_a, opb, opb_ok, clk_tick_ok_b, inmediato):
        self.linea_valida = linea_valida
        self.TAG_ROB = TAG_ROB
        self.operacion = operacion
        self.opa = opa
        self.opa_ok = opa_ok
        self.clk_tick_ok_a = clk_tick_ok_a
        self.opb = opb
        self.opb_ok = opb_ok
        self.clk_tick_ok_b = clk_tick_ok_b
        self.inmediato = inmediato

    def toString(self):
        return ('linea_valida: ' + str(self.linea_valida) + ' TAG_ROB: ' + str(self.TAG_ROB) + ' operacion: ' + str(self.operacion) + ' opa: ' + str(
            self.opa) + ' opa_ok: ' + str(self.opa_ok)+ ' clk_tick_ok_a: '+str(self.clk_tick_ok_a)+' opb: '+str(self.opb) + ' opb_ok: '+str(self.opb_ok)+ ' clk_tick_ok_b: '+str(self.clk_tick_ok_b))
