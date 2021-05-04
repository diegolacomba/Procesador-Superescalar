class ROB:
    def __init__(self, TAG_ROB, linea_valida, destino, valor, valor_ok, clk_tick_ok, etapa):
        self.TAG_ROB = TAG_ROB
        self.linea_valida = linea_valida
        self.destino = destino
        self.valor = valor
        self.valor_ok = valor_ok
        self.clk_tick_ok = clk_tick_ok
        self.etapa = etapa

    def toString(self):
        return ('TAG_ROB: ' + str(self.TAG_ROB) + ' linea_valida: ' + str(self.linea_valida) + ' destino: ' + str(self.destino) + ' valor: ' + str(
            self.valor) + ' valor_ok: ' + str(self.valor_ok)+ ' clk_tick_ok: '+str(self.clk_tick_ok)+' etapa: '+str(self.etapa))


