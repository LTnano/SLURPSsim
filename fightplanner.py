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
creatureDict = {'giantRat' : {'Name': 'Giant Rat', 'HP' : 50, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 8, 'INT' : 2, 'NOU' : 4, 'WIL' : 3, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 0},

                'meleeSkeleton' : {'Name' : 'Skeleton', 'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 2, 'AP' : 0},

                'meleeSkeletonH' : {'Name' : 'Skeleton (Hard)', 'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 6},

                'rangedSkeleton' : {'Name': 'Skeleton Archer', 'HP' : 110, 'STR' : 8, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 4, 'ARM' : 0, 'AP' : 0},

                'rangedSkeletonH' : {'Name' : 'Skeleton Archer(Hard)', 'HP' : 110, 'STR' : 8, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 6, 'ARM' : 0, 'AP' : 0},

                'wizardSkeleton' : {'Name': 'Skeleton Wizard', 'HP' : 100, 'STR' : 7, 'END' : 8, 'COR' : 8, 'DEX' : 7, 'INT' : 11, 'NOU' : 6, 'WIL' : 2, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

                'meleeKobold' : {'Name': 'Kobold Warrior', 'HP' : 60, 'STR' : 9, 'END' : 6, 'COR' : 8, 'DEX' : 5, 'INT' : 5, 'NOU' : 6, 'WIL' : 4, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 1, 'AP' : 0},

                'wizardKobold' : {'Name': 'Kobold Mage', 'HP' : 40, 'STR' : 6, 'END' : 6, 'COR' : 7, 'DEX' : 7, 'INT' : 10, 'NOU' : 7, 'WIL' : 8, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 7},

                'rangedKobold' : {'Name': 'Kobold Archer', 'HP' : 40, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 9, 'INT' : 8, 'NOU' : 6, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 4, 'ARM' : 0, 'AP' : 6},

                'priestKobold' : {'Name': 'Kobold Healer', 'HP' : 30, 'STR' : 3, 'END' : 5, 'COR' : 8, 'DEX' : 9, 'INT' : 7, 'NOU' : 6, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 7},

                'summonerKobold' : {'Name' : 'Kobold Summoner', 'HP' : 100, 'STR' : 5, 'END' : 5, 'COR' : 10, 'DEX' : 10, 'INT' : 10, 'NOU' : 9, 'WIL' : 10, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 0},

                'slowGolem' : {'Name': 'Golem', 'HP' : 300, 'STR' : 14, 'END' : 30, 'COR' : 8, 'DEX' : 4, 'INT' : 2, 'NOU' : 2, 'WIL' : 2, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 5, 'AP' : 0},

                'thinBilly' : {'Name' : 'Thin Billy', 'HP' : 200, 'STR' : 13, 'END' : 20, 'COR' : 13, 'DEX' : 13, 'INT' : 13, 'NOU' : 17, 'WIL' : 13, 'WEA' : 8, 'RWEA' : 0, 'ARM' : 2, 'AP' : 10},
                
                'bossSkeleton' : {'Name' : 'Captain Boney', 'HP' : 250, 'STR' : 15, 'END' : 25, 'COR' : 15, 'DEX' : 12, 'INT' : 17, 'NOU' : 12, 'WIL' : 13, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 5, 'AP' : 12}}
pickle.dump(creatureDict, dataCreatures)
dataCreatures.close()