import math
import wx

try: 
    import Numeric as N 
except: 
    try:
        import numpy as N
    except: 
        raise ImportError,"numpy and/or Numeric can not be imported."     

class GraphCanvas(wx.ScrolledWindow):
    """
    Test Docstring
    """
    selected_nodes = []
    selected_edges = []

    client_size = wx.Size(0, 0)
    node_radius = 5
    node_search_dist = 2
    edge_search_dist = 7

    x_min = y_min = -10.0
    x_max = y_max = 10.0
    x_scale = y_scale = 1.0

    graph_colors = []
    graph_colors.append(wx.RED)
    graph_colors.append(wx.BLACK)
    graph_colors.append(wx.BLUE)
    graph_colors.append(wx.GREEN)
    graph_colors.append(wx.CYAN)
    graph_colors.append(wx.LIGHT_GREY)

    MOUSE_MODE_VERTEX = 0
    MOUSE_MODE_SELECTION = 1
    MOUSE_MODE_LOCK = 2
    mouse_mode = MOUSE_MODE_VERTEX

    __DRAG_NONE = 0
    __DRAG_START = 1
    __DRAG_DRAGGING = 2
    __drag_start_pos = N.array([0.0, 0.0])
    __drag_node = None
    __drag_compensation = N.array([0,0, 0.0])
    __drag_mode = __DRAG_NONE
    __drag_vector = N.array([0.0, 0.0])

    on_node_create_funcs = []
    on_edge_create_funcs = []
    on_node_delete_funcs = []
    on_edge_delete_funcs = []
    on_node_select_funcs = []
    on_edge_select_funcs = []
    on_drag_end_funcs = []

    def __init__(self, parent, id, frame):
        wx.ScrolledWindow.__init__(self, parent, id)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
