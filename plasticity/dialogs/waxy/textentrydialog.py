# textentrydialog.py
# Simple dialog for entering a string.
# Note: Not based on wxPython's TextEntryDialog.

from dialog import Dialog
from textbox import TextBox
from label import Label
from keys import keys

class TextEntryDialog(Dialog):

    def __init__(self, parent, title="Enter some text", prompt="Enter some text",
     default="", cancel_button=1):
        self.prompt = prompt
        self.default = default
        Dialog.__init__(self, parent, title, cancel_button=cancel_button)

    def Body(self):
        label = Label(self, self.prompt)
        self.AddComponent(label, expand='h', border=7)

        self.text = TextBox(self, size=(100,25), process_enter=1)
        self.text.SetValue(self.default)
        self.text.OnChar = self.OnTextBoxChar
        self.AddComponent(self.text, expand='h', border=5)

    def OnTextBoxChar(self, event=None):
        # pressing Enter in the TextBox is the same as clicking OK
        if event.GetKeyCode() == keys.enter:
            self.OnClickOKButton(event)
        else:
            event.Skip()

    def GetValue(self):
        return self.text.GetValue()

