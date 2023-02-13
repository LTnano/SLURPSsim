import pickle
import random
import wx
import operator


#class for monster (self, stats, name)

    #member function generate rest of stats



# dataFight = open("fightdict.txt", "rb") #IMPORTANT FOR LATER
# fightDict = pickle.load(dataFight)

dataCreatures = open("creaturedict.txt", "rb")
creatureDict = pickle.load(dataCreatures)

dataHasAbility = open("creaturhasabilitydict.txt", "rb")
hasAbilityDict = pickle.load(dataHasAbility)

# dataAbilityDef = open("abilitydefdict.txt", "rb")
# abilityDefinitions = pickle.load(dataAbilityDef)



chosenList = ['thinBilly', 'bossSkeleton', 'wizardKobold', 'wizardKobold', 'rangedSkeletonH', 'giantRat']
teamList = [1, 1, 2, 1, 2, 2]
primedList = []
uniqueAbilityList = []
abilityList = []

class Creature():
    def __init__(self, type):
        
        #name for logs
        self.printName = creatureDict[type]['Name']

        #variables
        self.INIT = 0
        self._curHP = creatureDict[type]['HP']
        self.isAlive = True

        #stats
        self._HP = creatureDict[type]['HP']
        self._STR = creatureDict[type]['STR']
        self._END = creatureDict[type]['END']
        self._COR = creatureDict[type]['COR']
        self._DEX = creatureDict[type]['DEX']
        self._INT = creatureDict[type]['INT']
        self._NOU = creatureDict[type]['NOU']
        self._WIL = creatureDict[type]['WIL']

        # temp stats
        self.tempSTR = 0
        self.tempEND = 0
        self.tempCOR = 0
        self.tempDEX = 0
        self.tempINT = 0
        self.tempNOU = 0
        self.tempWIL = 0

               
        #status effects
        self.isBlocking = 0
        self.isCharmed = 0
        self.isClumsy = 0
        self.isDisarmed = 0
        self.isDoppelgangered = 0
        self.isEncouraged = 0
        self.isImmobilised = 0
        self.isLevitated = 0
        self.isPanicked = 0
        self.isPetrified = 0
        self.isProne = 0
        self.isScared = 0
        self.isStunned = 0
        
        

        #equip assignment
        self._WEA = creatureDict[type]['WEA']
        self._RWEA = creatureDict[type]['RWEA']
        self.ARM = creatureDict[type]['ARM']
        self.baseARM = creatureDict[type]['ARM']

        #ability logic
        self.AP = creatureDict[type]['AP']
        self.abilities = hasAbilityDict[type]
        self.prioList = []

    #put abilities as methods
    def takeDamage(self, damage):
        self.HP = self.HP - damage
        return
    
    def useAbility(self, name):
        return self.ability[name]
    
    def strength(self):
        return self._STR + self.tempSTR
    
    def coordination(self):
        return self._COR + self.tempCOR
    
    def endurance(self):
        return self._END + self.tempEND
    
    def dexterity(self):
        return self._DEX + self.tempDEX
    
    def intelligence(self):
        return self._INT + self.tempINT
    
    def nouse(self):
        return self._NOU + self.tempNOU
    
    def will(self):
        return self._WIL + self.tempWIL

