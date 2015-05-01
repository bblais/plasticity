# containers.py
# Containers are mixin classes that have a sizer and a number of methods to
# deal with that sizer (add components, etc).  Used to implement fairly
# "basic" controls like Panel and Frame.  When in doubt, derive from those
# two rather than making up your own container construct.

import utils
import waxyobject
import wx
import warnings

class Container(waxyobject.WaxyObject):

    def _create_sizer(self, direction):
        if direction.lower().startswith("h"):
            dir = wx.HORIZONTAL
        elif direction.lower().startswith("v"):
            dir = wx.VERTICAL
        else:
            raise ValueError, "Incorrect direction"
        self.sizer = wx.BoxSizer(dir)
        self._packed = 0

    def Body(self):
        """ Optionally override this to create components.  Add them with the
            AddComponent() method. """

    def AddComponent(self, comp, expand=0, stretch=0, align=None, border=0):
        # expand: expands a component in the direction of the panel/sizer
        # stretch: expands a component in the other direction
        # for example, if we have a horizontal panel, and resize the window
        # both horizontally and vertically, then a component with 'expand'
        # will expand horizontally, and one with 'stretch' will expand
        # vertically. (See simplebuttons.py)

        if isinstance(expand, str):
            expand = expand.lower()
            if expand.startswith("h"):
                if self.GetOrientation() == 'horizontal':
                    expand, stretch = 1, 0
                else:
                    expand, stretch = 0, 1
            elif expand.startswith("v"):
                if self.GetOrientation() == 'horizontal':
                    expand, stretch = 0, 1
                else:
                    expand, stretch = 1, 0
            elif expand.startswith("b"):
                expand = stretch = 1
            elif expand == '':
                expand = stretch = 0
            else:
                raise ValueError, "Invalid value for expand: %r" % (expand,)

        flags = 0
        if stretch:
            flags |= wx.EXPAND
        if align:
            flags |= {
                "t": wx.ALIGN_TOP,
                "c": wx.ALIGN_CENTER,
                "b": wx.ALIGN_BOTTOM,
                "r": wx.ALIGN_RIGHT,
                "l": wx.ALIGN_LEFT,
            }.get(align.lower()[:1], 0)
        if border:
            flags |= wx.ALL

        flags |= wx.FIXED_MINSIZE
        if 0 and hasattr(comp, 'sizer') and hasattr(comp, '_include_sizer'):
            # ugly hack to add nested sizer rather than its frame
            # only for certain quirky controls, like GroupBox!
            self.sizer.Add(comp.sizer, expand, flags)
        else:
            self.sizer.Add(comp, expand, flags, border)
            # comp can be a component or a tuple (width, height), but the
            # Add() method is called just the same, as of wxPython 2.5.1.5

    def AddSpace(self, width, height=None, *args, **kwargs):
        if height is None:
            height = width
        return self.AddComponent((width, height), *args, **kwargs)
    AddSeparator = AddSpace

    def Pack(self):
        if not self._packed:
            self.SetSizerAndFit(self.sizer)
            self._packed = 1

    def Repack(self):
        self.sizer.RecalcSizes()

    def GetOrientation(self):
        """ Return 'horizontal' or 'vertical'. """
        orientation = self.sizer.GetOrientation()
        if orientation == wx.HORIZONTAL:
            return 'horizontal'
        elif orientation == wx.VERTICAL:
            return 'vertical'
        else:
            raise ValueError, "Unknown direction for sizer"

#
# GridContainer (used to implement GridPanel)

