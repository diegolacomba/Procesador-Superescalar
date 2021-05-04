class Registro:
    def __init__(self, contenido, ok, clk_tick_ok, TAG_ROB): # Contenido, contenido valido (1) o no (0), a partir d q ciclo el contenido es ok, linea de ROB q actualiza
        self.contenido = contenido
        self.ok = ok
        self.clk_tick_ok = clk_tick_ok
        self.TAG_ROB = TAG_ROB
    def getContenido(self):
        return self.contenido
    def getOk(self):
        return self.ok
    def getClk_tick_ok(self):
        return self.clk_tick_ok
    def getTag_ROB(self):
        return self.TAG_ROB

    def toString(self):
        return ('contenido: ' + str(self.contenido) + ' ok: ' + str(self.ok) + ' clk_tick_ok: ' + str(self.clk_tick_ok) + ' TAG_ROB: ' + str(
            self.TAG_ROB) )