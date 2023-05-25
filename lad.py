import wx
import networkx as nx
from gui import LadFrame

class Lad(wx.App):
  def OnInit(self):
    self.main_window = LadFrame(None, -1, "")

    self.canvas = self.main_window.canvas
    self.notebook = self.main_window.notebook
    self.shell = self.main_window.shell

    self.SetTopWindow(self.main_window)
    return 1

# end of class Lad

if __name__ == "__main__":
  lad = Lad(0)
  lad.main_window.InitNotebook()
  lad.main_window.InitShell()
  lad.TopWindow.Show()
  lad.MainLoop()
