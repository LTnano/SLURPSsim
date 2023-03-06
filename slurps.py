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



# chosenList = ['thinBilly', 'bossSkeleton', 'wizardKobold', 'wizardKobold', 'rangedSkeletonH', 'giantRat']
# teamList = [1, 1, 2, 1, 2, 2]
chosenList = ['thinBilly', 'giantRat', 'meleeSkeleton', 'giantRat', 'giantRat', 'meleeSkeleton', 'giantRat', 'giantRat', 'meleeSkeleton']
teamList = [1, 2, 2, 1, 2, 2, 1, 1, 1]
primedList = []
aliveList = []
deadList = []
uniqueAbilityList = []
allAbilities = []

class Creature():
    def __init__(self, type):
        
        #name for logs
        self.printName = creatureDict[type]['Name']

        #variables
        self.INIT = 0
        self._curHP = creatureDict[type]['HP']
        self._tempHP = 0
        self.isAlive = True
        self.target = None
        self.targetAlly = None

        #stats
        self._HP = creatureDict[type]['HP'] #creature default max
        self._maxHP = creatureDict[type]['HP'] #flexible max
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
        self.isFortified = 0
        self.isImmobilised = 0
        self.isLevitated = 0
        self.isPanicked = 0
        self.isPetrified = 0
        self.isProne = 0
        self.isScared = 0
        self.isStunned = 0
        #notick status effects
        self.isSharpened = 0
        self.isTightened = 0        
        

        #equip assignment
        match creatureDict[type]['WEA']:
            case 20:
                self._WEA = D20
            case 12:
                self._WEA = D12
            case 10:
                self._WEA = D10
            case 8:
                self._WEA = D8
            case 6:
                self._WEA = D6
            case 4:
                self._WEA = D4
            case _:
                self._WEA = 0
        self.modWEA = 0
        match creatureDict[type]['RWEA']:
            case 20:
                self._RWEA = D20
            case 12:
                self._RWEA = D12
            case 10:
                self._RWEA = D10
            case 8:
                self._RWEA = D8
            case 6:
                self._RWEA = D6
            case 4:
                self._RWEA = D4
            case _:
                self._RWEA = 0
        self.modRWEA = 0
        self.ARM = creatureDict[type]['ARM']
        self.baseARM = creatureDict[type]['ARM']

        #ability logic
        self.AP = creatureDict[type]['AP']
        self._maxAP = creatureDict[type]['AP']
        self.abilities = hasAbilityDict[type]
        self.prioList = []

    def kill(self):
        self.isAlive = False
        print (f"{self.printName} died!")

    def takeDamage(self, damage):
        self._curHP = self._curHP - damage
        self.isStunned = 0
        return
    
    def takeHealing(self, healing):
        if (self._curHP + healing < self._maxHP):
            self._curHP = self._curHP + healing
            return
        self._curHP = self._maxHP
        return

    #randomly select an ability
    def chooseAbility(self):
        return random.choice(self.abilities)
    
    #choose an enemy 
    def chooseTarget(self, aliveList):
        if self.TEAM == 1:
            opposition = 2
        else:
            opposition = 1
        if self.target is None:
            self.target = random.choice(primedList)
            return
        if opposition in aliveList:
            while ((opposition == self.TEAM) or (self.target.isAlive == False)):
                self.target = random.choice(primedList)
        else:
            return
        #print (self.target.printName, self.target.TEAM, ' - ', self.printName, self.TEAM)

    #chooses an ally from own team
    def chooseAlly(self, aliveList):
        if self.TEAM == 1:
            allies = 1
        else:
            allies = 2
        if self.targetAlly is None:
            self.targetAlly = random.choice(primedList)
            return
        if allies in aliveList:
            while ((allies != self.TEAM) or (self.targetAlly.isAlive == False)):
                self.targetAlly = random.choice(primedList)
        else:
            return
        
    #uses selected ability  
    def useAbility(self, ability):
        for option in allAbilities:
            if option.name == ability:
                option.use(self, self.target, self.targetAlly)
                print (f"{self.printName} used {option.name}")

    #stat methods, returns stat + temp stat
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

    if (monster.isFortified):
        monster.isFortified -= 1
        if not(monster.isFortified):
            monster._maxHP = monster._HP
            monster._curHP = monster._curHP - monster._tempHP
            monster._tempHP = 0
            if (monster._curHP > monster._maxHP):
                monster._curHP = monster._maxHP
            if (monster._curHP <= 0):
                monster.isAlive = False

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
    def __init__(self, sides, name):
        self.sides = sides
        self.name = name
    
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
        self.canCast = False
    
          
    def statSuccess(self, success, monster):
        match success:
            case 'STR':
                return monster.strength()
            case 'END':
                return monster.endurance()
            case 'COR':
                return monster.coordination()
            case 'DEX':
                return monster.dexterity()
            case 'INT':
                return monster.intelligence()
            case 'NOU':
                return monster.nouse()
            case 'WIL':
                return monster.will()
            case _:
                return 0
    
    def use(self, caster, target, targetAlly):
        caster.AP -= self.AP
        armour = 0
        ignoreARM = False
        if hasattr(self, 'ignoreARM'):
            ignoreARM = self.ignoreARM
        successBonus = self.statSuccess(self.success, caster)
        match self.target:
            case 'ally'| 'self':
                if (D20.roll() + successBonus >= self.contest):
                    self.onSuccess(caster, targetAlly)
            case 'enemy':
                successContest = self.statSuccess(self.contest, target)
                if not (ignoreARM):
                    armour = target.ARM
                if (D20.roll() + successBonus >= D20.roll() + successContest + armour):
                    self.onSuccess(caster, target)
                else:
                    print (f"{caster.printName} missed {target.printName}")
        
        
             

        
