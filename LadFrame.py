# -*- coding: utf-8 -*-
# generated by wxGlade 0.6 on Fri Nov  2 11:04:27 2007

import sys
import os
import wx
import wx.py as py
import pickle
import GraphCanvas

# begin wxGlade: dependencies
# end wxGlade

LAD_EXPORT = wx.NewId()
LAD_EDIT_AXES = wx.NewId()
LAD_REFRESH = wx.NewId()
LAD_M_MODE_SEL = wx.NewId()
LAD_M_MODE_VER = wx.NewId()
LAD_M_MODE_LOCK = wx.NewId()
LAD_ADD_EDGES = wx.NewId()
LAD_ADD_PATH = wx.NewId()
LAD_EDIT_SEL = wx.NewId()
LAD_DEL_SEL = wx.NewId()
LAD_WEBSITE = wx.NewId()

class LadFrame(wx.Frame):
  lad_file = ""
  lad_full_file = ""

  def __init__(self, *args, **kwds):
    # begin wxGlade: LadFrame.__init__
    kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
    wx.Frame.__init__(self, *args, **kwds)
    self.SetSize((800, 600))
    self.SetTitle("LAD Graph Theory")

    # Menu Bar
    self.main_window_menubar = wx.MenuBar()
    wxglade_tmp_menu = wx.Menu()
    wxglade_tmp_menu.Append(wx.ID_NEW, "New\tCtrl-N", "Launch another LAD")
    self.Bind(wx.EVT_MENU, self.OnNew, id=wx.ID_NEW)
    wxglade_tmp_menu.Append(wx.ID_OPEN, "Open\tCtrl-O", "Open a previously saved graph")
    self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
    wxglade_tmp_menu.AppendSeparator()
    wxglade_tmp_menu.Append(wx.ID_SAVE, "Save\tCtrl-S", "Save graph to a file")
    self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
    wxglade_tmp_menu.Append(wx.ID_SAVEAS, "Save As...", "Save graph to a specified file name")
    self.Bind(wx.EVT_MENU, self.OnSaveAs, id=wx.ID_SAVEAS)
    wxglade_tmp_menu.Append(LAD_EXPORT, "Export As Image...", "Export graph image to a number of formats")
    self.Bind(wx.EVT_MENU, self.OnExport, id=LAD_EXPORT)
    wxglade_tmp_menu.AppendSeparator()
    wxglade_tmp_menu.Append(wx.ID_EXIT, "Quit\tCtrl-Q", "Quit LAD")
    self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
    self.main_window_menubar.Append(wxglade_tmp_menu, "&File")
    wxglade_tmp_menu = wx.Menu()
    wxglade_tmp_menu.Append(LAD_REFRESH, "Refresh\tCtrl-R", "Refresh the graph canvas")
    self.Bind(wx.EVT_MENU, self.OnRefresh, id=LAD_REFRESH)
    wxglade_tmp_menu.Append(LAD_EDIT_AXES, "Edit Axis", "Adjust canvas mins, maxes, and scales")
    self.Bind(wx.EVT_MENU, self.OnEditAxes, id=LAD_EDIT_AXES)
    self.main_window_menubar.Append(wxglade_tmp_menu, "&View")
    wxglade_tmp_menu = wx.Menu()
    wxglade_tmp_menu.Append(LAD_M_MODE_VER, "Creation", "Click the graph canvas to create vertices and drag elements", wx.ITEM_RADIO)
    self.Bind(wx.EVT_MENU, self.OnMouseModeVer, id=LAD_M_MODE_VER)
    wxglade_tmp_menu.Append(LAD_M_MODE_SEL, "Selection", "Allow element dragging, but don't allow vertex creation", wx.ITEM_RADIO)
    self.Bind(wx.EVT_MENU, self.OnMouseModeSel, id=LAD_M_MODE_SEL)
    wxglade_tmp_menu.Append(LAD_M_MODE_LOCK, "Lock", "Don't allow element dragging or vertex creation", wx.ITEM_RADIO)
    self.Bind(wx.EVT_MENU, self.OnMouseModeLock, id=LAD_M_MODE_LOCK)
    self.main_window_menubar.Append(wxglade_tmp_menu, "&Mouse Mode")
    wxglade_tmp_menu = wx.Menu()
    wxglade_tmp_menu.Append(LAD_ADD_EDGES, "Add Complete Edge(s)\tCtrl-E", "Create an edge between all selected vertices")
    self.Bind(wx.EVT_MENU, self.OnAddEdges, id=LAD_ADD_EDGES)
    wxglade_tmp_menu.Append(LAD_ADD_PATH, "Add Path Edge(s)\tCtrl-P", "Create a path in the order vertices were selected")
    self.Bind(wx.EVT_MENU, self.OnAddPath, id=LAD_ADD_PATH)
    wxglade_tmp_menu.AppendSeparator()
    wxglade_tmp_menu.Append(wx.ID_SELECTALL, "Select All\tCtrl-A", "Select all vertices and edges in the graph")
    self.Bind(wx.EVT_MENU, self.OnSelectAll, id=wx.ID_SELECTALL)
    wxglade_tmp_menu.Append(LAD_EDIT_SEL, "Edit Selected Vertices", "Edit the properties of the selected vertices")
    self.Bind(wx.EVT_MENU, self.OnEditSelection, id=LAD_EDIT_SEL)
    wxglade_tmp_menu.AppendSeparator()
    wxglade_tmp_menu.Append(LAD_DEL_SEL, "Delete Selection\tCtrl-BACK", "Delete selected vertices and edges")
    self.Bind(wx.EVT_MENU, self.OnDeleteSelection, id=LAD_DEL_SEL)
    self.main_window_menubar.Append(wxglade_tmp_menu, "&Graph")
    wxglade_tmp_menu = wx.Menu()
    wxglade_tmp_menu.Append(wx.ID_ABOUT, "About", "About LAD")
    self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
    wxglade_tmp_menu.Append(LAD_WEBSITE, "Website", "")
    self.Bind(wx.EVT_MENU, self.OnWebsite, id=LAD_WEBSITE)
    self.main_window_menubar.Append(wxglade_tmp_menu, "&Help")
    self.SetMenuBar(self.main_window_menubar)
    # Menu Bar end

    self.main_window_statusbar = self.CreateStatusBar(1)
    self.main_window_statusbar.SetStatusWidths([-1])
    # statusbar fields
    main_window_statusbar_fields = ["Welcome to LAD Graph Theory"]
    for i in range(len(main_window_statusbar_fields)):
      self.main_window_statusbar.SetStatusText(main_window_statusbar_fields[i], i)

    main_sizer = wx.BoxSizer(wx.VERTICAL)

    self.horiz_splitter = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3D | wx.SP_BORDER)
    self.horiz_splitter.SetMinimumPaneSize(20)
    main_sizer.Add(self.horiz_splitter, 1, wx.EXPAND, 0)

    self.top_pane = wx.Panel(self.horiz_splitter, wx.ID_ANY)

    top_pane_sizer = wx.BoxSizer(wx.VERTICAL)

    self.vert_splitter = wx.SplitterWindow(self.top_pane, wx.ID_ANY, style=wx.SP_3D | wx.SP_BORDER)
    self.vert_splitter.SetMinimumPaneSize(20)
    top_pane_sizer.Add(self.vert_splitter, 1, wx.EXPAND, 0)

    self.left_pane = wx.Panel(self.vert_splitter, wx.ID_ANY)

    left_pane_sizer = wx.BoxSizer(wx.VERTICAL)

    self.canvas = GraphCanvas.GraphCanvas(self.left_pane, wx.ID_ANY, self)
    left_pane_sizer.Add(self.canvas, 1, wx.EXPAND, 0)

    self.right_pane = wx.Panel(self.vert_splitter, wx.ID_ANY)

    sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

    self.notebook = wx.Notebook(self.right_pane, wx.ID_ANY)
    sizer_2.Add(self.notebook, 1, wx.EXPAND, 0)

    self.bottom_pane = wx.Panel(self.horiz_splitter, wx.ID_ANY)

    bottom_pane_sizer = wx.BoxSizer(wx.VERTICAL)

    self.shell = py.shell.Shell(self.bottom_pane, wx.ID_ANY)
    bottom_pane_sizer.Add(self.shell, 1, wx.EXPAND, 0)

    self.bottom_pane.SetSizer(bottom_pane_sizer)

    self.right_pane.SetSizer(sizer_2)

    self.left_pane.SetSizer(left_pane_sizer)

    self.vert_splitter.SplitVertically(self.left_pane, self.right_pane)

    self.top_pane.SetSizer(top_pane_sizer)

    self.horiz_splitter.SplitHorizontally(self.top_pane, self.bottom_pane)

    self.SetSizer(main_sizer)

    self.Layout()

    # end wxGlade

    self.horiz_splitter.SetSashGravity(1.0)
    self.vert_splitter.SetSashGravity(1.0)

    self.horiz_splitter.SetSashPosition(400)
    self.vert_splitter.SetSashPosition(600)

  def InitNotebook(self):
    import NotebookPage
    info_page = NotebookPage.InfoPage(self.notebook)
    vars_page = NotebookPage.VarsPage(self.notebook)

    self.notebook.AddPage(info_page, "Info")
    self.notebook.AddPage(vars_page, "G.vars['var']=val")

  def ReinitNotebook(self):
    for i in range(self.notebook.GetPageCount()):
      page = self.notebook.GetPage(i)
      if hasattr(page, "Reinit"):
        page.Reinit()

  def InitShell(self):
    self.shell.push("import Globals", silent=True)
    self.ReinitShell()
    self.shell.push("""print(\"\"\"
    Imported Packages
    -----------------
    nx  NetworkX package
    wx  wxPython package

    Initialized Variables
    ---------------------
    G        NetworkX graph object
    canvas   Graph drawing area (wx.ScrolledWindow)
    notebook Tabbed window (wx.Notebook)
    shell    This shell panel (wx.py.shell.Shell)
    \"\"\")
    """)

    #local variables dir() = ' + repr(dir()))")

  def ReinitShell(self):
    self.shell.push("import nx", silent=True)
    self.shell.push("G = Globals.G", silent=True)
    self.shell.push("canvas = Globals.canvas", silent=True)
    self.shell.push("notebook = Globals.notebook", silent=True)
    self.shell.push("shell = Globals.shell", silent=True)

  def OnQuit(self, event): # wxGlade: LadFrame.<event_handler>
    self.Close(True)

  def OnNew(self, event): # wxGlade: LadFrame.<event_handler>
    wx.Execute("python " + os.path.abspath(sys.argv[0]))

  def OnOpen(self, event): # wxGlade: LadFrame.<event_handler>
    import Globals
    dlg = wx.MessageDialog(self, "Open a graph?\nChanges to current graph since last save will be lost.", "Open", wx.OK | wx.CANCEL)
    dlg.CenterOnParent()

    if dlg.ShowModal() == wx.ID_OK:
      open_dlg = wx.FileDialog(self, "Open file...", "", "", "LAD files (*.lad)|*.lad", wx.OPEN|wx.FILE_MUST_EXIST)
      if open_dlg.ShowModal() == wx.ID_OK:
        graph_filename = open_dlg.GetFilename()
        graph_full_filename = open_dlg.GetPath()
        file = open(graph_full_filename, 'r')
        Globals.G = pickle.load(file)
        file.close()
        self.ReinitNotebook()
        self.ReinitShell()
        self.canvas.Refresh()
     
  def OnSave(self, event): # wxGlade: LadFrame.<event_handler>
    import Globals
    if self.lad_file != "" and lad_full_file != "":
      try:
        f = open(lad_full_file, 'w')
        pickle.dump(Globals.G)
        f.close()
      except:
        dlg = wx.MessageDialog(self, "Error saving file\nThe graph was not saved. Try Save as...", "Error", wx.OK)
        dlg.CenterOnParent();
        dlg.ShowModal()
    else:
      self.OnSaveAs(event)

  def OnSaveAs(self, event): # wxGlade: LadFrame.<event_handler>
    import Globals
    ext = ".lad"
    save_dlg = wx.FileDialog(self, "Save graph...", "", "", "LAD files (*.lad)|*.lad", wx.SAVE|wx.OVERWRITE_PROMPT)
    if save_dlg.ShowModal() == wx.ID_OK:
      graph_filename = save_dlg.GetFilename()
      graph_full_filename = save_dlg.GetPath()
      if graph_filename[len(graph_filename)-4:] != ext:
        graph_filename += ext 
        graph_full_filename += ext
      try:
        file = open(graph_full_filename, 'w')
        pickle.dump(Globals.G, file)
        file.close()
        self.lad_file = graph_filename
        self.lad_full_file = graph_full_filename
        #SetWindowTitle(graphFilename);
      except:
        dlg = wx.MessageDialog(self, "Error saving file\nThe graph was not saved. Try another file location or name.", "Error", wx.OK)
        dlg.CenterOnParent();
        dlg.ShowModal()

  def OnExport(self, event): # wxGlade: LadFrame.<event_handler>
    import ExportAsImageDlg
    # File types supported:
    # Dialog filter index
    # -------------------
    #     0      wx.BITMAP_TYPE_JPEG
    #     1      wx.BITMAP_TYPE_PNG
    #     2      wx.BITMAP_TYPE_BMP
    #     3      wx.BITMAP_TYPE_XPM
    #     4      wx.BITMAP_TYPE_PCX (tries 8-bit, 24-bit otherwise).
    #     5      wx.BITMAP_TYPE_PNM (as raw RGB always).
    # 
    # In wxImage but not supported:
    # wx.BITMAP_TYPE_ICO   Windows Icon File - graphs are too big
    # wx.BITMAP_TYPE_CUR   Windows cursor file - graphs are too big
    # wx.BITMAP_TYPE_TIFF  UNISYS legal issues
    types = {0:wx.BITMAP_TYPE_JPEG, 1:wx.BITMAP_TYPE_PNG, 2:wx.BITMAP_TYPE_BMP, 3:wx.BITMAP_TYPE_XPM, 4:wx.BITMAP_TYPE_PCX, 5:wx.BITMAP_TYPE_PNM}
    dlg = ExportAsImageDlg.ExportAsImageDlg(self)
    dlg.CenterOnParent()
    if dlg.ShowModal() == wx.ID_OK:
      try:
        width = int(dlg.width_ctrl.GetValue())
      except:
        dlg = wx.MessageDialog(self, "Error converting width value.", "Error", wx.OK)
        dlg.CenterOnParent();
        dlg.ShowModal()
        return

      try:
        height = int(dlg.height_ctrl.GetValue())
      except:
        dlg = wx.MessageDialog(self, "Error converting height value.", "Error", wx.OK)
        dlg.CenterOnParent();
        dlg.ShowModal()
        return

      type = dlg.type_ctrl.GetSelection()
      type_str = dlg.choices[type]
      type_ext = type_str[type_str.find('.'):type_str.find(')')]
      type_str = type_str + "|*" + type_ext
      
      save_dlg = wx.FileDialog(self, "Save image...", "", "", type_str, wx.SAVE|wx.OVERWRITE_PROMPT)
      if save_dlg.ShowModal() == wx.ID_OK:
        export_bitmap = wx.EmptyBitmap(width, height)
        self.canvas.DrawBitmap(export_bitmap)
        export_image = export_bitmap.ConvertToImage()
        image_full_filename = save_dlg.GetPath()
        if image_full_filename[len(image_full_filename)-4:] != type_ext:
          print(image_full_filename)
          print(image_full_filename[4:])
          print(type_ext)
          image_full_filename += type_ext
        try:
          export_image.SaveFile(image_full_filename, types[type])
        except:
          dlg = wx.MessageDialog(self, "Error saving image\nThe image was not saved. Try another file location or name.", "Error", wx.OK)
          dlg.CenterOnParent();
          dlg.ShowModal()

  def OnEditAxes(self, event): # wxGlade: LadFrame.<event_handler>
    import EditAxesDlg
    keep_trying = True
    while keep_trying:
      dlg = EditAxesDlg.EditAxesDlg(self)
      dlg.CenterOnParent()
      clicked_ok = dlg.ShowModal() == wx.ID_OK
      if clicked_ok:
        try:
          x_min = float(dlg.x_min_ctrl.GetValue())
          x_max = float(dlg.x_max_ctrl.GetValue())
          x_scale = float(dlg.x_scale_ctrl.GetValue())
          y_min = float(dlg.y_min_ctrl.GetValue())
          y_max = float(dlg.y_max_ctrl.GetValue())
          y_scale = float(dlg.y_scale_ctrl.GetValue())
          self.canvas.x_min = x_min
          self.canvas.x_max = x_max
          self.canvas.x_scale = x_scale
          self.canvas.y_min = y_min
          self.canvas.y_max = y_max
          self.canvas.y_scale = y_scale
          self.canvas.Refresh()
          keep_trying = False
        except:
          dlg = wx.MessageDialog(self, "Error setting axes.\nThere was a problem converting the values provided.", "Error", wx.OK)
          dlg.CenterOnParent();
          dlg.ShowModal()
      else:
        keep_trying = False

  def OnAddEdges(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.CreateEdgesFromSelection()

  def OnDeleteSelection(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.DeleteSelected()

  def OnMouseModeSel(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.mouse_mode = self.canvas.MOUSE_MODE_SELECTION

  def OnMouseModeVer(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.mouse_mode = self.canvas.MOUSE_MODE_VERTEX

  def OnMouseModeLock(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.mouse_mode = self.canvas.MOUSE_MODE_LOCK

  def OnAddPath(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.CreatePathFromSelection()

  def OnSelectAll(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.SelectAll()

  def OnEditSelection(self, event): # wxGlade: LadFrame.<event_handler>
    import EditSelectionDlg
    dlg = EditSelectionDlg.EditSelectionDlg(self)
    dlg.Show()
    self.canvas.Refresh()

  def OnRefresh(self, event): # wxGlade: LadFrame.<event_handler>
    self.canvas.Refresh()

  def OnAbout(self, event): # wxGlade: LadFrame.<event_handler>
    msg = """LAD - Lines and Dots
Copyright Brent W. Woodruff
Licensed under the GNU GPL"""
    dlg = wx.MessageDialog(self, msg, "About LAD", wx.OK)
    dlg.ShowModal()

  def OnWebsite(self, event): # wxGlade: LadFrame.<event_handler>
    wx.LaunchDefaultBrowser("http://www.fprimex.com/programming/lad")

# end of class LadFrame


