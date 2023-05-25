import networkx as nx

class GraphManager:
  def __init__(self, G=None, pos=None, labels=None, edge_labels=None):
    if G is None:
      self.G = nx.Graph()
    else:
      self.G = G

    # We have to have positions otherwise we can draw the nodes
    if pos is None:
      self.pos = {}
    else:
      self.pos = pos

    # Node labels default to the names given to the nodes when adding them to
    # the graph, but they can be overridden when drawing.
    self.labels = labels
    
    # There are no edge labels by default, but some can be supplied if desired.
    self.edge_labels = edge_labels