import wx
import Globals
from ListEditorCtrl import ListEditorCtrl

class InfoPage(wx.Panel):
    def __init__(self, parent, id=-1):
        wx.Panel.__init__(self, parent, -1)
        v_cols = [u"Vertex v", u"Value"]
        e_cols = [u"Edge e", u"v", u"G.vlabel[v]"]
        self.v_col0_labels = ["v", "G.vlabel[v]", "G.vpos[v][0]", "G.vpos[v][1]", "G.vweight[v]", "G.vcolor[v]"]
        self.e_col0_labels = ["e[0]         ", "e[1]         "]
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

        Globals.canvas.on_node_create_funcs.append(v_info_ctrl.RefreshList)
        Globals.canvas.on_edge_create_funcs.append(v_info_ctrl.RefreshList)
        Globals.canvas.on_node_delete_funcs.append(v_info_ctrl.RefreshList)
        Globals.canvas.on_edge_delete_funcs.append(v_info_ctrl.RefreshList)
        Globals.canvas.on_node_select_funcs.append(v_info_ctrl.RefreshList)
        Globals.canvas.on_edge_select_funcs.append(v_info_ctrl.RefreshList)
        Globals.canvas.on_drag_end_funcs.append(v_info_ctrl.RefreshList)

        Globals.canvas.on_node_create_funcs.append(e_info_ctrl.RefreshList)
        Globals.canvas.on_edge_create_funcs.append(e_info_ctrl.RefreshList)
        Globals.canvas.on_node_delete_funcs.append(e_info_ctrl.RefreshList)
        Globals.canvas.on_edge_delete_funcs.append(e_info_ctrl.RefreshList)
        Globals.canvas.on_node_select_funcs.append(e_info_ctrl.RefreshList)
        Globals.canvas.on_edge_select_funcs.append(e_info_ctrl.RefreshList)
        Globals.canvas.on_drag_end_funcs.append(e_info_ctrl.RefreshList)

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
        G = Globals.G
        num = len(Globals.canvas.selected_nodes)
        if num == 0:
            data = (self.GetParent().v_col0_labels[row], "")
            self.listctrldata[row] = data
            return data
        else:
            v = Globals.canvas.selected_nodes[num-1]
            value = eval(self.GetParent().v_col0_labels[row])
            if row == 1:
                data = (self.GetParent().v_col0_labels[row], value)
            else:
                data = (self.GetParent().v_col0_labels[row], repr(value))
            self.listctrldata[row] = (self.GetParent().v_col0_labels[row], value)
            return data
        
    def SetValue(self, row, col, text):
        # Could attempt to do this in a more clever way using exec
        # as below, but risk introducing things into global()
        # G = Globals.G
        #v = row
        #assignment = self.GetParent().v_col0_labels[row] + " = " + text
        #exec(assignment, globals(), globals())

        v = self.listctrldata[0][1]
        if row == 1:
            Globals.G.vlabel[v] = text
        elif row == 2:
            try:
                x = float(text)
                Globals.G.vpos[v][0] = x
            except:
                pass
        elif row == 3:
            try:
                y = float(text)
                Globals.G.vpos[v][1] = y
            except:
                pass
        elif row == 4:
            try:
                w = float(text)
                Globals.G.vweight[v] = w
            except:
                pass
        elif row == 5:
            try:
                c = int(text)
                if 0 <= c < len(Globals.canvas.graph_colors):
                    Globals.G.vcolor[v] = c
            except:
                pass

        self.listctrldata[row] = (self.GetParent().v_col0_labels[row][0], text)
        Globals.canvas.Refresh()

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
        num = len(Globals.canvas.selected_edges)
        if num == 0:
            data = (self.GetParent().e_col0_labels[row], "   ", "   ")
            self.listctrldata[row] = data
            return data
        else:
            e = Globals.canvas.selected_edges[num-1]
            if row == 1:
                v = e[0]
            else:
                v = e[1]
            vlabel = Globals.G.vlabel[v]
            self.listctrldata[row] = (self.GetParent().e_col0_labels[row], v, vlabel)
            return (self.GetParent().e_col0_labels[row], repr(v), vlabel)
        
    def OnOpenEditor(self, event):
        Globals.canvas.SelectVertex(self.listctrldata[event.m_itemIndex][1])
        Globals.canvas.Refresh()
        event.Veto()
        