class BuffAbility(Ability): #block 1 2, dead man walking 1 2, dodge, doppelganger, encourage, extra action 1 2, extra shot, heal 1 2 3, levitate, play dead 1 2, sharpen, tighten, turn, vault, weighten
    def __init__(self, name, AP, target, range, success, contest):
      super().__init__(name, AP, target, range, success, contest)
      self.effect = name

    def onSuccess(self, caster, target):
        match self.effect:
            case 'BLOCK':
                caster.ARM *= 2
                caster.isBlocking = D4.roll()+1
            case 'BLOCK 2':
                caster.ARM *= 2
                caster.isBlocking = D8.roll()+1
            case 'DEAD MAN WALKING':
                caster._tempHP += 20
                caster._curHP += 20
                caster._maxHP += 20
                caster.isFortified = D4.roll()+1
            case 'DEAD MAN WALKING 2':
                caster._tempHP += 30
                caster._curHP += 30
                caster._maxHP += 30
                caster.isFortified = D8.roll()+1
            case 'DEATH THROES': # need to be worked in to death
                #for monster in primedList:
                   # if monster.TEAM != caster.TEAM:
                pass
            case 'DOPPELGANGER':
                caster.isDoppelgangered = D8.roll()+1
            case 'ENCOURAGE':
                target.tempSTR += 1
                target.tempEND += 1
                target.tempCOR += 1
                target.tempDEX += 1
                target.tempINT += 1
                target.tempNOU += 1
                target.tempWIL += 1
                target.isEncouraged = D4.roll()+1
            case 'EXTRA ACTION':
                pass
            case 'EXTRA ACTION 2':
                pass
            case 'EXTRA SHOT':
                pass
            case 'HEAL':
                healval = caster.dexterity() * D6.roll()
                target.takeHealing(healval)
            case 'HEAL 2':
                healval = caster.dexterity() * (D6.roll() + 4)
                target.takeHealing(healval)
            case 'HEAL 3':
                healval = caster.dexterity() * (D12.roll() + 4)
                target.takeHealing(healval)
            case 'PLAY DEAD':
                pass
            case 'PLAY DEAD 2':
                pass
            case 'ROUSING SHOUT':
                for ally in primedList:
                    if caster.team == ally.team:
                        ally.tempSTR += 1
                        ally.tempEND += 1
                        ally.tempCOR += 1
                        ally.tempDEX += 1
                        ally.tempINT += 1
                        ally.tempNOU += 1
                        ally.tempWIL += 1
                        ally.isEncouraged = D4.roll()+1
            case 'ROUSING SONG':
                for ally in primedList:
                    if caster.team == ally.team:
                        ally.AP = ally._maxAP
            case 'SHARPEN':
                caster.isSharpened = 1
                caster.modWEA += 1
            case 'TIGHTEN':
                caster.isTightened = 1
                caster.modRWEA += 1
                        

class DebuffAbility(Ability):
    def __init__(self, name, AP, target, range, success, contest, duration, effect):
      super().__init__(name, AP, target, range, success, contest)

