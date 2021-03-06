# -*- coding: utf-8 -*-
# generated by wxGlade 0.6 on Sun Dec 16 16:40:31 2007

import wx
import Globals

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class ExportAsImageDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        self.choices=["JPEG (*.jpg)", "PNG (*.png)", "Bitmap (*.bmp)", "XPM (*.xpm)", "PCX (*.pcx)", "PNM (*.pnm)"]
        # begin wxGlade: ExportAsImageDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.width_label = wx.StaticText(self, -1, "Width:")
        self.width_ctrl = wx.TextCtrl(self, -1, "")
        self.height_label = wx.StaticText(self, -1, "Height:")
        self.height_ctrl = wx.TextCtrl(self, -1, "")
        self.type_label = wx.StaticText(self, -1, "Type:")
        self.type_ctrl = wx.Choice(self, -1, choices=self.choices)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ExportAsImageDlg.__set_properties
        self.SetTitle("Export graph as image...")
        # end wxGlade
        client_size = Globals.canvas.GetClientSize()
        self.width_ctrl.SetValue(repr(client_size[0]))
        self.height_ctrl.SetValue(repr(client_size[1]))
        self.type_ctrl.SetSelection(0)

    def __do_layout(self):
        self.buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        # begin wxGlade: ExportAsImageDlg.__do_layout
        dlg_sizer = wx.BoxSizer(wx.VERTICAL)
        dlg_grid_sizer = wx.GridSizer(3, 2, 0, 0)
        type_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        type_sizer2 = wx.BoxSizer(wx.VERTICAL)
        height_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        height_sizer2 = wx.BoxSizer(wx.VERTICAL)
        width_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        width_sizer2 = wx.BoxSizer(wx.VERTICAL)
        dlg_grid_sizer.Add(self.width_label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        width_sizer2.Add(self.width_ctrl, 0, wx.EXPAND, 0)
        width_sizer1.Add(width_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        dlg_grid_sizer.Add(width_sizer1, 1, wx.EXPAND, 0)
        dlg_grid_sizer.Add(self.height_label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        height_sizer2.Add(self.height_ctrl, 0, wx.EXPAND, 0)
        height_sizer1.Add(height_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        dlg_grid_sizer.Add(height_sizer1, 1, wx.EXPAND, 0)
        dlg_grid_sizer.Add(self.type_label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        type_sizer2.Add(self.type_ctrl, 1, wx.EXPAND, 0)
        type_sizer1.Add(type_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        dlg_grid_sizer.Add(type_sizer1, 1, wx.EXPAND, 0)
        dlg_sizer.Add(dlg_grid_sizer, 1, wx.EXPAND, 0)
        dlg_sizer.Add((20, 20), 0, 0, 0)
        self.SetSizer(dlg_sizer)
        dlg_sizer.Fit(self)
        self.Layout()
        # end wxGlade
        if self.buttons != None:
            dlg_sizer.Add(self.buttons, 0, wx.EXPAND, 0)
        dlg_sizer.Fit(self)
        self.Layout()

# end of class ExportAsImageDlg


