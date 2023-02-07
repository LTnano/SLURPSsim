import pickle
import random
import wx
import operator


#class for monster (self, stats, name)

    #member function generate rest of stats

#function monsterattack
    #get target
    #roll attack
    #deal damage
    #apply debuffs

# dataFight = open("fightdict.txt", "rb") #IMPORTANT FOR LATER
# fightDict = pickle.load(dataFight)

dataCreatures = open("creaturedict.txt", "rb")
creatureDict = pickle.load(dataCreatures)

chosenList = ['meleeSkeleton', 'giantRat']
primedList = []
class SimChar():
    def __init__(self, callsign):

        #build
        type = callsign

        #variables
        self.INIT = 0
        self.curHP = creatureDict[type]['HP']

        #stats
        self.maxHP = creatureDict[type]['HP']
        self.STR = creatureDict[type]['STR']
        self.END = creatureDict[type]['END']
        self.COR = creatureDict[type]['COR']
        self.DEX = creatureDict[type]['DEX']
        self.INT = creatureDict[type]['INT']
        self.NOU = creatureDict[type]['NOU']
        self.WIL = creatureDict[type]['WIL']

        #bools
        self.isAlive = True

        #weapon generation
        self.WEA = random.randint(1,4)
        
def constructFighters():
    for i in chosenList:
        primedList.append(SimChar(i))


def rollInitiative():
    for monster in primedList:
        monster.INIT = monster.COR + random.randint(1,20)
    primedList.sort(key=operator.attrgetter('INIT'))





# def executeCombat():
    

# in order of initiative
#     check if alive
#     if ranged target selection (choose ranged attack) monster attacks (bool has attacked)
#     otherwise move unless near enemy (bool has moved)
#     target selection attack (choose melee attack)
#     move   


# def cfight(crea1, damage):
#         crea1.curHP = crea1.curHP - damage


if __name__ == '__main__':
    constructFighters()
    rollInitiative()

# def beginCombat(fightDict, ):
#     Skeleton = SimChar("meleeSkeleton", "Skeleton")
#     #roll initiative
#     for each in fightDict:
#         random.randint(1,20) + fightDict.


# def beginCombat(combatantList):
#     for pos in initList:
#         moved = False
#         attacked = False
#         ranged = crea1.
#         if (ranged)
#             cfight(findTar())
#             attacked = True
        

       



        

# print(Skeleton.curHP)

# takeDam(Skeleton, 45)

# print(Skeleton.curHP)