class MeleeAbility(Ability):
    def __init__(self, name, AP, target, range, success, contest, damstat, ignoreARM):
        super().__init__(name, AP, target, range, success, contest)
        self.damStat = damstat
        self.ignoreARM = ignoreARM
    def onSuccess(self, caster, target):
        match self.name:
            case 'BACKSTAB':#behind implementation might not ever exist (even more OP)
                dieroll = caster._WEA.roll()
                totaldamage = dieroll * self.damageStat(caster, self.damStat)
                target.takeDamage(totaldamage)
                print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
            case 'DISARM':
                disarmDuration = D4.roll() + 1
                if target.isDisarmed < disarmDuration:
                    target.isDisarmed = disarmDuration
                print (f"{caster.printName} hit and disarmed {target.printName} for {target.isDisarmed} rounds")
            case 'FEINT':
                dieroll = caster._WEA.roll()
                totaldamage = (dieroll + 1) * self.damageStat(caster, self.damStat)
                target.takeDamage(totaldamage)
                print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
            case 'FEINT 2':
                dieroll = caster._WEA.roll()
                totaldamage = (dieroll + 2) * self.damageStat(caster, self.damStat)
                target.takeDamage(totaldamage)
                print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
            case 'FEINT 3':
                dieroll = caster._WEA.roll()
                totaldamage = (dieroll + 3) * self.damageStat(caster, self.damStat)
                target.takeDamage(totaldamage)
                print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
            case 'FLATTEN':
                effectDuration = D6.roll() + 4
                if target.isProne < effectDuration:
                    target.isProne = effectDuration
                if target.isStunned < effectDuration:
                    target.isStunned = effectDuration
                print (f"{caster.printName} flattened {target.printName} for {target.isProne} rounds")
            case 'GAROTTE': #garotte weapon?? (status effect) maybe)
                pass
            case 'KNOCK BACK': # needs movement implementation
                print (f"{caster.printName} hit {target.printName} and knocked them back!")
            case 'KNOCK BACK 2': # needs movement implementation
                target.takeDamage(20)
                print (f"{caster.printName} hit {target.printName} for {20} damage and knocked them back far!")
            case 'KNOCK BACK 3': # needs movement implementation
                target.takeDamage(60)
                print (f"{caster.printName} hit {target.printName} for {60} damage and knocked them back very far!")
            case 'KNOCK OVER':
                proneDuration = D4.roll() + 1
                if target.isProne < proneDuration:
                    target.isProne = proneDuration
                print (f"{caster.printName} hit and knocked {target.printName} over for {target.isProne} rounds")
                pass
            case 'OFF-HAND ATTACK': # needs multiple weapon implementation
                pass
            case 'PIERCING THRUST':
                dieroll = caster._WEA.roll()
                totaldamage = (dieroll + 2) * self.damageStat(caster, self.damStat)
                target.takeDamage(totaldamage)
                print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
            case 'SPLIT ATTACK': # needs multiple weapon implementation
                pass
            case 'STRIKE':
                dieroll = caster._WEA.roll()
                totaldamage = dieroll * self.damageStat(caster, self.damStat)
                target.takeDamage(totaldamage)
                print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
            case 'STUN':
                stunDuration = D4.roll() + 1
                if target.isStunned < stunDuration:
                    target.isStunned = stunDuration
                print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
            case 'STUN 2':
                stunDuration = D4.roll() + 3
                if target.isStunned < stunDuration:
                    target.isStunned = stunDuration
                print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
            case 'STUN 3':
                stunDuration = D6.roll() + 6
                if target.isStunned < stunDuration:
                    target.isStunned = stunDuration
                print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
            case _:
                pass
        return
    def damageStat(self, monster, damStat):
        match damStat:
            case 'STR':
                return monster.strength()
            case 'END':
                return monster.endurance()
            case 'COR':
                return monster.coordination()
            case 'DEX':
                return monster.dexterity()
            case 'INT':
                return monster.intelligence()
            case 'NOU':
                return monster.nouse()
            case 'WIL':
                return monster.will()
            case _:
                return 1

class RangedAbility(Ability):
    def __init__(self, name, AP, target, range, success, contest):
        super().__init__(name, AP, target, range, success, contest)

#BUFF ABILITIES

