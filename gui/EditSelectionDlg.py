# -*- coding: utf-8 -*-
# generated by wxGlade 0.6 on Sun Dec 16 22:24:14 2007

import wx
from .ListEditorCtrl import ListEditorCtrl

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

app = wx.GetApp()

class EditSelectionDlg(wx.Dialog):
  def __init__(self, *args, **kwds):
    cols = [u"v", u"label", u"x", u"y", u"weight", u"color"]
    listdata = {}
    for i in range(len(app.canvas.selected_nodes)):
      v = app.canvas.selected_nodes[i]
      listdata[i] = (repr(v), app.vlabel[v], repr(app.vpos[v][0]), repr(app.vpos[v][1]), repr(app.vweight[v]), repr(app.vcolor[v]))
    # begin wxGlade: EditSelectionDlg.__init__
    kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
    wx.Dialog.__init__(self, *args, **kwds)
    self.SetTitle("Edit Selection")

    dlg_sizer = wx.BoxSizer(wx.VERTICAL)

    self.selection_ctrl = SelectionListCtrl(self, wx.ID_ANY, cols, listdata, style=wx.LC_REPORT|wx.BORDER_NONE)
    self.selection_ctrl.SetMinSize((500, 300))
    dlg_sizer.Add(self.selection_ctrl, 1, wx.EXPAND, 0)

    dlg_sizer.Add((400, 20), 0, 0, 0)

    self.SetSizer(dlg_sizer)
    dlg_sizer.Fit(self)

    self.Layout()
    # end wxGlade

  def __do_layout(self):
    self.button = self.CreateButtonSizer(wx.OK)
    if self.button != None:
      dlg_sizer.Add(self.button, 0, wx.EXPAND, 0)
    dlg_sizer.Fit(self)
    self.Layout()

# end of class EditSelectionDlg

class SelectionListCtrl(ListEditorCtrl):
  def __init__(self, parent, ID, headings, listdata, pos=wx.DefaultPosition,
         size=wx.DefaultSize, style=0):
    ListEditorCtrl.__init__(self, parent, ID, headings, listdata, pos, size, style)
    self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnOpenEditor)

    # Remove separator, Insert, Delete, and Refresh entries from submenu
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))
    self.context_menu.DestroyItem(self.context_menu.FindItemByPosition(1))

  def SetValue(self, row, col, text):
    v = int(self.listctrldata[row][0])
    if col == 1:
      app.vlabel[v] = text
    elif col == 2:
      try:
        x = float(text)
        app.vpos[v][0] = x
      except:
        pass
    elif col == 3:
      try:
        y = float(text)
        app.vpos[v][1] = y
      except:
        pass
    elif col == 4:
      try:
        w = float(text)
        app.vweight[v] = w
      except:
        pass
    elif col == 5:
      try:
        c = int(text)
        app.vcolor[v] = c
      except:
        pass
    ListEditorCtrl.SetValue(self, row, col, text)

  def OnOpenEditor(self, event):
    if event.m_col == 0:
      event.Veto()
