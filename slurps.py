import pickle
import random
import wx
import operator
import os
import time
#import math



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
chosenList = ['testMonster', 'giantRat', 'giantRat','giantRat', 'giantRat', 'giantRat', 'giantRat','giantRat', 'giantRat', 'giantRat', 'giantRat','giantRat', 'giantRat', 'giantRat', 'giantRat','giantRat', 'giantRat', 'giantRat', 'giantRat','giantRat', 'giantRat', 'giantRat', 'giantRat','giantRat', 'giantRat', 'giantRat', 'giantRat','giantRat', 'giantRat', 'giantRat', 'giantRat','giantRat', 'giantRat']
teamList = [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
primedList = []
uniqueAbilityList = []
allAbilities = []
combatRoundList = []
winrateList = []
avgCombatdur = 3.5
ffEnabled = True

def takeSecond(elem):
    return elem[1]

def numberDuplicates(monsterlist):
    seen = {}
    for monster in monsterlist:
        key = str(monster.printName)
        if key in seen:
            seen[key] += 1
            monster.printName += " " + str(seen[key]+1)
        else:
            seen[key] = 0

class CombatLog:
    def __init__(self, filename, logdir):
        self.filename = filename
        self.log = []
        self.logdir = logdir
        if not os.path.exists(logdir):
            os.mkdir(logdir)
    
    def record(self, event):
        fevent = event + "\n"
        self.log.append(fevent)
        
    def writeFile(self):
        filename = time.strftime('%Y%m%d%H%M%S_combat_log.txt')
        filepath = os.path.join(self.logdir, filename)
        with open(filepath, 'w') as f:
            for event in self.log:
                f.write(event)

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
        self.hasHeadache = 0
        self.headacheSeverity = 0
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
                self._WEA = D0
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
                self._RWEA = D0
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
        if logEvents:
            cLog.record(f"{self.printName} died!")

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

    def healWeighting(self, healing):
        if (self._maxHP/(self._curHP + healing) > 1.5):
            return self._maxHP/(self._curHP + healing)
        else:
            return 0.5
        
        #return self._maxHP / (1 + (self._curHP / self._maxHP)**2 * math.exp(-(self._maxHP - self._curHP) / self._maxHP) * healing)
    
    def checkAbility(self):
        weightingList = []
        for ability in self.abilities:
            for realability in allAbilities:
                weighting = self.setPriority(realability, ability)
                if not weighting == None:
                    weightingList.append(int(weighting))
        self.prioList = list(zip(self.abilities, weightingList))
        print (f"{self.prioList}")
        self.prioList.sort(key=takeSecond)
        print (f"{self.prioList}")


    def hitChance(self, successBonus, successContest):
        roll = 1
        while roll <= 100:
            if (successBonus+roll >= successContest):
                return (1 - ((roll-1)/20))
            roll +=1

    def setPriority(self, realability, ability):
        if realability.name == ability:
            match realability.target:
                case 'enemy':
                    successBonus = realability.statSuccess(realability.success, self)
                    successContest = realability.statSuccess(realability.contest, self.target) + D20.average()
                    weighting = self.hitChance(successBonus, successContest) * realability.onSuccess(self, self.target, True)
                case 'ally'|'self':
                    successBonus = realability.statSuccess(realability.success, self) + D20.average()
                    successContest = realability.statSuccess(realability.contest, self.target) + D20.average()
                    weighting = self.hitChance(successBonus, successContest) * realability.onSuccess(self, self.target, True)
            return weighting

    

        #check the damage of the ability based on monsters stats
        #check the health of allies and increase

    def chooseAbility(self):
        #return random.choice(self.abilities)
        return self.prioList[-1][0]    
            
    #choose an enemy 
    def chooseTarget(self):
        if self.TEAM == 1:
            opposition = 2
            print (f"Opposition = {opposition}")
        else:
            opposition = 1
            print (f"Opposition = {opposition}")
        if self.target is None:
            self.target = random.choice(primedList)
            print (f"Choosing target because target should be None - Target = {self.target}")
        if opposition in simState.aliveList:
            while ((self.target.TEAM == self.TEAM) or (self.target.isAlive == False)):
                print (f"Choosing target because target is on my team {self.target.TEAM == self.TEAM} and/or target is dead {self.target.isAlive == False}")
                self.target = random.choice(primedList)
                print (f"{self.printName}(team {self.TEAM})'s target = {self.target.printName}(team {self.target.TEAM})")
        else:
            print (f"No enemies remain")
            return
        print (f"No change needed as target valid = {(self.target.TEAM != self.TEAM and self.target.isAlive == True)}")
        #print (self.target.printName, self.target.TEAM, ' - ', self.printName, self.TEAM)

    #chooses an ally from own team
    def chooseAlly(self):
        if self.TEAM == 1:
            allies = 1
        else:
            allies = 2
        if self.targetAlly is None:
            self.targetAlly = random.choice(primedList)
        if allies in simState.aliveList:
            while ((self.targetAlly.TEAM != self.TEAM) or (self.targetAlly.isAlive == False)):
                self.targetAlly = random.choice(primedList)
        else:
            return
        
    #uses selected ability  
    def useAbility(self, ability):
        for option in allAbilities:
            if option.name == ability:
                print (f"{self.printName} used {option.name}")
                if logEvents:
                    cLog.record(f"{self.printName} used {option.name}")
                option.use(self, self.target, self.targetAlly)
                

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

    def statAverage(self):
        return (self.strength() + self.coordination() + self.endurance() + self.intelligence() + self.nouse() + self.will())/7
    
class SimState():
    def __init__(self):
        self.aliveList = []
        self.deadList = []

def checkDeath(monster):
    if monster.isAlive:
        if (monster._curHP <= 0):
            simState.deadList.insert(-1, monster.printName)
            simState.aliveList.remove(monster.TEAM)
            monster.kill()

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
            monster._maxHP += 10

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
            monster._maxHP += 20

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
            monster._maxHP -= 10

    if (monster.isFortified):
        monster.isFortified -= 1
        if not(monster.isFortified):
            monster._maxHP = monster._HP
            monster._curHP = monster._curHP - monster._tempHP
            monster._tempHP = 0
            
    if (monster.isDoppelgangered):
        monster.isDoppelgangered -= 1

    if (monster.isDisarmed):
        monster.isDisarmed -= 1
        #set dice back to original weapon die (need to add to creature class)

    if (monster.isClumsy):
        monster.isClumsy -= 1
        if not(monster.isClumsy):
            monster.tempCOR += (monster._COR/2)

    if (monster.isBlocking):
        monster.isBlocking -= 1
        if not(monster.isBlocking):
            monster.ARM -= monster.baseARM
    
    if (monster._curHP > monster._maxHP):
        monster._curHP = monster._maxHP

    checkDeath(monster)

class Die():
    def __init__(self, sides, name):
        self.sides = sides
        self.name = name
    
    def roll(self):
        return random.randint(1,self.sides)
    
    def average(self):
        return (self.sides+1)/2


class Ability():
    def __init__(self, name, AP, target, success, contest):
        
        self.name = name
        self.AP = AP
        self.target = target
        #self.range = range
        self.success = success
        self.contest = contest

    def combatDurWeighting(self, effectdur):
        if avgCombatdur <= effectdur:
            return effectdur/avgCombatdur
        return 1  

    def canCast(self, caster):
        if caster.AP >= self.AP:
            return True
        return False
    
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
                return 1
            
    def use(self, caster, target, targetAlly):
        caster.AP -= self.AP
        armour = 0
        range = 0
        ignoreARM = False
        if hasattr(self, 'ignoreARM'):
            ignoreARM = self.ignoreARM
        if hasattr(self, 'ranged'):
            range = self.ranged
        successBonus = self.statSuccess(self.success, caster)
        match self.target:
            case 'ally'| 'self':
                if (D20.roll() + successBonus >= self.contest):
                    self.onSuccess(caster, targetAlly, False)
                else:
                    if logEvents:
                        cLog.record(f"{caster.printName} failed to cast {self.name}")
            case 'enemy':
                successContest = self.statSuccess(self.contest, target)
                if not (ignoreARM):
                    armour = target.ARM
                if not (range):
                    if (D20.roll() + successBonus >= D20.roll() + successContest + armour):
                        target.takeDamage(self.onSuccess(caster, target, False))
                    else:
                        print (f"{caster.printName} missed {target.printName}")
                        if logEvents:
                            cLog.record(f"{caster.printName} missed {target.printName}")
                else:
                    if (D20.roll() + successBonus >= self.contest + range + armour):
                        target.takeDamage(self.onSuccess(caster, target, False))
                    else:
                        print (f"{caster.printName} missed {target.printName}")
                        if logEvents:
                            cLog.record(f"{caster.printName} missed {target.printName}")
        
          
class BuffAbility(Ability): #block 1 2, dead man walking 1 2, dodge, doppelganger, encourage, extra action 1 2, extra shot, heal 1 2 3, levitate, play dead 1 2, sharpen, tighten, turn, vault, weighten
    def __init__(self, name, AP, target, success, contest):
      super().__init__(name, AP, target, success, contest)
      self.effect = name

    def onSuccess(self, caster, target, test):
        abilityweight = 0
        match self.effect:

            case 'BLOCK':
                if not test:
                    caster.ARM *= 2
                    caster.isBlocking = D4.roll()+1
                    if logEvents:
                        cLog.record(f"{caster.printName} starts blocking for {caster.isBlocking} rounds!")
                if test:
                    if self.canCast(caster):
                        if not caster.isBlocking:
                            abilityweight =  (caster.ARM * 2 * D4.average()) / self.combatDurWeighting(D4.average()+1)
                        else:
                            abilityweight = 0
                    

            case 'BLOCK 2':
                if not test:
                    caster.ARM *= 2
                    caster.isBlocking = D8.roll()+1
                    if logEvents:
                        cLog.record(f"{caster.printName} starts blocking for {caster.isBlocking} rounds! Raising their armour to {caster.ARM}")
                if test:
                    if self.canCast(caster):
                        if not (caster.isBlocking):
                            abilityweight =  (caster.ARM * 2 * D8.average()) / self.combatDurWeighting(D8.average()+1)
                        else:
                            abilityweight = 0
                    

            case 'DEAD MAN WALKING':
                if not test:
                    caster._tempHP += 20
                    caster._curHP += 20
                    caster._maxHP += 20
                    caster.isFortified = D4.roll()+1
                    if logEvents:
                        cLog.record(f"{caster.printName} is a dead man walking for {caster.isFortified} rounds!")
                if test:
                    if self.canCast(caster):
                        if not (caster.isFortified):
                            abilityweight = (15 * D4.average()+1) / self.combatDurWeighting(D4.average()+1) * caster.healWeighting(20)
                            #half of current HP + quarter of maxHP increase * average rounds of effect
                            #divided by the combat duration weighting
                            #multiplied by the heal weighting    
                        else:
                            abilityweight = 0
                    

            case 'DEAD MAN WALKING 2':
                if not test:
                    caster._tempHP += 30
                    caster._curHP += 30
                    caster._maxHP += 30
                    caster.isFortified = D8.roll()+1
                    if logEvents:
                        cLog.record(f"{caster.printName} is a very dead man walking for {caster.isFortified} rounds!")
                if test:
                    if self.canCast(caster):
                        if not (caster.isFortified):
                            abilityweight = (25 * D8.average()+1) / self.combatDurWeighting(D8.average()+1) * caster.healWeighting(30)  
                        else:
                            abilityweight = 0
                    

            case 'DEATH THROES': # need to be worked in to death
                #for monster in primedList:
                   # if monster.TEAM != caster.TEAM:
                pass

            case 'DOPPELGANGER':
                if not test:
                    caster.isDoppelgangered = D8.roll()+1
                if test:
                    if self.canCast(caster):
                        abilityweight = 0

            case 'ENCOURAGE':
                if not test:
                    target.tempSTR += 1
                    target.tempEND += 1
                    target.tempCOR += 1
                    target.tempDEX += 1
                    target.tempINT += 1
                    target.tempNOU += 1
                    target.tempWIL += 1
                    target._maxHP += 10
                    encourageDuration = D4.roll()+1
                    if target.isEncouraged < encourageDuration:
                        target.isEncouraged = encourageDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} encouraged {target.printName} for {target.isEncouraged} rounds!")
                if test:
                    if self.canCast(caster):
                        if not (target.isEncouraged):
                            abilityweight = (9.5 * D4.average()+1) / self.combatDurWeighting(D4.average()+1)
                            #half of current HP + quarter of maxHP increase + (temp stats * 10 / 2) * average rounds of effect
                            #divided by the combat duration weighting
                            #multiplied by the heal weighting    
                        else:
                            abilityweight = 0

            case 'EXTRA ACTION':
                pass

            case 'EXTRA ACTION 2':
                pass

            case 'EXTRA SHOT':
                pass

            case 'HEAL':
                if not test:
                    healval = caster.dexterity() * D6.roll()
                    target.takeHealing(healval)
                    if logEvents:
                        cLog.record(f"{caster.printName} healed {caster.targetAlly.printName} for {healval}!")
                if test:
                    if self.canCast(caster):
                        healval = caster.dexterity() * (D6.average())
                        abilityweight = (healval / 2) * target.healWeighting(healval)  

            case 'HEAL 2':
                if not test:
                    healval = caster.dexterity() * (D6.roll() + 4)
                    target.takeHealing(healval)
                    if logEvents:
                        cLog.record(f"{caster.printName} healed {caster.targetAlly.printName} for {healval}! They have {caster.targetAlly._curHP} remaining")
                if test:
                    if self.canCast(caster):
                        healval = caster.dexterity() * (D6.average() + 4)
                        abilityweight = (healval / 2) * target.healWeighting(healval)  

            case 'HEAL 3':
                if not test:
                    healval = caster.dexterity() * (D12.roll() + 4)
                    target.takeHealing(healval)
                    if logEvents:
                        cLog.record(f"{caster.printName} healed on {caster.targetAlly.printName} for {healval}!")
                if test:
                    if self.canCast(caster):
                        healval = caster.dexterity() * (D12.average() + 4)
                        abilityweight = (healval / 2) * target.healWeighting(healval)  

            case 'PLAY DEAD':
                pass

            case 'PLAY DEAD 2':
                pass

            case 'ROUSING SHOUT':
                if not test:
                    encourageDuration = D4.roll()+1
                    for ally in primedList:
                        if caster.TEAM == ally.TEAM:
                            if not ally.isEncouraged:
                                ally.tempSTR += 1
                                ally.tempEND += 1
                                ally.tempCOR += 1
                                ally.tempDEX += 1
                                ally.tempINT += 1
                                ally.tempNOU += 1
                                ally.tempWIL += 1
                                ally._maxHP += 10
                            if ally.isEncouraged < encourageDuration:
                                ally.isEncouraged = encourageDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} encourages their whole team for {encourageDuration} rounds!")
                if test:
                    if self.canCast(caster):
                        for ally in primedList:
                            if caster.TEAM == ally.TEAM:
                                if not ally.isEncouraged:
                                    abilityweight = abilityweight + (9.5 * D4.average()+1) / self.combatDurWeighting(D4.average()+1)
                            #half of current HP + quarter of maxHP increase * average rounds of effect
                            #divided by the combat duration weighting
                            #multiplied by the heal weighting    

            case 'ROUSING SONG':
                if not test:
                    for ally in primedList:
                        if caster.TEAM == ally.TEAM:
                            ally.AP = ally._maxAP
                    if logEvents:
                        cLog.record(f"{caster.printName} rouses their team with a song, resoring all AP!")
                if test:
                    if self.canCast(caster):
                        for ally in primedList:
                            if caster.TEAM == ally.TEAM:
                                abilityweight = abilityweight + (ally._maxAP/(ally.AP+1)) * (ally.statAverage())
                    
            case 'SHARPEN':
                if not test:
                    caster.isSharpened = 1
                    caster.modWEA += 1
                if logEvents:
                        cLog.record(f"{caster.printName} enhances their weapon!")
                if test:
                    if self.canCast(caster):
                        abilityweight = avgCombatdur*self.statSuccess(self.damStat, caster)

            case 'TIGHTEN':
                if not test:
                    caster.isTightened = 1
                    caster.modRWEA += 1
                if logEvents:
                        cLog.record(f"{caster.printName} enhances their weapon!")
                if test:
                    if self.canCast(caster):
                        abilityweight = avgCombatdur*self.statSuccess(self.damStat, caster)

        return abilityweight        