class GridContainer(Container):

    _sizerclass = wx.GridSizer

    alignment = {
        'b': wx.ALIGN_BOTTOM,
        'r': wx.ALIGN_RIGHT,
        'l': wx.ALIGN_LEFT,
        'c': wx.ALIGN_CENTER,
        't': wx.ALIGN_TOP,
        'h': wx.ALIGN_CENTER_HORIZONTAL,
        'v': wx.ALIGN_CENTER_VERTICAL,
    }

    def _create_sizer(self, rows, cols, hgap=1, vgap=1):
        self.sizer = self._sizerclass(rows, cols, vgap, hgap)
        self.controls = {}
        for row in range(rows):
            for col in range(cols):
                self.controls[col, row] = None
                # (col, row) allows for (x, y)-like calling
        self._packed = 0

    def AddComponent(self, col, row, obj, expand=1, align='', border=0, stretch=0, proportion=0):
        # make sure the parents are correct
        if stretch:
            warnings.warn("stretch is deprecated and has no effect here")

        if self.controls[col, row]:
            raise ValueError, "A control has already been set for position (%s, %s)" % (row, col)
        self.controls[col, row] = {'obj': obj, 'expand': expand, 'align': align,
                                   'border': border, 'proportion': proportion}

    def Pack(self):
        if not self._packed:
            controls = self._AllControls()
            self.sizer.AddMany(controls)
            self.SetSizerAndFit(self.sizer) # is this still necessary?
            self._packed = 1

    def __setitem__(self, index, value):
        col, row = index
        self.AddComponent(col, row, value)

    def __getitem__(self, index):
        col, row = index
        return self.controls[col, row]['obj']  # may raise KeyError

    def _AllControls(self):
        controls = []
        for row in range(self.sizer.GetRows()):
            for col in range(self.sizer.GetCols()):
                d = self.controls[col, row]
                if d is None:
                    from panel import Panel
                    p = Panel(self) # hack up a dummy panel
                    controls.append((p, 0, wx.EXPAND|wx.FIXED_MINSIZE))
                else:
                    obj = d['obj']

                    # set alignment
                    align = d['align'].lower()
                    alignment = 0
                    for key, value in self.__class__.alignment.items():
                        if key in align:
                            alignment |= value

                    z = d['expand'] and wx.EXPAND
                    z |= alignment
                    border = d['border']
                    #if border and not alignment:
                    if border:
                        z |= wx.ALL
                    z |= wx.FIXED_MINSIZE
                    proportion = d['proportion']
                    controls.append((obj, proportion, z, border))

        return controls

    # XXX maybe a Wax version of AddMany() would be useful?

#
# FlexGridContainer

class FlexGridContainer(GridContainer):
    _sizerclass = wx.FlexGridSizer

    def AddGrowableRow(self, row):
        self.sizer.AddGrowableRow(row)

    def AddGrowableCol(self, col):
        self.sizer.AddGrowableCol(col)

#
# OverlayContainer

class OverlaySizer(wx.PySizer):
    def __init__(self):
        wx.PySizer.__init__(self)

    def CalcMin(self):
        maxx, maxy = 0, 0
        for win in self.GetChildren():
            x, y = win.CalcMin()
            maxx = max(maxx, x)
            maxy = max(maxy, y)
        return wx.Size(maxx, maxy)

    def RecalcSizes(self):
        pos = self.GetPosition()
        size = self.GetSize()
        for win in self.GetChildren():
            win.SetDimension(pos, size)


class OverlayContainer(Container):
    """ Container that takes an arbitrary number of windows, and stacks them
        on top of each other.  Controls are hidden by default. """

    def _create_sizer(self):
        self.sizer = OverlaySizer()
        self.windows = []
        self._packed = 0

    def AddComponent(self, window, expand=0, stretch=0, align=None, border=0):
        """
        # make sure the parents are correct
        if waxconfig.WaxConfig.check_parent:
            if window.GetParent() is not self:
                utils.parent_warning(window, self)

        flags = 0
        if stretch:
            flags |= wx.EXPAND
        if align:
            flags |= {
                "t": wx.ALIGN_TOP,
                "c": wx.ALIGN_CENTER,
                "b": wx.ALIGN_BOTTOM,
                "r": wx.ALIGN_RIGHT,
                "l": wx.ALIGN_LEFT,
            }.get(align.lower()[:1], 0)
        if border:
            flags |= wx.ALL
        flags |= wx.FIXED_MINSIZE

        self.sizer.Add(window, expand, flags, border)
        """
        Container.AddComponent(self, window, expand, stretch, align, border)
        self.windows.append(window)
        window.Hide()   # default is hiding

    

#
# GroupBoxContainer

class GroupBoxContainer(Container):

    def _create_sizer(self, groupbox, direction='h'):
        direction = direction.lower()
        if direction.startswith('v'):
            dir = wx.VERTICAL
        elif direction.startswith('h'):
            dir = wx.HORIZONTAL
        else:
            raise ValueError, "Unknown direction: %s" % (direction,)

        self.sizer = wx.StaticBoxSizer(groupbox, dir)
        self._packed = 0

#
# PlainContainer

class PlainContainer(Container):
    """ A container without a sizer.  Controls must be added at a given position.
        Size can be specified as well.
    """

    def _create_sizer(self):
        self.sizer = None
        self._packed = 0    # included for compatibility

    def AddComponent(self, x, y, comp):
        # make sure the parents are correct

        comp.SetPosition((x, y))

    def AddComponentAndSize(self, x, y, sx, sy, comp):
        # make sure the parents are correct

        comp.SetPosition((x, y))
        comp.SetSize((sx, sy))

    def Pack(self):
        self._packed = 1    # useless, but included for compatibility

        if len(self.Children) == 1:
            import panel
            dummy = panel.Panel(self, size=(0,0))
            dummy.Position = 0, 0
            self.__dummy = dummy

    def Repack():
        pass

