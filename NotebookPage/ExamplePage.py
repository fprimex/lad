import wx
from Globals import *

class ExamplePage(wx.Panel):
  def __init__(self, parent, id=-1):
    wx.Panel.__init__(self, parent, -1)

    ctrl = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
    page_sizer = wx.BoxSizer(wx.VERTICAL)
    page_sizer.Add(ctrl, 1, wx.EXPAND, 0)
    self.SetSizer(page_sizer)
