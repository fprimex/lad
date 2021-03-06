# -*- coding: utf-8 -*-
# generated by wxGlade 0.6 on Sun Dec 16 19:08:35 2007

import wx
import Globals

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class EditAxesDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: EditAxesDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.x_min_label = wx.StaticText(self, -1, "x min:")
        self.x_min_ctrl = wx.TextCtrl(self, -1, "")
        self.x_max_label = wx.StaticText(self, -1, "x max:")
        self.x_max_ctrl = wx.TextCtrl(self, -1, "")
        self.x_scale_label = wx.StaticText(self, -1, "x scale:")
        self.x_scale_ctrl = wx.TextCtrl(self, -1, "")
        self.y_min_label = wx.StaticText(self, -1, "y min:")
        self.y_min_ctrl = wx.TextCtrl(self, -1, "")
        self.y_max_label = wx.StaticText(self, -1, "y max:")
        self.y_max_ctrl = wx.TextCtrl(self, -1, "")
        self.y_scale_label = wx.StaticText(self, -1, "y scale:")
        self.y_scale_ctrl = wx.TextCtrl(self, -1, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: EditAxesDlg.__set_properties
        self.SetTitle("Edit Axes")
        # end wxGlade
        canvas = Globals.canvas
        self.x_min_ctrl.SetValue(repr(canvas.x_min))
        self.x_max_ctrl.SetValue(repr(canvas.x_max))
        self.x_scale_ctrl.SetValue(repr(canvas.x_scale))
        self.y_min_ctrl.SetValue(repr(canvas.y_min))
        self.y_max_ctrl.SetValue(repr(canvas.y_max))
        self.y_scale_ctrl.SetValue(repr(canvas.y_scale))

    def __do_layout(self):
        self.buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        # begin wxGlade: EditAxesDlg.__do_layout
        axes_sizer = wx.BoxSizer(wx.VERTICAL)
        axes_grid_sizer = wx.GridSizer(2, 6, 0, 0)
        y_scale_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        y_scale_sizer2 = wx.BoxSizer(wx.VERTICAL)
        y_max_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        y_max_sizer2 = wx.BoxSizer(wx.VERTICAL)
        y_min_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        y_min_sizer2 = wx.BoxSizer(wx.VERTICAL)
        x_scale_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        x_scale_sizer2 = wx.BoxSizer(wx.VERTICAL)
        x_max_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        x_max_sizer2 = wx.BoxSizer(wx.VERTICAL)
        x_min_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        x_min_sizer2 = wx.BoxSizer(wx.VERTICAL)
        axes_grid_sizer.Add(self.x_min_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        x_min_sizer2.Add(self.x_min_ctrl, 0, wx.EXPAND, 0)
        x_min_sizer1.Add(x_min_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        axes_grid_sizer.Add(x_min_sizer1, 1, wx.EXPAND, 0)
        axes_grid_sizer.Add(self.x_max_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        x_max_sizer2.Add(self.x_max_ctrl, 0, wx.EXPAND, 0)
        x_max_sizer1.Add(x_max_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        axes_grid_sizer.Add(x_max_sizer1, 1, wx.EXPAND, 0)
        axes_grid_sizer.Add(self.x_scale_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        x_scale_sizer2.Add(self.x_scale_ctrl, 0, wx.EXPAND, 0)
        x_scale_sizer1.Add(x_scale_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        axes_grid_sizer.Add(x_scale_sizer1, 1, wx.EXPAND, 0)
        axes_grid_sizer.Add(self.y_min_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        y_min_sizer2.Add(self.y_min_ctrl, 0, wx.EXPAND, 0)
        y_min_sizer1.Add(y_min_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        axes_grid_sizer.Add(y_min_sizer1, 1, wx.EXPAND, 0)
        axes_grid_sizer.Add(self.y_max_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        y_max_sizer2.Add(self.y_max_ctrl, 0, wx.EXPAND, 0)
        y_max_sizer1.Add(y_max_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        axes_grid_sizer.Add(y_max_sizer1, 1, wx.EXPAND, 0)
        axes_grid_sizer.Add(self.y_scale_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        y_scale_sizer2.Add(self.y_scale_ctrl, 0, wx.EXPAND, 0)
        y_scale_sizer1.Add(y_scale_sizer2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        axes_grid_sizer.Add(y_scale_sizer1, 1, wx.EXPAND, 0)
        axes_sizer.Add(axes_grid_sizer, 1, wx.EXPAND, 0)
        axes_sizer.Add((20, 20), 0, 0, 0)
        self.SetSizer(axes_sizer)
        axes_sizer.Fit(self)
        self.Layout()
        # end wxGlade
        if self.buttons != None:
            axes_sizer.Add(self.buttons, 0, wx.EXPAND, 0)
        axes_sizer.Fit(self)
        self.Layout()

# end of class EditAxesDlg