#        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.__parent = parent
        self.__lad_frame = frame
        self.SetBackgroundColour('WHITE')
        # SetScrollbars(5, 5, 200, 200)

    def __bound_box(self, pos):
        if pos[0] < self.box_x1:
            self.box_x1 = pos[0]
        if pos[0] > self.box_x2:
            self.box_x2 = pos[0]
        if pos[1] < self.box_y1:
            self.box_y1 = pos[1]
        if pos[1] > self.box_y2:
            self.box_y2 = pos[1]

    def __drag(self, pos):
        new_pos = pos + self.__drag_vector
        # scale the drag vector on a collision with the canvas edge
        if new_pos[0] < self.x_min:
            self.__drag_vector = N.array([self.x_min - pos[0], self.__drag_vector[1]])
            new_pos = pos + self.__drag_vector
        if new_pos[0] > self.x_max:
            self.__drag_vector = N.array([self.x_max - pos[0], self.__drag_vector[1]])
            new_pos = pos + self.__drag_vector
        if new_pos[1] < self.y_min:
            self.__drag_vector = N.array([self.__drag_vector[0], self.y_min - pos[1]])
            new_pos = pos + self.__drag_vector
        if new_pos[1] > self.y_max:
            self.__drag_vector = N.array([self.__drag_vector[0], self.y_max - pos[1]])
            new_pos = pos + self.__drag_vector
        return new_pos

    def __execute_callback(self, call_list):
        for func in call_list:
            func()

    def InitArtist(self):
        import GraphArtist
        self.artist = GraphArtist.DefaultArtist()
        self.blank_artist = GraphArtist.BlankArtist()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.PrepareDC(dc)
        myfont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.client_size = self.GetClientSize()
        dc.SetFont(myfont)
        dc.BeginDrawing()
        self.artist.DrawBackground(dc)
        self.artist.DrawAxes(dc)
        self.artist.DrawAllEdges(dc)
        self.artist.DrawAllNodes(dc)
        dc.EndDrawing()

    def OnResize(self, event):
        self.Refresh()

    def DrawBitmap(self, bitmap):
        dc = wx.MemoryDC()
        dc.SelectObject(bitmap)
        myfont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.client_size = bitmap.GetSize()
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        dc.SetFont(myfont)
        self.artist.DrawBackground(dc)
        self.artist.DrawAxes(dc)
        self.artist.DrawAllEdges(dc)
        self.artist.DrawAllNodes(dc)

    def OnMouse(self, event):
        import Globals
        self.client_size = self.GetClientSize()
        mouse_pos = N.array(self.CalcUnscrolledPosition(event.GetX(), event.GetY()))
        world_mouse_pos = N.array(self.ClientToWorld(mouse_pos))
        msg = "(%g, %g)" % (world_mouse_pos[0], world_mouse_pos[1])
        self.__lad_frame.SetStatusText(msg)

        if event.LeftDown():
            # clicked on a vertex?
            u = self.SearchNodes(mouse_pos)
            if u != None:
                if not event.CmdDown():
                    self.DeselectAll()
                if u not in self.selected_nodes:
                    self.SelectVertex(u)
                self.__drag_mode = self.__DRAG_START
                self.__drag_start_pos = world_mouse_pos
                self.__drag_node = u
                self.__drag_compensation = Globals.G.vpos[self.__drag_node] - self.__drag_start_pos
            else:
                # clicked on an edge?
                e = self.SearchEdges(mouse_pos)
                if e != None:
                    if not event.CmdDown():
                        self.DeselectAll()
                    if e not in self.selected_edges:
                        self.SelectEdge(e)
                    self.__drag_mode = self.__DRAG_START
                    self.__drag_start_pos = world_mouse_pos
                    self.__drag_node = e[0]
                    self.__drag_compensation = Globals.G.vpos[self.__drag_node] - world_mouse_pos
                    self.__execute_callback(self.on_edge_select_funcs)
            if u == None and e == None:
                # didn't click on either
                if self.mouse_mode == self.MOUSE_MODE_VERTEX: # creation mode
                    # naming based on order
                    #num = Globals.G.order() + 1
                    #label = "v%i" % num

                    # Fill-in-the-gaps naming scheme
                    v = 0
                    label = "v0"

                    while v in Globals.G.nodes() or label in Globals.G.vlabel.values():
                        v += 1
                        label = "v%i" % v

                    Globals.G.vpos[v] = world_mouse_pos
                    Globals.G.vlabel[v] = label
                    Globals.G.vweight[v] = 1.0
                    Globals.G.vcolor[v] = 1
                    Globals.G.add_node(v)
                    self.__execute_callback(self.on_node_create_funcs)

                    if not event.CmdDown():
                        self.DeselectAll()
                    self.SelectVertex(v)
              
                    self.__drag_mode = self.__DRAG_START
                    self.__drag_start_pos = world_mouse_pos
                    self.__drag_node = v
                    self.__drag_compensation = N.array([0.0, 0.0])
                elif self.mouse_mode == self.MOUSE_MODE_SELECTION or self.mouse_mode == self.MOUSE_MODE_LOCK:
                    self.DeselectAll()
                    self.__drag_mode = self.__DRAG_START
                    self.__drag_start_pos = world_mouse_pos
            self.Refresh()
        elif event.LeftUp(): # && self.__drag_mode != self.__DRAG_NONE)
            self.Refresh()
            self.__drag_mode = self.__DRAG_NONE
            self.__drag_node = None
            self.__execute_callback(self.on_drag_end_funcs)
        elif event.Dragging() and self.__drag_mode != self.__DRAG_NONE:
            if self.__drag_mode == self.__DRAG_START:
                tolerance = 2.0
                dx = math.fabs(mouse_pos[0] - self.__drag_start_pos[0])
                dy = math.fabs(mouse_pos[1] - self.__drag_start_pos[1])
                if dx <= tolerance and dy <= tolerance:
                    return
                self.__drag_mode = self.__DRAG_DRAGGING
            elif self.__drag_mode == self.__DRAG_DRAGGING:
                if self.__drag_node != None and self.mouse_mode != self.MOUSE_MODE_LOCK:
                    self.__drag_vector = world_mouse_pos - Globals.G.vpos[self.__drag_node] + self.__drag_compensation

                    # init the corners of the bounding box
                    self.box_x1 = Globals.G.vpos[self.__drag_node][0]
                    self.box_x2 = Globals.G.vpos[self.__drag_node][0]
                    self.box_y1 = Globals.G.vpos[self.__drag_node][1]
                    self.box_y2 = Globals.G.vpos[self.__drag_node][1]

                    nodes_to_move = set([])
                    for e in self.selected_edges:
                        nodes_to_move.add(e[0])
                        self.__bound_box(Globals.G.vpos[e[0]])
                        nodes_to_move.add(e[1])
                        self.__bound_box(Globals.G.vpos[e[1]])
                    for v in self.selected_nodes:
                        if v not in nodes_to_move:
                            nodes_to_move.add(v)
                            self.__bound_box(Globals.G.vpos[v])

                    # adjust the drag vector to account for canvas edge collisions
                    # by dragging the corners of the bounding box first
                    self.__drag(N.array([self.box_x1, self.box_y1]))
                    self.__drag(N.array([self.box_x1, self.box_y2]))
                    self.__drag(N.array([self.box_x2, self.box_y1]))
                    self.__drag(N.array([self.box_x2, self.box_y2]))

                    # move the vertices
                    for v in nodes_to_move:
                        Globals.G.vpos[v] = self.__drag(Globals.G.vpos[v])

                    self.Refresh()
                elif self.mouse_mode == self.MOUSE_MODE_SELECTION or self.mouse_mode == self.MOUSE_MODE_LOCK:
                    # Not dragging an object and in selection or lock mode
                    # - do selection rectangle
                    dc = wx.BufferedPaintDC(self)
                    self.PrepareDC(dc)
                    myfont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
                    dc.SetFont(myfont)
                    screen_drag_pos = self.WorldToClient(self.__drag_start_pos)
      
                    screen_tl = screen_drag_pos
                    screen_tr = (mouse_pos[0], screen_drag_pos[1])
                    screen_bl = (screen_drag_pos[0], mouse_pos[1])
                    screen_br = mouse_pos

                    world_tl = self.__drag_start_pos
                    world_tr = self.ClientToWorld(screen_tr)
                    world_bl = self.ClientToWorld(screen_bl)
                    world_br = self.ClientToWorld(screen_br)
      
                    for v in Globals.G.nodes():
                        # if the vertex is within all four line segments making
                        # up the rectangle, select it
                        pos = Globals.G.vpos[v]
                        if not ((self.PointLineDist(pos, world_tl, world_tr) == None) or
                                (self.PointLineDist(pos, world_tl, world_bl) == None) or
                                (self.PointLineDist(pos, world_tr, world_br) == None) or
                                (self.PointLineDist(pos, world_bl, world_br) == None)):
                            if v not in self.selected_nodes:
                                self.SelectVertex(v)
                        else:
                            if v in self.selected_nodes:
                                self.DeselectVertex(v)

                    dc.Clear()

                    self.artist.DrawAxes(dc)
                    self.artist.DrawAllEdges(dc)
                    self.artist.DrawAllNodes(dc)

                    dc.DrawLine(screen_tl[0], screen_tl[1], screen_tr[0], screen_tr[1])
                    dc.DrawLine(screen_tl[0], screen_tl[1], screen_bl[0], screen_bl[1])
                    dc.DrawLine(screen_tr[0], screen_tr[1], screen_br[0], screen_br[1])
                    dc.DrawLine(screen_bl[0], screen_bl[1], screen_br[0], screen_br[1])

