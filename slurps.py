import pickle
import random
import wx


#class for monster (self, stats, name)

    #member function generate rest of stats

#function monsterattack
    #get target
    #roll attack
    #deal damage
    #apply debuffs


dataCreatures = open("creaturedict.txt", "rb")
creatureDict = pickle.load(dataCreatures)

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