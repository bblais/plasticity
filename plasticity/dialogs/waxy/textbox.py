# textbox.py

import waxyobject
import wx
import core
import styles

class TextBox(wx.TextCtrl, waxyobject.WaxyObject):

    __events__ = {
        'Char': wx.EVT_CHAR,    # do all controls have this?
        'MaxLength': wx.EVT_TEXT_MAXLEN,  # alias for TextMaxLen
        'Text': wx.EVT_TEXT,
        'TextEnter': wx.EVT_TEXT_ENTER,
        'TextMaxLen': wx.EVT_TEXT_MAXLEN,
        'TextURL': wx.EVT_TEXT_URL,
    }

    def __init__(self, parent, text="", size=None, **kwargs):
        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)

        wx.TextCtrl.__init__(self, parent, wx.NewId(), text,
         size=size or (125,-1), style=style)

        self.BindEvents()
        styles.properties(self, kwargs)

    def write(self, s):
        # Added so we can use a TextBox as a file-like object and redirect
        # stdout to it.
        self.AppendText(s)
        try:
            core.Yield()
        except:
            pass

    def GetCurrentLineNumber(self):
        """ Return the current line number (i.e. the number of the line the
            cursor is on). """
        pos = self.GetInsertionPoint()
        x, y = self.PositionToXY(pos)
        return y

    def GetLines(self):
        """ Return the current text as a list of lines.  (Changing the list
            does not affect the contents of the TextBox.) """
        text = self.GetValue()
        lines = text.split("\n")
        return lines

    def SetModified(self, modified):
        if modified:
            # set to modified by appending a dummy space and removing it again
            self.AppendText(' ')
            lastpos = self.GetLastPosition()
            self.Remove(lastpos-1, lastpos)
        else:
            self.DiscardEdits()

    def GetModified(self):
        """ Returns true if the contents of the control were modified.  (Alias
            for IsModified(). """
        return self.IsModified()

    def InsertText(self, pos, text):
        """ Insert text at the given position. """
        old_insertion_point = self.GetInsertionPoint()
        self.SetInsertionPoint(pos)
        self.WriteText(text)
        # put cursor at original insertion point
        if old_insertion_point <= pos:
            self.SetInsertionPoint(old_insertion_point)
        else:
            self.SetInsertionPoint(old_insertion_point + len(text))

    # ideas:
    # should Remove support negative indexes? (like slices)
    # should it support slicing?  e.g. del atextbox[10:20]

    #
    # style parameters

    #_textbox_justify = {
    #    "left": wx.TE_LEFT,
    #    "center": wx.TE_CENTRE,
    #    "centre": wx.TE_CENTRE,
    #    "middle": wx.TE_CENTRE,
    #    "right": wx.TE_RIGHT,
    #}

    __styles__ = {
        'justify': ({
            'left': wx.TE_LEFT,
            'center': wx.TE_CENTRE,
            'centre': wx.TE_CENTRE,
            'middle': wx.TE_CENTRE,
            'right': wx.TE_RIGHT,
        }, styles.DICTSTART),
        'multiline': (wx.TE_MULTILINE, styles.NORMAL),
        'password': (wx.TE_PASSWORD, styles.NORMAL),
        'readonly': (wx.TE_READONLY, styles.NORMAL),
        'wrap': (wx.TE_DONTWRAP, styles.NORMAL | styles.REVERSE),
        'process_enter': (wx.TE_PROCESS_ENTER, styles.NORMAL),
        'process_tab': (wx.TE_PROCESS_TAB, styles.NORMAL),
        'rich': (wx.TE_RICH, styles.NORMAL),
        'rich2': (wx.TE_RICH2, styles.NORMAL),
        'auto_url': (wx.TE_AUTO_URL, styles.NORMAL),
        'hscroll': (wx.HSCROLL, styles.NORMAL),
    }
        
    def _params(self, kwargs):
        flags = 0 | wx.TE_NOHIDESEL # maybe add the option of changing this one
        #flags |= styles.stylebool('multiline', wx.TE_MULTILINE, kwargs)
        #flags |= styles.stylebool('password', wx.TE_PASSWORD, kwargs)
        #flags |= styles.stylebool('readonly', wx.TE_READONLY, kwargs)
        #flags |= styles.stylebool('wrap', wx.TE_DONTWRAP, kwargs, reverse=1)
        #flags |= styles.stylebool('process_enter', wx.TE_PROCESS_ENTER, kwargs)
        #flags |= styles.stylebool('process_tab', wx.TE_PROCESS_TAB, kwargs)
        #flags |= styles.stylebool('rich', wx.TE_RICH, kwargs)
        #flags |= styles.stylebool('rich2', wx.TE_RICH2, kwargs)
        #flags |= styles.stylebool('auto_url', wx.TE_AUTO_URL, kwargs)
        #flags |= styles.stylebool('hscroll', wx.HSCROLL, kwargs)
        #flags |= styles.styledictstart('justify', self._textbox_justify, kwargs, 0)
        flags |= styles.dostyle(self.__styles__, kwargs)
        return flags

