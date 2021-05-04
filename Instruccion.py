class Instruccion:
    def __init__(self, cod, rd, rs, rt, inm):
        self.cod = cod
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.inm = inm
    def toString(self):
        return ('cod: '+str(self.cod)+' rd: '+str(self.rd)+' rs: '+str(self.rs)+' rt: '+str(self.rt)+' inm: '+str(self.inm))

    def getCod(self):
        return self.cod

    def getRd(self):
        return self.rd

    def getRs(self):
        return self.rs

    def getRt(self):
        return self.rt

    def getinm(self):
        return self.inm