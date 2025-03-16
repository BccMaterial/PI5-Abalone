class No:
  def __init__(self, estado, no_pai=None, aresta=None, custo=0.0, heuristica=0.0):
    self.estado = estado
    self.no_pai = no_pai
    self.aresta = aresta
    self.custo = custo
    self.heuristica = heuristica

  def __repr__(self):
    return str(self.estado)

  def __lt__(self, outro):
    return (self.custo + self.heuristica) < (outro.custo + outro.heuristica)