class DebuffAbility(Ability):
    def __init__(self, name, AP, target, success, contest, duration, effect):
      super().__init__(name, AP, target, success, contest)

class MeleeAbility(Ability):
    def __init__(self, name, AP, target, success, contest, damstat, ignoreARM):
        super().__init__(name, AP, target, success, contest)
        self.damStat = damstat
        self.ignoreARM = ignoreARM
    def onSuccess(self, caster, target, test):
        totaldamage = 0
        match self.name:

            case 'BACKSTAB':#behind implementation might not ever exist (even more OP)
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)

            case 'DISARM':
                if not test:
                    disarmDuration = D4.roll() + 1
                    if target.isDisarmed < disarmDuration:
                        target.isDisarmed = disarmDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for and disarmed them for {disarmDuration} rounds!")
                    #need to set weapon die to D0
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
                #calculate the potential damage halved (basically healing)
                print (f"{caster.printName} hit and disarmed {target.printName} for {target.isDisarmed} rounds")
            
            case 'FEINT':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 1) * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 1) * self.statSuccess(self.damStat, caster)
            
            case 'FEINT 2':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
            
            case 'FEINT 3':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 3) * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 3) * self.statSuccess(self.damStat, caster)
            
            case 'FLATTEN':
                if not test:
                    effectDuration = D6.roll() + 4
                    if target.isProne < effectDuration:
                        target.isProne = effectDuration
                    if target.isStunned < effectDuration:
                        target.isStunned = effectDuration
                    print (f"{caster.printName} flattened {target.printName} for {target.isProne} rounds")
                    if logEvents:
                        cLog.record(f"{caster.printName} flattened {target.printName} for {target.isProne} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0 + 0
            
            case 'GAROTTE': #garotte weapon?? (status effect) maybe)
                pass
            #case 'KNOCK BACK': # needs movement implementation
                #print (f"{caster.printName} hit {target.printName} and knocked them back!")
            #case 'KNOCK BACK 2': # needs movement implementation
                #totaldamage = 20
                #print (f"{caster.printName} hit {target.printName} for {20} damage and knocked them back far!")
            #case 'KNOCK BACK 3': # needs movement implementation
               # totaldamage = 60
                #print (f"{caster.printName} hit {target.printName} for {60} damage and knocked them back very far!")
            
            case 'KNOCK OVER':
                if not test:
                    proneDuration = D4.roll() + 1
                    if target.isProne < proneDuration:
                        target.isProne = proneDuration
                    print (f"{caster.printName} hit and knocked {target.printName} over for {target.isProne} rounds")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and knocked {target.printName} over for {target.isProne} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
            
            case 'OFF-HAND ATTACK': # needs multiple weapon implementation
                pass
            
            case 'PIERCING THRUST':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
            
            case 'SPLIT ATTACK': # needs multiple weapon implementation
                pass
            
            case 'STRIKE':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
            
            case 'STUN':
                if not test:
                    stunDuration = D4.roll() + 1
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                    print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
            
            case 'STUN 2':
                if not test:
                    stunDuration = D4.roll() + 3
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                    print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
            
            case 'STUN 3':
                if not test:
                    stunDuration = D6.roll() + 6
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                    print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
            
            case _:
                pass

        return totaldamage

class RangedAbility(Ability):
    def __init__(self, name, AP, target, success, contest, damstat, ignoreARM, ranged):
        super().__init__(name, AP, target, success, contest)
        self.damStat = damstat
        self.ignoreARM = ignoreARM
        self.ranged = ranged
    def onSuccess(self, caster, target, test):
        totaldamage = 0
        match self.name:

            case 'CURSE OF CLUMSINESS':
                if not test:
                    clumDuration = D4.roll() + 1
                    if target.isClumsy < clumDuration:
                        target.tempCOR -= (target._COR/2)
                        target.isClumsy = clumDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and cursed {target.printName} for {target.isClumsy} rounds")
                    print (f"{caster.printName} hit and cursed {target.printName} for {target.isClumsy} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0

            case 'DOUBLE SHOT':
                if not test:
                    if logEvents:
                        cLog.record(f"")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
                print (f"")
            
            case 'FIREBALL':
                if not test:
                    dieroll = D4.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = D4.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
            
            case 'FIREBALL 2':
                if not test:
                    dieroll = D6.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = D6.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
            
            case 'FIREBALL 3':
                if not test:
                    dieroll = D8.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = D8.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
            
            case 'FIRESTORM':
                if not test:
                    totaldamage = 2 * self.statSuccess(self.damStat, caster)
                    if ffEnabled:
                        for monster in primedList:
                            if monster.isAlive:
                                monster.takeDamage(totaldamage)
                                #logging
                                if monster.TEAM == caster.TEAM:
                                    if monster == caster:
                                        print (f"{caster.printName} singed themselves for {totaldamage} damage")
                                        if logEvents:
                                            cLog.record(f"{caster.printName} singed themselves for {totaldamage} damage")
                                        checkDeath(monster)
                                    else:
                                        print (f"{caster.printName} singed their ally {monster.printName} for {totaldamage} damage")
                                        if logEvents:
                                            cLog.record(f"{caster.printName} singed their ally {monster.printName} for {totaldamage} damage")
                                        checkDeath(monster)
                                                                
                                elif monster == caster.target:
                                    print (f"{caster.printName} blasted {monster.printName} for {totaldamage*2} damage")
                                    if logEvents:
                                        cLog.record(f"{caster.printName} blasted {monster.printName} for {totaldamage*2} damage")
                                else:
                                    print (f"{caster.printName} singed {monster.printName} for {totaldamage} damage")
                                    if logEvents:
                                        cLog.record(f"{caster.printName} singed {monster.printName} for {totaldamage} damage")
                                    checkDeath(monster)
                    else:
                        for monster in primedList:
                            if monster.isAlive:
                                if monster.TEAM != caster.TEAM:
                                    monster.takeDamage(totaldamage)
                                    #logging
                                    if monster != target:
                                        print (f"{caster.printName} singed {monster.printName} for {totaldamage} damage")
                                        if logEvents:
                                            cLog.record(f"{caster.printName} singed {monster.printName} for {totaldamage} damage")
                                        checkDeath(monster)
                                    else:
                                        print (f"{caster.printName} blasted {monster.printName} for {totaldamage*2} damage")
                                        if logEvents:
                                            cLog.record(f"{caster.printName} blasted {monster.printName} for {totaldamage*2} damage")
                if test:
                    if self.canCast(caster):
                        damage = 2 * self.statSuccess(self.damStat, caster)
                        for monster in primedList:
                            if monster.isAlive:
                                if monster.TEAM != caster.TEAM:
                                    if monster != target:
                                        totaldamage = totaldamage + damage
                                    else:
                                        totaldamage = totaldamage + (damage*2)
                                else:
                                    totaldamage = totaldamage - (damage/2)
                        if (caster._curHP - damage <= 0):
                            print (caster._curHP)
                            totaldamage = totaldamage * 0
                        print (totaldamage)

            
            case 'GAROTTE': #garotte weapon?? (status effect) maybe)
                pass
            #case 'KNOCK BACK': # needs movement implementation
                #print (f"{caster.printName} hit {target.printName} and knocked them back!")
            #case 'KNOCK BACK 2': # needs movement implementation
                #totaldamage = 20
                #print (f"{caster.printName} hit {target.printName} for {20} damage and knocked them back far!")
            #case 'KNOCK BACK 3': # needs movement implementation
               # totaldamage = 60
                #print (f"{caster.printName} hit {target.printName} for {60} damage and knocked them back very far!")
            
            case 'KNOCK OVER':
                if not test:
                    proneDuration = D4.roll() + 1
                    if target.isProne < proneDuration:
                        target.isProne = proneDuration
                    print (f"{caster.printName} hit and knocked {target.printName} over for {target.isProne} rounds")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and knocked {target.printName} over for {target.isProne} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
            
            case 'OFF-HAND ATTACK': # needs multiple weapon implementation
                pass
            
            case 'PIERCING THRUST':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
            
            case 'SPLIT ATTACK': # needs multiple weapon implementation
                pass
            
            case 'STRIKE':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                    print (f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    dieroll = caster._WEA.average()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
            
            case 'STUN':
                if not test:
                    stunDuration = D4.roll() + 1
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                    print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    totaldamage = 0
            
            case 'STUN 2':
                if not test:
                    stunDuration = D4.roll() + 3
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                    print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    totaldamage = 0
            
            case 'STUN 3':
                if not test:
                    stunDuration = D6.roll() + 6
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                    print (f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    totaldamage = 0
            
            case _:
                pass
        return totaldamage
#BUFF ABILITIES

allAbilities.append(BuffAbility('BLOCK', 1, 'self', 'END', 20))
allAbilities.append(BuffAbility('BLOCK 2', 2, 'self', 'END', 25))
allAbilities.append(BuffAbility('DEAD MAN WALKING', 2, 'self', 'END', 20))
allAbilities.append(BuffAbility('DEAD MAN WALKING 2', 3, 'self', 'END', 25))
#death throes
#doppelganger*
allAbilities.append(BuffAbility('ENCOURAGE', 1, 'ally', 'END', 0))
#extraaction*
#extraction2*
#extrashot*
allAbilities.append(BuffAbility('HEAL', 1, 'ally', 'NOU', 20))
allAbilities.append(BuffAbility('HEAL 2', 2, 'ally', 'NOU', 22))
allAbilities.append(BuffAbility('HEAL 3', 4, 'ally', 'NOU', 24))
allAbilities.append(BuffAbility('SHARPEN', 1, 'ally', 'END', 0))
allAbilities.append(BuffAbility('TIGHTEN', 1, 'ally', 'END', 0))
allAbilities.append(BuffAbility('SHARPEN', 1, 'ally', 'END', 0))
allAbilities.append(BuffAbility('ROUSING SHOUT', 2, 'ally', 'NA', 0))
allAbilities.append(BuffAbility('ROUSING SONG', 0, 'ally', 'NA', 0))


#MELEE ABILITIES

allAbilities.append(MeleeAbility('BACKSTAB', 1, 'enemy', 'COR', 'NA', 'COR', False))
allAbilities.append(MeleeAbility('DISARM', 3, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('FEINT', 1, 'enemy', 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FEINT 2', 2, 'enemy', 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FEINT 3', 3, 'enemy', 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FLATTEN', 4, 'enemy', 'STR', 'COR', 'NA', False))
#garotte
allAbilities.append(MeleeAbility('KNOCK BACK', 1, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK BACK 2', 2, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK BACK 3', 3, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK OVER', 2, 'enemy', 'STR', 'COR', 'NA', True))
#off-hand attack
allAbilities.append(MeleeAbility('PIERCING THRUST', 2, 'enemy', 'STR', 'NA', 'STR', False))
#split attack
allAbilities.append(MeleeAbility('STRIKE', 0, 'enemy', 'COR', 'COR' , 'STR', False))
allAbilities.append(MeleeAbility('STUN', 1, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('STUN 2', 2, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('STUN 3', 3, 'enemy', 'STR', 'COR', 'NA', True))

#RANGED ABILITIES
allAbilities.append(RangedAbility('CURSE OF CLUMSINESS', 2, 'enemy', 'INT', 15, 'NA', True, 3))
allAbilities.append(RangedAbility('DOUBLE SHOT', 3, 'enemy', 'DEX', 15, 'STR', False, 3))
allAbilities.append(RangedAbility('FIREBALL', 1, 'enemy', 'INT', 15, 'DEX', True, 3))
allAbilities.append(RangedAbility('FIREBALL 2', 2, 'enemy', 'INT', 15, 'DEX', True, 3))
allAbilities.append(RangedAbility('FIREBALL 3', 3, 'enemy', 'INT', 15, 'DEX', True, 3))
allAbilities.append(RangedAbility('FIRESTORM', 3, 'enemy', 'INT', 20, 'INT', True, 3))
allAbilities.append(RangedAbility('FOOT SHOT', 3, 'enemy', 'DEX', 18, 'STR', False, 3))
allAbilities.append(RangedAbility('HEADACHE', 1, 'enemy', 'INT', 15, 'NA', True, 3))
allAbilities.append(RangedAbility('HEAD SHOT', 4, 'enemy', 'DEX', 30, 'STR', True, 3))
allAbilities.append(RangedAbility('MIGRAINE', 3, 'enemy', 'INT', 15, 'NA', True, 3))
allAbilities.append(RangedAbility('SHOOT', 1, 'enemy', 'DEX', 15, 'STR', False, 3))
allAbilities.append(RangedAbility('SHOOT 2', 2, 'enemy', 'DEX', 15, 'STR', False, 3))

def constructFighters():
    primedList.clear()
    simState.aliveList.clear()
    simState.deadList.clear()
    for i in chosenList:
        primedList.append(Creature(i))
    numberDuplicates(primedList)
    for monster in primedList:
        
        print (f"{monster.printName}")
    

def rollInitiative():
    for monster, team in zip(primedList, teamList):
        monster.INIT = monster._COR + D20.roll()
        monster.TEAM = team
    primedList.sort(key=operator.attrgetter('INIT'),reverse=True)
    if logEvents:
        loggingList = []
        loggingList = sorted(primedList, key=operator.attrgetter('TEAM'),reverse=True)
        cLog.record(f"Team 1:")
        for monster in loggingList:
            if (monster.TEAM == 1):
                cLog.record(monster.printName)
        cLog.record(f"\nTeam 2:")
        for monster in loggingList:
            if (monster.TEAM == 2):
                cLog.record(monster.printName)
        cLog.record("\n")


def beginCombatLoop(monList):
    simState.aliveList = teamList.copy()
    print (f"{simState.aliveList} : {teamList}")
    combatRound = 1
    while (simState.aliveList.count(1) > 0 and simState.aliveList.count(2) > 0):
        if logEvents:
            cLog.record(f"\nRound {combatRound}\n")
        print (f"Round {combatRound} Alive List:{simState.aliveList}")
        for monster in monList:
            statusTicker(monster)
            if (monster.isAlive):
                if not monster.isStunned:
                    monster.chooseTarget()
                    monster.chooseAlly()
                    monster.checkAbility()
                    monster.useAbility(monster.chooseAbility())
                    checkDeath(monster.target)
            if (simState.aliveList.count(1) == 0 or simState.aliveList.count(2) == 0):
                break
        combatRound += 1
    if logEvents:
            cLog.record(f"\nCombat Ended! Team {simState.aliveList[0]} won!")
    print (f"Combat Ended! Team {simState.aliveList} won!")
    combatRoundList.append(combatRound)
    return (sum(combatRoundList) / len(combatRoundList)), (simState.aliveList[0]-1)

if __name__ == '__main__':
    D20 = Die(20, 'D20')
    D12 = Die(12, 'D12')
    D10 = Die(10, 'D10')
    D8 = Die(8, 'D8')
    D6 = Die(6, 'D6')
    D4 = Die(4, 'D4')
    D0 = Die(0, 'D0')
    simState = SimState()
    varianceMinimizer = 1
    cycleloop = 0
    logEvents = False
    cLog = CombatLog("combat_log.txt", "./logs")
    while cycleloop < varianceMinimizer:
        if cycleloop+1 == varianceMinimizer:
            logEvents = True
        constructFighters()
        rollInitiative()
        avgCombatdur, combatVictor = beginCombatLoop(primedList)
        avgCombatdur = avgCombatdur - 1
        winrateList.append(combatVictor)
        if logEvents:
            print (f"{combatRoundList}, Average = {avgCombatdur}\n Winning Team: {combatVictor+1}")
        
        cycleloop += 1
    winrate =  (sum(winrateList) / len(winrateList))
    
    cLog.record(f"\nOver {varianceMinimizer} rounds:\n")
    cLog.record(f"Team 1 has {winrate*100}% winrate")
    cLog.record(f"Team 2 has {(1-winrate)*100}% winrate")
    cLog.record(f"The average number of rounds per combat was {avgCombatdur}")
    print (f"Team 1 has {winrate*100}% winrate \n Team 2 has {(1-winrate)*100}% winrate")
    print (f"\nFinal Round Outcome:")
    for monster in primedList:
        print (f"\n{monster.printName}")
        print (f"Initiative: {monster.INIT}")
        print (f"Team: {monster.TEAM}")
        print (f"HP: {monster._curHP}")
        print (f"AP: {monster.AP}")
        print (f"Abilities: {monster.abilities}")
    cLog.writeFile()
    

