import wx
import networkx as NX

G = NX.Graph()
G.vlabel = {}
G.vpos = {}
G.vweight = {}
G.vcolor = {}
G.var_exps = {u"order": u"G.order()", u"size": u"G.size()"}
G.vars = {u"order": 0, u"size": 0}
canvas = wx.GetApp().TopWindow.canvas
notebook = wx.GetApp().TopWindow.notebook
shell = wx.GetApp().TopWindow.shell
