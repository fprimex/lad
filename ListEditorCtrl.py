import sys
import operator
import wx
import  wx.lib.mixins.listctrl  as  listmix
from bisect import bisect

LE_COPY = wx.NewId()
LE_INS = wx.NewId()
LE_DEL = wx.NewId()
LE_REFRESH = wx.NewId()

class ListEditorCtrl(wx.ListCtrl,
           listmix.ListCtrlAutoWidthMixin,
           listmix.TextEditMixin):

  def __init__(self, parent, ID, headings, listdata, pos=wx.DefaultPosition,
         size=wx.DefaultSize, style=0):
    wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
    listmix.ListCtrlAutoWidthMixin.__init__(self)
    listmix.TextEditMixin.__init__(self)

    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDouble)
    self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

    self.base_name = headings[0]
    for i in range(0, len(headings)):
      self.InsertColumn(i, headings[i])

    self.listctrldata = listdata
    self.context_menu = wx.Menu()

    self.Bind(wx.EVT_MENU, self.OnCopy, id=LE_COPY)
    self.context_menu.Append(LE_COPY, "Copy")
    self.Bind(wx.EVT_MENU, self.OnInsert, id=LE_INS)
    self.context_menu.Append(LE_INS, "Insert Row")
    self.Bind(wx.EVT_MENU, self.OnDelete, id=LE_DEL)
    self.context_menu.Append(LE_DEL, "Delete Selection")
    self.context_menu.AppendSeparator()
    self.Bind(wx.EVT_MENU, self.OnRefreshList, id=LE_REFRESH)
    self.context_menu.Append(LE_REFRESH, "Refresh")

    self.RefreshList()

    self.col_locs = [0]
    loc = 0
    for n in range(self.GetColumnCount()):
      loc = loc + self.GetColumnWidth(n)
      self.col_locs.append(loc)

  def RefreshList(self):
    self.DeleteAllItems()

    for row in self.listctrldata.keys():
      row_data = self.GetRowValues(row)
      index = self.InsertItem(sys.maxsize, row_data[0])
      for i in range(0, len(row_data)):
        self.SetItem(index, i, row_data[i])
        self.SetItemData(index, row)

    # if there are items, auto-size each col
    for n in range(self.GetColumnCount()):
      self.SetColumnWidth(n, wx.LIST_AUTOSIZE)

    self.resizeColumn(self.GetColumnWidth(0))

    # if there are no items, size each col equally
    if self.GetItemCount() == 0:
      cols = self.GetColumnCount()
      width = self.GetClientSize()[0] / cols
      for n in range(cols):
        self.SetColumnWidth(n, width)


  def OpenEditor(self, col, row):
    """
    Opens an editor at the current position.
    Modified to allow a generic getter to set editor text.
    """

    # give the derived class a chance to Allow/Veto this edit.
    evt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_BEGIN_LABEL_EDIT, self.GetId())
    evt.m_itemIndex = row
    evt.m_col = col
    item = self.GetItem(row, col)
    evt.m_item.SetId(item.GetId()) 
    evt.m_item.SetColumn(item.GetColumn()) 
    evt.m_item.SetData(item.GetData()) 
    evt.m_item.SetText(item.GetText()) 
    ret = self.GetEventHandler().ProcessEvent(evt)
    if ret and not evt.IsAllowed():
      return   # user code doesn't allow the edit.

    if self.GetColumn(col).m_format != self.col_style:
      self.make_editor(self.GetColumn(col).m_format)
  
    x0 = self.col_locs[col]
    x1 = self.col_locs[col+1] - x0

    scrolloffset = self.GetScrollPos(wx.HORIZONTAL)

    # scroll forward
    if x0+x1-scrolloffset > self.GetSize()[0]:
      if wx.Platform == "__WXMSW__":
        # don't start scrolling unless we really need to
        offset = x0+x1-self.GetSize()[0]-scrolloffset
        # scroll a bit more than what is minimum required
        # so we don't have to scroll everytime the user presses TAB
        # which is very tireing to the eye
        addoffset = self.GetSize()[0]/4
        # but be careful at the end of the list
        if addoffset + scrolloffset < self.GetSize()[0]:
          offset += addoffset

        self.ScrollList(offset, 0)
        scrolloffset = self.GetScrollPos(wx.HORIZONTAL)
      else:
        # Since we can not programmatically scroll the ListCtrl
        # close the editor so the user can scroll and open the editor
        # again
        self.editor.SetValue(self.GetItem(row, col).GetText())
        self.curRow = row
        self.curCol = col
        self.CloseEditor()
        return

    y0 = self.GetItemRect(row)[1]
    
    editor = self.editor
    editor.SetDimensions(x0-scrolloffset,y0, x1,-1)
    
    editor.SetValue(self.GetEditValue(row, col)) 
    
    editor.Show()
    editor.Raise()
    editor.SetSelection(-1,-1)
    editor.SetFocus()
  
    self.curRow = row
    self.curCol = col

  def CloseEditor(self, evt=None):
    """
    Close the editor and save the new value to the ListCtrl.
    Modified to allow a generic setter to save edited data.
    """
    if not self.editor.IsShown():
      return
    text = self.editor.GetValue()
    self.editor.Hide()
    self.SetFocus()

    self.SetValue(self.curRow, self.curCol, text)
    
    # post wxEVT_COMMAND_LIST_END_LABEL_EDIT
    # Event can be vetoed. It doesn't has SetEditCanceled(), what would 
    # require passing extra argument to CloseEditor() 
    evt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT, self.GetId())
    evt.m_itemIndex = self.curRow
    evt.m_col = self.curCol
    item = self.GetItem(self.curRow, self.curCol)
    evt.m_item.SetId(item.GetId()) 
    evt.m_item.SetColumn(item.GetColumn()) 
    evt.m_item.SetData(item.GetData()) 
    evt.m_item.SetText(text) #should be empty string if editor was canceled
    ret = self.GetEventHandler().ProcessEvent(evt)
    if not ret or evt.IsAllowed():
      if self.IsVirtual():
        # replace by whather you use to populate the virtual ListCtrl
        # data source
        self.SetVirtualData(self.curRow, self.curCol, text)
      else:
        self.SetStringItem(self.curRow, self.curCol, text)
    self.RefreshItem(self.curRow)
    self.RefreshList()

  def OnChar(self, event):
    """Catch ESC and cancel gracefully, preserving data"""
    if event.GetKeyCode() == wx.WXK_ESCAPE:
      if not self.editor.IsShown():
        return
      self.editor.Hide()
      self.SetFocus()
    else:
      listmix.TextEditMixin.OnChar(self, event)

  def OnLeftDown(self, evt=None):
    evt.Skip()

  def OnLeftDouble(self, evt=None):
    """Open the editor on double clicks"""
    
    if self.editor.IsShown():
      self.CloseEditor()
      
    x,y = evt.GetPosition()
    row,flags = self.HitTest((x,y))
  
    # the following should really be done in the mixin's init but
    # the wx.ListCtrl demo creates the columns after creating the
    # ListCtrl (generally not a good idea) on the other hand,
    # doing this here handles adjustable column widths
    
    self.col_locs = [0]
    loc = 0
    for n in range(self.GetColumnCount()):
      loc = loc + self.GetColumnWidth(n)
      self.col_locs.append(loc)

    col = bisect(self.col_locs, x+self.GetScrollPos(wx.HORIZONTAL)) - 1
    self.OpenEditor(col, row)

  def OnRightDown(self, event):
    if self.editor.IsShown():
      self.CloseEditor()
      
    x, y = event.GetPosition()
    row, flags = self.HitTest((x,y))

    if row != self.curRow: # self.curRow keeps track of the current row
      self.Select(self.curRow, on=0)
    self.Select(row)

    self.col_locs = [0]
    loc = 0
    for n in range(self.GetColumnCount()):
      loc = loc + self.GetColumnWidth(n)
      self.col_locs.append(loc)

    self.curCol = bisect(self.col_locs, x+self.GetScrollPos(wx.HORIZONTAL)) - 1

    self.PopupMenu(self.context_menu)

  def OnCopy(self, event):
    wx.TheClipboard.Open()
    str = wx.TextDataObject()
    str.SetText(self.GetItem(self.curRow, self.curCol).GetText())
    wx.TheClipboard.SetData(str)

  def OnInsert(self, event):
    num = len(self.listctrldata.keys())
    name = self.base_name + repr(num + 1)
    col_one_items = map(operator.itemgetter(0), self.listctrldata.values())
    while name in col_one_items:
      num += 1
      name = self.base_name + repr(num + 1)
      
    value = "None"
    index = self.InsertStringItem(sys.maxint, name)
    self.SetStringItem(index, 0, name)
    for n in range(1, self.GetColumnCount()):
      self.SetStringItem(index, n, value)
    self.SetItemData(index, num)

    self.listctrldata[index] = (name, value)
    self.PostInsert(index)

    self.OpenEditor(0, index)

  def OnDelete(self, event):
    # build selection list
    item = self.GetFirstSelected()
    selection = []
    while item != -1:
      selection.append(item)
      item = self.GetNextSelected(item)

    # delete items in reverse
    selection.sort(reverse=True)
    for item in selection:
      self.PreDelete(item)
      del self.listctrldata[item]
      #del Vars[self.GetItem(item, 0).GetText()]
      self.DeleteItem(item)

    # repack the listctrldata dict - indexed from 0
    index = 0
    newdata = {}
    ordered_keys = self.listctrldata.keys()
    ordered_keys.sort()
    for key in ordered_keys:
      var = self.listctrldata[key][0]
      exp = self.listctrldata[key][1]
      newdata[index] = (var, exp)
      index += 1
    self.listctrldata = newdata

    self.RefreshList()

  def OnRefreshList(self, event):
    self.RefreshList()

  def GetRowValues(self, row):
    return self.listctrldata[row]

  def GetEditValue(self, row, col):
    return self.GetItem(row, col).GetText()
  
  def SetValue(self, row, col, text):
    l = list(self.listctrldata[row])
    l[col] = text
    self.listctrldata[row] = tuple(l)

  def PreDelete(self, row):
    pass

  def PostInsert(self, row):
    pass
