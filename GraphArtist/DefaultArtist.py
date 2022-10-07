import wx
import math
import numpy as np
import Globals

class DefaultArtist:
  def __init__(self):
    pass

  def DrawBackground(self, dc):
    backgroundColor = Globals.canvas.GetBackgroundColour()#wx.Color('WHITE')
    dc.SetBrush(wx.Brush(backgroundColor))
    dc.SetPen(wx.Pen(backgroundColor, 1))
    dc.DrawRectangle(0, 0, Globals.canvas.client_size.width, Globals.canvas.client_size.height)

  def DrawAxes(self, dc):
    dc.SetPen(wx.BLACK_PEN)
    unscrolledZeroX, unscrolledZeroY = Globals.canvas.CalcUnscrolledPosition(0, 0)
    origin = Globals.canvas.WorldToClient((0,0))

    top = origin[0], unscrolledZeroY
    bottom = origin[0], Globals.canvas.client_size.height + unscrolledZeroY
    left = unscrolledZeroX, origin[1]
    right = Globals.canvas.client_size.width + unscrolledZeroX, origin[1]

    pts = np.array([
      [ top[0],  top[1]  ],
      [ bottom[0], bottom[1] ]
      ]).astype('intc')
    dc.DrawLinesFromBuffer(pts)

    pts = np.array([
      [ left[0],   left[1]   ],
      [ right[0],  right[1]  ]
      ]).astype('intc')
    dc.DrawLinesFromBuffer(pts)

    ticks = int(math.floor(Globals.canvas.x_max - Globals.canvas.x_min / Globals.canvas.x_scale))
    for i in range(0, ticks):
      p = Globals.canvas.WorldToClient((i * Globals.canvas.x_scale, 0.0))
      pts = np.array([
        [ p[0], p[1]   ],
        [ p[0], p[1] + 5 ],
        ]).astype('intc')
      dc.DrawLinesFromBuffer(pts)

      p = Globals.canvas.WorldToClient((-i*Globals.canvas.x_scale, 0.0))
      pts = np.array([
        [ p[0], p[1]   ],
        [ p[0], p[1] + 5 ],
        ]).astype('intc')
      dc.DrawLinesFromBuffer(pts)

    ticks = int(math.floor(Globals.canvas.y_max - Globals.canvas.y_min / Globals.canvas.y_scale))
    for i in range(0, ticks):
      p = Globals.canvas.WorldToClient((0.0, i * Globals.canvas.y_scale))
      pts = np.array([
        [ p[0],   p[1] ],
        [ p[0] - 5, p[1] ],
        ]).astype('intc')
      dc.DrawLinesFromBuffer(pts)

      p = Globals.canvas.WorldToClient((0.0, -i * Globals.canvas.y_scale))
      pts = np.array([
        [ p[0],   p[1] ],
        [ p[0] - 5, p[1] ],
        ]).astype('intc')
      dc.DrawLinesFromBuffer(pts)

  def DrawAllEdges(self, dc):
    edges = Globals.G.edges()
    for e in edges:
      self.__DrawEdge(dc, e)

  def __DrawEdge(self, dc, e):
    ei = e[1], e[0]
    if e in Globals.canvas.selected_edges or ei in Globals.canvas.selected_edges:
      edgePen = wx.Pen(Globals.canvas.graph_colors[0], 2, wx.SOLID)
    else:
      edgePen = wx.Pen(Globals.canvas.graph_colors[1], 2, wx.SOLID)
    dc.SetPen(edgePen)

    x1, y1 = Globals.G.vpos[e[0]]
    x2, y2 = Globals.G.vpos[e[1]]
    cx1, cy1 = Globals.canvas.WorldToClient( (x1, y1) )
    cx2, cy2 = Globals.canvas.WorldToClient( (x2, y2) )
    #x0 = (x1 + x2) / 2
    #y0 = (y1 + y2) / 2

    #r = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )
    #x = x0 - r
    #y = y0 - r
    #w = 2 * r
    #h = 2 * r
    #start = int(180 / math.pi * math.atan2(y1-y0, x1-x0))
    #end   = int(180 / math.pi * math.atan2(y2-y0, x2-x0))

    #cx, cy = Globals.canvas.WorldToClient( (x, y) )
    #cw, ch = Globals.canvas.WorldToClient( (w, h) )

    #ix, iy = int(cx), int(cy)
    #iw = int(cw)
    #ih = int(ch)

    #dc.DrawEllipticArc(ix, iy, iw, ih, start, end)

    pts = np.array([
      [ cx1, cy1 ],
      [ cx2, cy2 ]
      ]).astype('intc')
    dc.DrawLinesFromBuffer(pts)

    self.__DrawEdgeLabel(dc, e)

  def __DrawEdgeLabel(self, dc, e):
    pass

  def DrawAllNodes(self, dc):
    nodes = Globals.G.nodes()
    dc.SetPen(wx.BLACK_PEN)
    for v in nodes:
      self.__DrawNode(dc, v)

  def __DrawNode(self, dc, v):
    if v in Globals.canvas.selected_nodes:
      node_brush = wx.Brush(Globals.canvas.graph_colors[0], wx.SOLID)
    else:
      node_brush = wx.Brush(Globals.canvas.graph_colors[Globals.G.vcolor[v]], wx.SOLID)
    dc.SetBrush(node_brush)
    pos = Globals.canvas.WorldToClient(Globals.G.vpos[v])
    dc.DrawCircle(pos[0].astype('intc'), pos[1].astype('intc'), Globals.canvas.node_radius)
    self.__DrawNodeLabel(dc, v)

  def __DrawNodeLabel(self, dc, v):
    pos = Globals.canvas.WorldToClient(Globals.G.vpos[v])
    pos = np.array([
      pos[0] - Globals.canvas.node_radius - 15, pos[1] - Globals.canvas.node_radius - 15
      ]).astype('intc')
    dc.DrawText(Globals.G.vlabel[v], pos[0], pos[1])

