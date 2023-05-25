import wx

from ..ListEditorCtrl import ListEditorCtrl

class VarsPage(wx.Panel):
  def __init__(self, parent, id=-1):
    wx.Panel.__init__(self, parent, -1)
    self.vars = {u"order": 0, u"size": 0}
    self.var_exps = {u"order": u"app.canvas.G.order()", u"size": u"app.canvas.G.size()"}
    cols = [u"var", u"val / exp"]
    listdata = {}
    i = 0
    for var in self.vars.keys():
      listdata[i] = (var, self.var_exps[var])
      i += 1
    self.vars_ctrl = ExpListCtrl(self, -1, cols, listdata, style=wx.LC_REPORT | wx.BORDER_NONE)
    page_sizer = wx.BoxSizer(wx.VERTICAL)
    page_sizer.Add(self.vars_ctrl, 1, wx.EXPAND, 0)
    self.SetSizer(page_sizer)

    app = wx.GetApp()
    app.canvas.on_node_create_funcs.append(self.vars_ctrl.RefreshList)
    app.canvas.on_edge_create_funcs.append(self.vars_ctrl.RefreshList)
    app.canvas.on_node_delete_funcs.append(self.vars_ctrl.RefreshList)
    app.canvas.on_edge_delete_funcs.append(self.vars_ctrl.RefreshList)
    app.canvas.on_drag_end_funcs.append(self.vars_ctrl.RefreshList)

  def Reinit(self):
    listdata = {}
    i = 0
    for var in self.vars.keys():
      listdata[i] = (var, self.var_exps[var])
      i += 1
    self.vars_ctrl.listctrldata = listdata
    self.vars_ctrl.RefreshList()
    
    

class ExpListCtrl(ListEditorCtrl):
  def __init__(self, parent, ID, headings, listdata, pos=wx.DefaultPosition,
         size=wx.DefaultSize, style=0):
    self.parent = parent
    ListEditorCtrl.__init__(self, parent, ID, headings, listdata, pos, size, style)

  def GetRowValues(self, row):
    app = wx.GetApp()
    G = app.canvas.G
    var = self.listctrldata[row][0]
    exp = self.listctrldata[row][1]
    try:
      value = eval(exp)
    except:
      value = u"ERROR"
    self.parent.var_exps[var] = exp
    self.parent.vars[var] = value
    return (var, repr(value))

  def GetEditValue(self, row, col):
    if col == 1:
      return self.listctrldata[row][1]
    else:
      return self.GetItem(row, col).GetText()
  
  def SetValue(self, row, col, text):
    # save exp text back into the expression dict
    if col == 0:
      del self.parent.vars[self.listctrldata[row][0]]
      del self.parent.var_exps[self.listctrldata[row][0]]
      self.listctrldata[row] = (text, self.listctrldata[row][1])
    else:
      self.listctrldata[row] = (self.listctrldata[row][0], text)

  def PreDelete(self, row):
    var = self.GetItem(row, 0).GetText()
    del self.parent.vars[var]
    del self.parent.var_exps[var]

  def PostInsert(self, row):
    var = self.listctrldata[row][0]
    self.parent.vars[var] = None
    self.parent.var_exps[var] = None
