import pickle
import random
import wx
import operator


#class for monster (self, stats, name)

    #member function generate rest of stats



# dataFight = open("fightdict.txt", "rb") #IMPORTANT FOR LATER
# fightDict = pickle.load(dataFight)

dataCreatures = open("creaturedict.txt", "rb")
dataHasAbility = open("creaturhasabilitydict.txt", "rb")
hasAbilityDict = pickle.load(dataHasAbility)
creatureDict = pickle.load(dataCreatures)

chosenList = ['thinBilly', 'bossSkeleton', 'wizardKobold', 'wizardKobold', 'rangedSkeletonH', 'giantRat']
teamList = [1, 1, 2, 1, 2, 2]
primedList = []

class SimChar():
    def __init__(self, callsign):
        
        #build
        type = callsign

        #name for logs
        self.printName = creatureDict[type]['Name']

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

        #weapon assignment
        self.WEA = creatureDict[type]['WEA']

        #ability logic
        self.AP = creatureDict[type]['AP']
        self.abilities = hasAbilityDict[type]
   
class Ability():
    def __init__(self, abilityname):
        type = abilityname
        self.stat = 'STR'
        self.average = 2
        self.ranged = True

        #STAT + average damage = damage

def constructAbilties():
    for monster in primedList:
        primedList.abilities = hasAbilityDict[i]

def constructFighters():
    for i in chosenList:
        primedList.append(SimChar(i))


def rollInitiative():
    for monster, team in zip(primedList, teamList):
        monster.INIT = monster.COR + random.randint(1,20)
        monster.TEAM = team
    primedList.sort(key=operator.attrgetter('INIT'),reverse=True)

def beginCombatLoop(monList):
    for monster in monList:
        monster.moved = False
        monster.attacked = False
        findTar(monster, monList)


def findTar():
    #find target
    return 0

def checkBuff():
    #check buffs
    return 0

def attackmove(cr1, cr2, ability):
    random.randint(1,20) + ability.stat
    #check range
    #move if out of range
    #roll attack
    #deal damage
    #move if havent moved
    #apply debuffs

def bestAbil():
    #pick ability
    return 0

#function monsterattack
   

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
    for monster in primedList:
        print ('\n', monster.printName)
        print ('Initiative:', monster.INIT)
        print ('Team:', monster.TEAM)
        print ('HP:', monster.curHP)
        print ('AP', monster.AP)
        print ('Abilities: ', monster.abilities)
        

        

# def beginCombat(fightDict, ):
#     Skeleton = SimChar("meleeSkeleton", "Skeleton")
#     #roll initiative
#     for each in fightDict:
#         random.randint(1,20) + fightDict.



        

       



        

# print(Skeleton.curHP)

# takeDam(Skeleton, 45)

# print(Skeleton.curHP)