#    def OnKeyDown(self, event):
#        key = event.GetKeyCode()
#        if key == wx.WXK_DELETE or key == wx.WXK_BACK:
#            self.DeleteSelected()
#            self.Refresh()
#
#        if event.GetModifiers() == wx.MOD_CMD:
#            if key == ord('A'):
#                self.SelectAll()
#                self.Refresh()
#            if key == ord('E'):
#                self.CreateEdgesFromSelection()
#                self.Refresh()
#            if key == ord('P'):
#                self.CreatePathFromSelection()
#                self.Refresh()
                
#    def GetViewScroll(xmin, xmax, ymin, ymax):
#        xmin = scrollXmin
#        xmax = scrollXmax
#        ymin = scrollYmin
#        ymax = scrollYmax
#
#    def SetViewScroll(double xmin, double xmax, double ymin, double ymax)
#        int width, height
#        scrollXmin = xmin
#        scrollXmax = xmax
#        scrollYmin = ymin
#        scrollYmax = ymax
#
#        topLeft = WorldToClient(wxRealPoint(xmin, ymax));
##        topRight = WorldToClient(wxRealPoint(xmax, ymax));
##        bottomLeft = WorldToClient(wxRealPoint(xmin, ymin));
#        bottomRight = WorldToClient(wxRealPoint(xmax, ymin));
#
#        width = bottomRight.x - topLeft.x;
#        height = bottomRight.y - topLeft.y;
#        self.SetScrollbars(5, 5, width/5, height/5, 100, 100);

    def GetSelectedNodes(self):
        return self.selected_nodes

    def GetSelectedEdges(self):
        return self.selected_edges

    def SelectAll(self):
        import Globals
        self.DeselectAll()
        for v in Globals.G.nodes():
            self.selected_nodes.append(v)
        for e in Globals.G.edges():
            self.selected_edges.append(e)
        self.Refresh()

    def DeselectAll(self):
        self.selected_edges = []
        self.selected_nodes = []

    def SelectVertex(self, v):
        self.selected_nodes.append(v)
        self.__execute_callback(self.on_node_select_funcs)

    def DeselectVertex(self, v):
        self.selected_nodes.remove(v)

    def SelectEdge(self, e):
        self.selected_edges.append(e)

    def DeselectEdge(self, e):
        self.selected_edges.remove(e)

    def CreateEdgesFromSelection(self):
        import Globals
        if self.mouse_mode != self.MOUSE_MODE_LOCK:
            # hop around all of the selected vertices creating an edge
            # between every one of them
            for i in range(len(self.selected_nodes)):
                for j in range(i+1, len(self.selected_nodes)):
                    u = self.selected_nodes[i]
                    v = self.selected_nodes[j]
                    if not Globals.G.has_neighbor(u, v):
                        # labeling scheme if we start doing that
                        #size = Globals.G.size()
                        #l = "e%i" % size

                        #while l in Globals.G.elabels_or_whatever:
                        #    size = size + 1
                        #    el = "e%i" % size

                        e = u, v
                        Globals.G.add_edge(*e)
                        self.SelectEdge(e)
        self.Refresh()
        self.__execute_callback(self.on_edge_create_funcs)

    def CreatePathFromSelection(self):
        import Globals
        if self.mouse_mode != self.MOUSE_MODE_LOCK:
            for i in range(len(self.selected_nodes) - 1):
                u = self.selected_nodes[i]
                v = self.selected_nodes[i+1]
                if not Globals.G.has_neighbor(u, v):
                    e = u, v
                    Globals.G.add_edge(*e)
                    self.SelectEdge(e)
        self.Refresh()
        self.__execute_callback(self.on_edge_create_funcs)

    def DeleteSelected(self):
        import Globals
        for v in self.selected_nodes:
            del Globals.G.vpos[v]
            del Globals.G.vlabel[v]
            del Globals.G.vcolor[v]

        Globals.G.delete_edges_from(self.selected_edges)
        Globals.G.delete_nodes_from(self.selected_nodes)
        self.selected_edges = []
        self.selected_nodes = []
        self.Refresh()
        self.__execute_callback(self.on_node_delete_funcs)
        self.__execute_callback(self.on_edge_delete_funcs)

    def SearchNodes(self, p):
        import Globals
        vertices = Globals.G.nodes()
        for v in vertices:
            v_pos = self.WorldToClient(Globals.G.vpos[v])
            if self.TwoPointDist(p, v_pos) <= self.node_radius + self.node_search_dist:
                return v
        return None

    def SearchEdges(self, p):
        import Globals
        edges = Globals.G.edges()
        for e in edges:
            u_pos = self.WorldToClient(Globals.G.vpos[e[0]])
            v_pos = self.WorldToClient(Globals.G.vpos[e[1]])
            dist = self.PointLineDist(p, u_pos, v_pos)
            if dist >= 0.0 and dist <= self.edge_search_dist:
                return e
        return None

    def TwoPointDist(self, p1, p2):
        return math.sqrt( (p2[0] - p1[0])*(p2[0] - p1[0]) + 
                          (p2[1] - p1[1])*(p2[1] - p1[1]) )

    def PointLineDist(self, p, endpoint1, endpoint2):
        x1, y1 = endpoint1[0], endpoint1[1]
        x2, y2 = endpoint2[0], endpoint2[1]
        x3, y3 = p[0], p[1]

        edgeLength = self.TwoPointDist(endpoint1, endpoint2)

        # avoid devide by zero in next computation
        if edgeLength == 0.0:
          return None

        U = ( ( (x3 - x1) * (x2 - x1) ) + ( (y3 - y1) * (y2 - y1) ) ) / (edgeLength * edgeLength)

        # the point isn't within the line segment
        if U < 0.0 or U > 1.0:
          return None

        intersection = N.array([x1 + U * (x2 - x1), y1 + U * (y2 - y1)])
        return self.TwoPointDist(intersection, p)

    def ClientToWorld(self, p):
        dx = (self.x_max - self.x_min) / self.client_size.width
        dy = (self.y_max - self.y_min) / self.client_size.height
        return N.array([p[0] * dx - math.fabs(self.x_min), self.y_max - p[1] * dy])

    def WorldToClient(self, p):
        dx = ( self.client_size.width  / (self.x_max - self.x_min));
        dy = ( self.client_size.height / (self.y_max - self.y_min));
        return N.array([dx * (math.fabs(self.x_min) + p[0]), dy * (self.y_max - p[1])])

