import wx
import Globals
from ListEditorCtrl import ListEditorCtrl

class VarsPage(wx.Panel):
  def __init__(self, parent, id=-1):
    wx.Panel.__init__(self, parent, -1)
    cols = [u"var", u"val / exp"]
    listdata = {}
    i = 0
    for var in Globals.G.vars.keys():
      listdata[i] = (var, Globals.G.var_exps[var])
      i += 1
    self.vars_ctrl = ExpListCtrl(self, -1, cols, listdata, style=wx.LC_REPORT | wx.BORDER_NONE)
    page_sizer = wx.BoxSizer(wx.VERTICAL)
    page_sizer.Add(self.vars_ctrl, 1, wx.EXPAND, 0)
    self.SetSizer(page_sizer)

    Globals.canvas.on_node_create_funcs.append(self.vars_ctrl.RefreshList)
    Globals.canvas.on_edge_create_funcs.append(self.vars_ctrl.RefreshList)
    Globals.canvas.on_node_delete_funcs.append(self.vars_ctrl.RefreshList)
    Globals.canvas.on_edge_delete_funcs.append(self.vars_ctrl.RefreshList)
    Globals.canvas.on_drag_end_funcs.append(self.vars_ctrl.RefreshList)

  def Reinit(self):
    listdata = {}
    i = 0
    for var in Globals.G.vars.keys():
      listdata[i] = (var, Globals.G.var_exps[var])
      i += 1
    self.vars_ctrl.listctrldata = listdata
    self.vars_ctrl.RefreshList()
    
    

class ExpListCtrl(ListEditorCtrl):
  def __init__(self, parent, ID, headings, listdata, pos=wx.DefaultPosition,
         size=wx.DefaultSize, style=0):
    ListEditorCtrl.__init__(self, parent, ID, headings, listdata, pos, size, style)

  def GetRowValues(self, row):
    G = Globals.G
    var = self.listctrldata[row][0]
    exp = self.listctrldata[row][1]
    try:
      value = eval(exp)
    except:
      value = u"ERROR"
    Globals.G.var_exps[var] = exp
    Globals.G.vars[var] = value
    return (var, repr(value))

  def GetEditValue(self, row, col):
    if col == 1:
      return self.listctrldata[row][1]
    else:
      return self.GetItem(row, col).GetText()
  
  def SetValue(self, row, col, text):
    # save exp text back into the expression dict
    if col == 0:
      del Globals.G.vars[self.listctrldata[row][0]]
      del Globals.G.var_exps[self.listctrldata[row][0]]
      self.listctrldata[row] = (text, self.listctrldata[row][1])
    else:
      self.listctrldata[row] = (self.listctrldata[row][0], text)

  def PreDelete(self, row):
    var = self.GetItem(row, 0).GetText()
    del Globals.G.vars[var]
    del Globals.G.var_exps[var]

  def PostInsert(self, row):
    var = self.listctrldata[row][0]
    Globals.G.vars[var] = None
    Globals.G.var_exps[var] = None
