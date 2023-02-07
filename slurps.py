import pickle
import random
import wx


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        panel = wx.Panel(self)

        self.text_ctrl = wx.TextCtrl(panel, pos=(5, 5))
        my_btn = wx.Button(panel, label='Press Me', pos=(5, 55))

        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()

#class for monster (self, stats, name)

    #member function generate rest of stats

#function monsterattack
    #get target
    #roll attack
    #deal damage
    #apply debuffs



dataCreatures = open("creaturedict.txt", "wb")
creatureDict = {'giantRat' : {'HP' : 50, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 8, 'INT' : 12, 'NOU' : 4, 'WIL' : 3},
                'meleeSkeleton' : {'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7}}
pickle.dump(creatureDict, dataCreatures)
dataCreatures.close()

abilityDict = dict()


# dataCreatures = open("creaturedict.txt", "rb")
# creatureDict = pickle.load(dataCreatures)

class SimChar():
    def __init__(self, name):
        type = name
        self.maxHP = creatureDict[type]['HP']
        self.curHP = creatureDict[type]['HP']
        self.STR = creatureDict[type]['STR']
        self.END = creatureDict[type]['END']
        self.COR = creatureDict[type]['COR']
        self.DEX = creatureDict[type]['DEX']
        self.INT = creatureDict[type]['INT']
        self.NOU = creatureDict[type]['NOU']
        self.WIL = creatureDict[type]['WIL']
        self.WEA = random.randint(1,4)