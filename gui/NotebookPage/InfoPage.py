import wx
from ..ListEditorCtrl import ListEditorCtrl

class InfoPage(wx.Panel):
  def __init__(self, parent, id=-1):
    wx.Panel.__init__(self, parent, -1)
    v_cols = [u"Vertex v", u"Value"]
    e_cols = [u"Edge e", u"v", u"app.canvas.vlabel[v]"]
    self.v_col0_labels = ["v", "app.canvas.vlabel[v]", "app.canvas.vpos[v][0]", "app.canvas.vpos[v][1]", "app.canvas.vweight[v]", "app.canvas.vcolor[v]"]
    self.e_col0_labels = ["e[0]     ", "e[1]     "]
    v_listdata = {}
    e_listdata = {}
    for i in range(len(self.v_col0_labels)):
      v_listdata[i] = (self.v_col0_labels[i], "")
    for i in range(len(self.e_col0_labels)):
      e_listdata[i] = (self.e_col0_labels[i], "")

    v_info_ctrl = VertexInfoCtrl(self, -1, v_cols, v_listdata, style=wx.LC_REPORT | wx.BORDER_NONE)
    e_info_ctrl = EdgeInfoCtrl(self, -1, e_cols, e_listdata, style=wx.LC_REPORT | wx.BORDER_NONE)
    page_sizer = wx.BoxSizer(wx.VERTICAL)
    page_sizer.Add(v_info_ctrl, 1, wx.EXPAND, 0)
    page_sizer.Add(e_info_ctrl, 1, wx.EXPAND, 0)
    self.SetSizer(page_sizer)


    app = wx.GetApp()
    app.canvas.on_node_create_funcs.append(v_info_ctrl.RefreshList)
    app.canvas.on_edge_create_funcs.append(v_info_ctrl.RefreshList)
    app.canvas.on_node_delete_funcs.append(v_info_ctrl.RefreshList)
    app.canvas.on_edge_delete_funcs.append(v_info_ctrl.RefreshList)
    app.canvas.on_node_select_funcs.append(v_info_ctrl.RefreshList)
    app.canvas.on_edge_select_funcs.append(v_info_ctrl.RefreshList)
    app.canvas.on_drag_end_funcs.append(v_info_ctrl.RefreshList)

    app.canvas.on_node_create_funcs.append(e_info_ctrl.RefreshList)
    app.canvas.on_edge_create_funcs.append(e_info_ctrl.RefreshList)
    app.canvas.on_node_delete_funcs.append(e_info_ctrl.RefreshList)
    app.canvas.on_edge_delete_funcs.append(e_info_ctrl.RefreshList)
    app.canvas.on_node_select_funcs.append(e_info_ctrl.RefreshList)
    app.canvas.on_edge_select_funcs.append(e_info_ctrl.RefreshList)
    app.canvas.on_drag_end_funcs.append(e_info_ctrl.RefreshList)

class VertexInfoCtrl(ListEditorCtrl):
  def __init__(self, parent, ID, headings, listdata, pos=wx.DefaultPosition,
         size=wx.DefaultSize, style=0):
    ListEditorCtrl.__init__(self, parent, ID, headings, listdata, pos, size, style)
    self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnOpenEditor)

    # Remove separator, Insert, and Delete entries from submenu
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))

  def GetRowValues(self, row):
    app = wx.GetApp()
    G = app.canvas.G
    num = len(app.canvas.selected_nodes)
    if num == 0:
      data = (self.GetParent().v_col0_labels[row], "")
      self.listctrldata[row] = data
      return data
    else:
      try:
        v = app.canvas.selected_nodes[num-1]
        value = eval(self.GetParent().v_col0_labels[row])
        if row == 1:
          data = (self.GetParent().v_col0_labels[row], value)
        else:
          data = (self.GetParent().v_col0_labels[row], repr(value))
        self.listctrldata[row] = (self.GetParent().v_col0_labels[row], value)
        return data
      except KeyError:
        data = (self.GetParent().v_col0_labels[row], "")
        self.listctrldata[row] = data
        return data
    
  def SetValue(self, row, col, text):
    # Could attempt to do this in a more clever way using exec
    # as below, but risk introducing things into global()
    # G = app.G
    #v = row
    #assignment = self.GetParent().v_col0_labels[row] + " = " + text
    #exec(assignment, globals(), globals())

    app = wx.GetApp()
    v = self.listctrldata[0][1]
    if row == 1:
      app.vlabel[v] = text
    elif row == 2:
      try:
        x = float(text)
        app.vpos[v][0] = x
      except:
        pass
    elif row == 3:
      try:
        y = float(text)
        app.vpos[v][1] = y
      except:
        pass
    elif row == 4:
      try:
        w = float(text)
        app.vweight[v] = w
      except:
        pass
    elif row == 5:
      try:
        c = int(text)
        if 0 <= c < len(app.canvas.graph_colors):
          app.vcolor[v] = c
      except:
        pass

    self.listctrldata[row] = (self.GetParent().v_col0_labels[row][0], text)
    app.canvas.Refresh()

  def OnOpenEditor(self, event):
    if event.m_col == 0 or event.m_itemIndex == 0:
      event.Veto()
    
class EdgeInfoCtrl(ListEditorCtrl):
  def __init__(self, parent, ID, headings, listdata, pos=wx.DefaultPosition,
         size=wx.DefaultSize, style=0):
    ListEditorCtrl.__init__(self, parent, ID, headings, listdata, pos, size, style)
    self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnOpenEditor)

    # Remove separator, Insert, and Delete entries from submenu
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))

  def GetRowValues(self, row):
    app = wx.GetApp()
    num = len(app.canvas.selected_edges)
    if num == 0:
      data = (self.GetParent().e_col0_labels[row], "   ", "   ")
      self.listctrldata[row] = data
      return data
    else:
      e = app.canvas.selected_edges[num-1]
      if row == 1:
        v = e[0]
      else:
        v = e[1]
      vlabel = app.canvas.vlabel[v]
      self.listctrldata[row] = (self.GetParent().e_col0_labels[row], v, vlabel)
      return (self.GetParent().e_col0_labels[row], repr(v), vlabel)
    
  def OnOpenEditor(self, event):
    app = wx.GetApp()
    app.canvas.SelectVertex(self.listctrldata[event.m_itemIndex][1])
    app.canvas.Refresh()
    event.Veto()
    