def statusTicker(monster):

    if (monster.isStunned):
        monster.isStunned -= 1

    if (monster.isScared):
        monster.isScared -= 1
        if not(monster.isScared):
            monster.tempSTR += 1
            monster.tempEND += 1
            monster.tempCOR += 1
            monster.tempDEX += 1
            monster.tempINT += 1
            monster.tempNOU += 1
            monster.tempWIL += 1

    if (monster.isProne):
        monster.isProne -= 1
        if not(monster.isProne):
            monster.tempCOR += monster._COR
    
    if (monster.isPetrified):
        monster.isPetrified -= 1
        if not(monster.isPetrified):
            monster.tempSTR += 2
            monster.tempEND += 2
            monster.tempCOR += 2
            monster.tempDEX += 2
            monster.tempINT += 2
            monster.tempNOU += 2
            monster.tempWIL += 2

    if (monster.isPanicked):
        monster.isPanicked -= 1
        if not(monster.isPanicked):
            monster.tempSTR += 5
            monster.tempCOR += 5
    
    if (monster.isLevitated):
        monster.isLevitated -= 1

    if (monster.isImmobilised):
        monster.isImmobilised -= 1

    if (monster.isEncouraged):
        monster.isEncouraged -= 1
        if not(monster.isEncouraged):
            monster.tempSTR -= 1
            monster.tempEND -= 1
            monster.tempCOR -= 1
            monster.tempDEX -= 1
            monster.tempINT -= 1
            monster.tempNOU -= 1
            monster.tempWIL -= 1

    if (monster.isDoppelgangered):
        monster.isDoppelgangered -= 1

    if (monster.isDisarmed):
        monster.isDisarmed -= 1

    if (monster.isClumsy):
        monster.isClumsy -= 1
        if not(monster.isClumsy):
            monster.tempCOR += (monster._COR/2)

    if (monster.isCharmed):
        monster.isCharmed -= 1


    if (monster.isBlocking):
        monster.isBlocking -= 1
        if not(monster.isBlocking):
            monster.ARM -= monster.baseARM

class Die():
    def __init__(self, sides):
        self.sides = sides
    def roll(self):
        return random.randint(1,self.sides)


class Ability():
    def __init__(self, name, AP, target, range, success, contest):
        
        self.name = name
        self.AP = AP
        self.target = target
        self.range = range
        self.success = success
        self.contest = contest

class BuffAbility(Ability):
    def __init__(self, name, AP, target, range, success, contest, duration, effect):
      super().__init__(name, AP, target, range, success, contest)
      self.duration = duration
      self.effect = effect

    def onSuccess(self, monster):
        match self.effect:
            case 'BLOCK':
                monster.armour *= 2
                monster.blocking = D4+1
            case 'BLOCK 2':
                monster.armour *= 2
                monster.blocking = D8+1


# the code speaks for itself




Block2 = BuffAbility('BLOCK 2', 2, 'self', 0, 'END', 25, 8, 'BLOCK')


class DebuffAbility(Ability):
    def __init__(self, name, AP, target, range, success, contest, duration, effect):
      super().__init__(name, AP, target, range, success, contest)

class MeleeAbility(Ability):
    def __init__(self, name, AP, target, range, success, contest):
        super().__init__(name, AP, target, range, success, contest)

class RangedAbility(Ability):
    def __init__(self, name, AP, target, range, success, contest):
        super().__init__(name, AP, target, range, success, contest)



# def constructAbilties():
#     for ability in abilityList:
#         if ability not in uniqueAbilityList:
#             uniqueAbilityList.append(Ability(ability))

def constructFighters():
    for i in chosenList:
        primedList.append(Creature(i))

def rollInitiative():
    for monster, team in zip(primedList, teamList):
        monster.INIT = monster._COR + D20
        monster.TEAM = team
    primedList.sort(key=operator.attrgetter('INIT'),reverse=True)

def beginCombatLoop(monList):
    for monster in monList:
        monster.moved = False
        monster.attacked = False
       # if (!monster.target):
          #  findTar(monster, monList)
        
            


# def findTar(monster, list):
#     monster.target = random.choice(list)
#     while (monster.target.charmed)
#         monster.target = random.choice(list)


def attackmove(cr1, cr2, ability):
    D20 + ability.stat
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

    D20 = Die(20)
    D12 = Die(12)
    D10 = Die(10)
    D8 = Die(8)
    D6 = Die(6)
    D4 = Die(4)

    constructFighters()
    rollInitiative()
    beginCombatLoop(primedList)

    for monster in primedList:
        print ('\n', monster.printName)
        print ('Initiative:', monster.INIT)
        print ('Team:', monster.TEAM)
        print ('HP:', monster.curHP)
        print ('AP', monster.AP)
        print ('Abilities: ', monster.abilities)
        

        

# def beginCombat(fightDict, ):
#     Skeleton = Creature("meleeSkeleton", "Skeleton")
#     #roll initiative
#     for each in fightDict:
#         random.randint(1,20) + fightDict.


# print(Skeleton.curHP)

# takeDam(Skeleton, 45)

# print(Skeleton.curHP)