allAbilities.append(BuffAbility('BLOCK', 1, 'self', 0, 'END', 20))
allAbilities.append(BuffAbility('BLOCK 2', 2, 'self', 0, 'END', 25))
allAbilities.append(BuffAbility('DEAD MAN WALKING', 2, 'self', 0, 'END', 20))
allAbilities.append(BuffAbility('DEAD MAN WALKING 2', 3, 'self', 0, 'END', 25))
#death throes
#doppelganger*
allAbilities.append(BuffAbility('ENCOURAGE', 1, 'ally', 0, 'END', 0))
#extraaction*
#extraction2*
#extrashot*
allAbilities.append(BuffAbility('HEAL', 1, 'ally', 1, 'NOU', 20))
allAbilities.append(BuffAbility('HEAL 2', 2, 'ally', 1, 'NOU', 22))
allAbilities.append(BuffAbility('HEAL 3', 4, 'ally', 1, 'NOU', 24))
allAbilities.append(BuffAbility('SHARPEN', 1, 'ally', 0, 'END', 0))
allAbilities.append(BuffAbility('TIGHTEN', 1, 'ally', 0, 'END', 0))
allAbilities.append(BuffAbility('SHARPEN', 1, 'ally', 0, 'END', 0))


#MELEE ABILITIES

allAbilities.append(MeleeAbility('BACKSTAB', 1, 'enemy', 1, 'COR', 'NA', 'COR', False))
allAbilities.append(MeleeAbility('DISARM', 3, 'enemy', 1, 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('FEINT', 1, 'enemy', 1, 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FEINT', 2, 'enemy', 1, 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FEINT', 3, 'enemy', 1, 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FLATTEN', 4, 'enemy', 1, 'STR', 'COR', 'NA', False))
#garotte
allAbilities.append(MeleeAbility('KNOCK BACK', 1, 'enemy', 1, 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK BACK 2', 2, 'enemy', 1, 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK BACK 3', 3, 'enemy', 1, 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK OVER', 2, 'enemy', 1, 'STR', 'COR', 'NA', True))
#off-hand attack
allAbilities.append(MeleeAbility('PIERCING THRUST', 2, 'enemy', 1, 'STR', 'NA', 'STR', False))
#split attack
allAbilities.append(MeleeAbility('STUN', 1, 'enemy', 1, 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('STUN 2', 2, 'enemy', 1, 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('STUN 3', 3, 'enemy', 1, 'STR', 'COR', 'NA', True))


def constructFighters():
    primedList.clear()
    aliveList.clear()
    deadList.clear()
    for i in chosenList:
        primedList.append(Creature(i))

def rollInitiative():
    for monster, team in zip(primedList, teamList):
        monster.INIT = monster._COR + D20.roll()
        monster.TEAM = team
    primedList.sort(key=operator.attrgetter('INIT'),reverse=True)

def beginCombatLoop(monList):
    aliveList = teamList.copy()
    print (f"{aliveList} : {teamList}")
    combatRound = 1
    while (aliveList.count(1) > 0 and aliveList.count(2) > 0):
        print (f"Round {combatRound} Alive List:{aliveList}")
        for monster in monList:
            if (monster.isAlive):
                statusTicker(monster)
                monster.chooseTarget(aliveList)
                monster.chooseAlly(aliveList)
                monster.useAbility(monster.chooseAbility())
                if (monster.target._curHP <= 0):
                    deadList.insert(-1, monster.target.printName)
                    aliveList.remove(monster.target.TEAM)
                    monster.target.kill()
            if (aliveList.count(1) == 0 or aliveList.count(2) == 0):
                break
        combatRound += 1
    print (f"Combat Ended! Team {aliveList} won!") 



if __name__ == '__main__':

    D20 = Die(20, 'D20')
    D12 = Die(12, 'D12')
    D10 = Die(10, 'D10')
    D8 = Die(8, 'D8')
    D6 = Die(6, 'D6')
    D4 = Die(4, 'D4')
    
    
    varianceMinimizer = 10
    cycleloop = 0

    while cycleloop < varianceMinimizer:
        constructFighters()
        rollInitiative()
        beginCombatLoop(primedList)
        cycleloop += 1

    for monster in primedList:
        print ('\n', monster.printName)
        print ('Initiative:', monster.INIT)
        print ('Team:', monster.TEAM)
        print ('HP:', monster._curHP)
        print ('AP', monster.AP)
        print ('Abilities: ', monster.abilities)
        

