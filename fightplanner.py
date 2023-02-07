import pickle
import random
import wx


class MyFrame(wx.Frame):    #main ui class
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Press Me')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)        
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()


dataCreatures = open("creaturedict.txt", "wb")
creatureDict = {'giantRat' : {'HP' : 50, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 8, 'INT' : 12, 'NOU' : 4, 'WIL' : 3},
                'meleeSkeleton' : {'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7}}
pickle.dump(creatureDict, dataCreatures)
dataCreatures.close()