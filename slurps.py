import pickle
import random
import operator
import os
import time
import tkinter as tk
from tkinter import filedialog

# Ask user to select a file
root = tk.Tk()
root.withdraw()
filePath = filedialog.askopenfilename()

# Load data from file
if filePath:
    with open(filePath, 'rb') as f:
        data = pickle.load(f)


print(f"Building monsters from file")
creatureDict = data['creatureDict']
hasAbilityDict = data['hasAbilityDict']
chosenList = data['chosenList']
teamList = data['teamList']
varianceMinimizer = data['testIterations']
primedList = []
uniqueAbilityList = []
allAbilities = []
combatRoundList = []
winrateList = []
avgCombatdur = 3.5
ffEnabled = True

#sorting key function
def takeSecond(elem):
    return elem[1]

#concatenates string names of monsters to differentiate between duplicates
def numberDuplicates(monsterlist):
    seen = {}
    for monster in monsterlist:
        key = str(monster.printName)
        if key in seen:
            seen[key] += 1
            monster.printName += " " + str(seen[key]+1)
        else:
            seen[key] = 0

#combat log class is called when logging is true
class CombatLog:
    def __init__(self, filename, logdir):
        self.filename = filename
        self.log = []
        self.logdir = logdir
        if not os.path.exists(logdir):
            os.mkdir(logdir)
    
    #appends the event to the log 
    def record(self, event):
        fevent = event + "\n"
        self.log.append(fevent)
    
    #dumps the log as a file with a timestamp name
    def writeFile(self):
        filename = time.strftime('%Y%m%d%H%M%S_combat_log.txt')
        filepath = os.path.join(self.logdir, filename)
        with open(filepath, 'w') as f:
            for event in self.log:
                f.write(event)

#creature class builds from the creatureDict dictionary
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
        self.headacheSeverityPrintName = ''
        self.hasSummoningSickness = 0
        #alternate tick status effects
        self.extraAction = 0
        self.extraShot = 0
        self.doubleShot = 0
        #notick status effects
        self.isSharpened = 0
        self.isTightened = 0        
        

        #equipment assignment
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
        self.defWEA = self._WEA
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
        self.defRWEA = self._RWEA
        self.ARM = creatureDict[type]['ARM']
        self.baseARM = creatureDict[type]['ARM']

        #ability logic
        self.AP = creatureDict[type]['AP']
        self._maxAP = creatureDict[type]['AP']
        self.abilities = hasAbilityDict[type]
        self.prioList = []

    # when called sets monster to dead and appends the log with the event
    def kill(self):
        self.isAlive = False
        if logEvents:
            cLog.record(f"{self.printName} died!")

    # remove the stunned effect and damages the monster
    def takeDamage(self, damage):
        self._curHP = self._curHP - damage
        if damage > 0:
            self.isStunned = 0
        return
    
    def takeHealing(self, healing):
        if (self._curHP + healing < self._maxHP):
            self._curHP = self._curHP + healing
            return
        self._curHP = self._maxHP
        return

    def healWeighting(self, healing):
        if self._curHP == self._maxHP:
            return 0  # or some other high weighting
        elif self._maxHP / (self._curHP + healing) > 1.3:
            return (self._maxHP / (self._curHP + healing))
        else:
            return 0.5

    
    def checkAbility(self):
        weightingList = []
        for ability in self.abilities:
            for realability in allAbilities:
                weighting = self.setPriority(realability, ability)
                if not weighting == None:
                    weightingList.append(int(weighting))
        self.prioList = list(zip(self.abilities, weightingList))
        self.prioList.sort(key=takeSecond)
        print(f"{self.prioList}")

    def hitChance(self, successBonus, successContest):
        roll = 1
        while roll <= 100:
            if (successBonus+roll >= successContest):
                return (1 - ((roll-1)/20)) 
            roll +=1

    def setPriority(self, realability, ability):
        if realability.name == ability:
            armour = 0
            range = 0
            ignoreARM = False
            if hasattr(realability, 'ignoreARM'):
                ignoreARM = realability.ignoreARM
            if hasattr(realability, 'ranged'):
                range = realability.ranged
            successBonus = realability.statSuccess(realability.success, self) + D20.average()
            match realability.target:
                case 'enemy':
                    successContest = realability.statSuccess(realability.contest, self.target)
                    if not (ignoreARM):
                        armour = self.target.ARM
                    if not (range):
                        successContest = D20.average() + successContest + armour
                    else:
                        successContest = successContest + armour + range
                case 'ally'|'self':
                    successContest = realability.statSuccess(realability.contest, self.target) + D20.average()
                    
            weighting = self.hitChance(successBonus, successContest) * realability.onSuccess(self, self.target, True)
            return weighting

    def chooseAbility(self):
        return self.prioList[-1][0]    
            
    #choose an enemy 
    def chooseTarget(self):
        if self.TEAM == 1:
            opposition = 2
        else:
            opposition = 1
        if self.target is None:
            self.target = random.choice(primedList)
        if opposition in simState.aliveList:
            while ((self.target.TEAM == self.TEAM) or (self.target.isAlive == False) or (self.target.isStunned == True)):
                self.target = random.choice(primedList)
            if all(tar.isStunned for tar in primedList if tar.TEAM == opposition):
                stunnedTargets = [tar for tar in primedList if tar.isStunned and tar.TEAM == opposition]
                if stunnedTargets:
                    self.target = random.choice(stunnedTargets)
            return

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
                if option.AP > self.AP:
                    if logEvents:
                        cLog.record(f"{self.printName} cannot use {option.name} as they do not have enough AP!")
                    return
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
    
    def statHighest(self):
        return max(self.strength(), self.coordination(), self.endurance(), self.intelligence(), self.nouse(), self.will())
    
class SimState():
    def __init__(self):
        self.aliveList = []
        self.deadList = []
        self.staleMate = False

def checkDeath(monster):
    if monster.isAlive:
        if (monster._curHP <= 0):
            simState.deadList.insert(-1, monster.printName)
            simState.aliveList.remove(monster.TEAM)
            monster.kill()

def statusTicker(monster):
    # if (monster.hasSummoningSickness):
    #     monster.hasSummoningSickness -= 1

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
        if not(monster.isDisarmed):
            monster._WEA, monster._RWEA = monster.defWEA, monster.defRWEA
        #set dice back to original weapon die (need to add to creature class)

    if (monster.isClumsy):
        monster.isClumsy -= 1
        if not(monster.isClumsy):
            monster.tempCOR += (monster._COR/2)

    if (monster.isBlocking):
        monster.isBlocking -= 1
        if not(monster.isBlocking):
            monster.ARM -= monster.baseARM
            if monster.ARM < 0:
                monster.ARM = 0
    
    if (monster.hasHeadache):
        monster.hasHeadache -= 1
        monster.takeDamage(monster.headacheSeverity)
        if logEvents:
            cLog.record(f"{monster.printName} takes {monster.headacheSeverity} damage from a {monster.headacheSeverityPrintName}")
    
    if (monster._curHP > monster._maxHP):
        monster._curHP = monster._maxHP

    checkDeath(monster)

class Die():
    def __init__(self, sides, name):
        self.sides = sides
        self.name = name
    
    def roll(self):
        if self.sides > 0: 
            return random.randint(1,self.sides)
        return 0
    
    def average(self):
        return (self.sides+1)/2


class Ability():
    def __init__(self, name, AP, target, success, contest):
        
        self.name = name
        self.AP = AP
        self.target = target
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
                doppelRoll = D2.roll()
                if not target.isDoppelgangered or doppelRoll == 2:
                    if not (ignoreARM):
                        armour = target.ARM
                    if not (range):
                        if (D20.roll() + successBonus >= D20.roll() + successContest + armour):
                            target.takeDamage(self.onSuccess(caster, target, False))
                        else:
                            if logEvents:
                                cLog.record(f"{caster.printName} missed {target.printName}")
                    else:
                        if (D20.roll() + successBonus >= self.contest + range + armour):
                            target.takeDamage(self.onSuccess(caster, target, False))
                        else:
                            if logEvents:
                                cLog.record(f"{caster.printName} missed {target.printName}")
                else:
                    if logEvents:
                        cLog.record(f"{caster.printName} strikes an illusory doppelganger of {target.printName}!")
        
          
class BuffAbility(Ability):
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
                        return abilityweight
                    

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
                        return abilityweight

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
                        return abilityweight
                    

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
                        return abilityweight
                    
            case 'DOPPELGANGER':
                if not test:
                    caster.isDoppelgangered = D8.roll()+1
                    if logEvents:
                        cLog.record(f"{caster.printName} creates a illusory clone mimicking their movements for {caster.isDoppelgangered} rounds!")
                if test:
                    if self.canCast(caster):
                        if not (caster.isDoppelgangered):
                            abilityweight =  caster.target.statAverage() * D8.average() * (D8.average()+1) / self.combatDurWeighting(D8.average()+1)
                        return abilityweight
                        
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
                            # stats+maxHP increase quartered, multiplied by the duration 
                        else:
                            abilityweight = 0
                        return abilityweight

            case 'EXTRA ACTION':
                if not test:
                    caster.extraAction = 2
                    while caster.extraAction > 0:
                        caster.chooseTarget()
                        monster.chooseAlly()
                        caster.checkAbility()
                        caster.useAbility(caster.chooseAbility())
                        caster.extraAction -= 1
                if test:
                    if self.canCast(caster):
                        dieroll = caster._RWEA.average()
                        abilityweight = dieroll * caster.statHighest() * 3
                        if caster.extraAction:
                            abilityweight *= 0
                        if caster.extraShot:
                            abilityweight *= 0
                        return abilityweight

            case 'EXTRA ACTION 2':
                if not test:
                    caster.extraAction = 3
                    while caster.extraAction > 0:
                        caster.chooseTarget()
                        monster.chooseAlly()
                        caster.checkAbility()
                        caster.useAbility(caster.chooseAbility())
                        caster.extraAction -= 1
                if test:
                    if self.canCast(caster):
                        dieroll = caster._RWEA.average()
                        abilityweight = dieroll * caster.statHighest() * 1.5 * 4
                        if caster.extraAction:
                            abilityweight *= 0
                        if caster.extraShot:
                            abilityweight *= 0
                        return abilityweight

            case 'EXTRA SHOT':
                if not test:
                    caster.extraShot = 2
                    while caster.extraShot > 0:
                        caster.chooseTarget()
                        caster.checkAbility()
                        caster.useAbility(caster.chooseAbility())
                        caster.extraShot -= 1
                if test:
                    if self.canCast(caster):
                        dieroll = caster._RWEA.average()
                        abilityweight = dieroll * self.statSuccess('DEX', caster) * 3
                        if caster.extraAction:
                            abilityweight *= 0
                        if caster.extraShot:
                            abilityweight *= 0
                        return abilityweight

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
                    return abilityweight

            case 'HEAL 2':
                if not test:
                    healval = caster.dexterity() * (D6.roll() + 4)
                    target.takeHealing(healval)
                    if logEvents:
                        cLog.record(f"{caster.printName} healed {caster.targetAlly.printName} for {healval}!")
                if test:
                    if self.canCast(caster):
                        healval = caster.dexterity() * (D6.average() + 4)
                        abilityweight = (healval / 2) * target.healWeighting(healval)
                    return abilityweight

            case 'HEAL 3':
                if not test:
                    healval = caster.dexterity() * (D12.roll() + 4)
                    target.takeHealing(healval)
                    if logEvents:
                        cLog.record(f"{caster.printName} healed {caster.targetAlly.printName} for {healval}!")
                if test:
                    if self.canCast(caster):
                        healval = caster.dexterity() * (D12.average() + 4)
                        abilityweight = (healval / 2) * target.healWeighting(healval) 
                    return abilityweight
                        
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
                    return abilityweight
                
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
                    return abilityweight
                    
            case 'SHARPEN'|'WEIGHTEN':
                if not test:
                    caster.isSharpened = 1
                    caster.modWEA += 1
                    if logEvents:
                            cLog.record(f"{caster.printName} enhances their weapon!")
                if test:
                    if self.canCast(caster):
                        abilityweight = avgCombatdur*caster.statHighest()
                        if caster.isSharpened:
                            abilityweight *= 0
                    return abilityweight

            case 'TIGHTEN':
                if not test:
                    caster.isTightened = 1
                    caster.modRWEA += 1
                    if logEvents:
                            cLog.record(f"{caster.printName} enhances their weapon!")
                if test:
                    if self.canCast(caster):
                        abilityweight = avgCombatdur*caster.statHighest()
                        if caster.isTightened:
                            abilityweight *= 0
                    return abilityweight
        return abilityweight        

class DebuffAbility(Ability):
    def __init__(self, name, AP, target, success, contest):
        super().__init__(name, AP, target, success, contest)
        self.effect = name
    def onSuccess(self, caster, target, test):
        abilityweight = 0
        match self.effect:

            case 'PANIC':
                if not test:
                    target.tempSTR -= 5
                    target.tempCOR -= 5
                    target.isPanicked = D4.roll()+1
                    if logEvents:
                        cLog.record(f"{caster.printName} panics {target.printName} for {target.isPanicked} rounds!")
                if test:
                    if self.canCast(caster):
                        if not target.isPanicked:
                            abilityweight =  (max(target._RWEA.average(), target._WEA.average()))*2.5*(D4.average()+1)/ self.combatDurWeighting(D4.average()+1)
                        else:
                            abilityweight = 0
                    return abilityweight

            case 'PETRIFY':
                if not test:
                    target.tempSTR -= 2
                    target.tempEND -= 2
                    target.tempCOR -= 2
                    target.tempDEX -= 2
                    target.tempINT -= 2
                    target.tempNOU -= 2
                    target.tempWIL -= 2
                    target._maxHP -= 20
                    target.isPetrified = D4.roll()+3
                    if logEvents:
                        cLog.record(f"{caster.printName} petrifies {target.printName} for {target.isPetrified} rounds!")
                if test:
                    if self.canCast(caster):
                        if not (target.isPetrified):
                            abilityweight =  (19 * (D4.average()+3)) / self.combatDurWeighting(D4.average()+3)
                        else:
                            abilityweight = 0
                    return abilityweight  

            case 'SCARE':
                if not test:
                    target.tempSTR -= 1
                    target.tempEND -= 1
                    target.tempCOR -= 1
                    target.tempDEX -= 1
                    target.tempINT -= 1
                    target.tempNOU -= 1
                    target.tempWIL -= 1
                    target._maxHP -= 10
                    target.isScared = D4.roll()+1
                    if logEvents:
                        cLog.record(f"{caster.printName} scares {target.printName} for {target.isScared} rounds!")
                if test:
                    if self.canCast(caster):
                        if not target.isScared:
                            abilityweight =  (12 * (D4.average()+1)) / self.combatDurWeighting(D4.average()+1)
                        else:
                            abilityweight = 0
                    return abilityweight  

            case 'SCARE 2':
                if not test:
                    target.tempSTR -= 1
                    target.tempEND -= 1
                    target.tempCOR -= 1
                    target.tempDEX -= 1
                    target.tempINT -= 1
                    target.tempNOU -= 1
                    target.tempWIL -= 1
                    target._maxHP -= 10
                    target.isScared = D4.roll()+4
                    if logEvents:
                        cLog.record(f"{caster.printName} scares {target.printName} for {target.isScared} rounds!")
                if test:
                    if self.canCast(caster):
                        if not target.isScared:
                            abilityweight =  (12 * (D4.average()+4)) / self.combatDurWeighting(D4.average()+4)
                        else:
                            abilityweight = 0
                    return abilityweight

            case 'UNDRESS':
                if not test:
                    target.ARM = 0
                    if logEvents:
                        cLog.record(f"{caster.printName} undressed {target.printName} and their armour clatters to the ground!")
                if test:
                    if self.canCast(caster):
                            abilityweight =  (target.ARM/20) * max(target._RWEA.average(), target._WEA.average()) * avgCombatdur
                    return abilityweight
                        
        return abilityweight       

class MeleeAbility(Ability):
    def __init__(self, name, AP, target, success, contest, damstat, ignoreARM):
        super().__init__(name, AP, target, success, contest)
        self.damStat = damstat
        self.ignoreARM = ignoreARM
    def onSuccess(self, caster, target, test):
        totaldamage = 0
        match self.name:

            case 'BACKSTAB':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    return totaldamage

            case 'DISARM':
                if not test:
                    disarmDuration = D4.roll() + 1
                    target._WEA, target._RWEA = D0
                    if target.isDisarmed < disarmDuration:
                        target.isDisarmed = disarmDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} and disarmed them for {disarmDuration} rounds!")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
                    return totaldamage
            
            case 'FEINT':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 1) * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 1) * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
            case 'FEINT 2':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
            case 'FEINT 3':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 3) * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 3) * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
            case 'FLATTEN':
                if not test:
                    effectDuration = D6.roll() + 4
                    if target.isProne < effectDuration:
                        target.isProne = effectDuration
                    if target.isStunned < effectDuration:
                        target.isStunned = effectDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} flattened {target.printName} for {target.isProne} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0 + 0
                    return totaldamage
            
            case 'KNOCK OVER':
                if not test:
                    proneDuration = D4.roll() + 1
                    if target.isProne < proneDuration:
                        target.isProne = proneDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and knocked {target.printName} over for {target.isProne} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage = 0
                    return totaldamage
            
            case 'PIERCING THRUST':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = (dieroll + 2) * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
            case 'STRIKE':
                if not test:
                    dieroll = caster._WEA.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._WEA.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
            case 'STUN':
                if not test:
                    stunDuration = D4.roll() + 1
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage =  D6.average() * target.statAverage() / self.combatDurWeighting(D4.average()+1)
                    return totaldamage
            
            case 'STUN 2':
                if not test:
                    stunDuration = D4.roll() + 3
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage =  D6.average() * target.statAverage() / self.combatDurWeighting(D4.average()+3)
                    return totaldamage
            
            case 'STUN 3':
                if not test:
                    stunDuration = D6.roll() + 6
                    if target.isStunned < stunDuration:
                        target.isStunned = stunDuration
                    if logEvents:
                        cLog.record(f"{caster.printName} hit and stunned {target.printName} for {target.isStunned} rounds")
                if test:
                    if self.canCast(caster):
                        totaldamage =  D6.average() * target.statAverage() / self.combatDurWeighting(D6.average()+6)
                    return totaldamage
            
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
                if test:
                    if self.canCast(caster):
                        totaldamage = target.coordination() * (D4.roll+1) / 2 / self.combatDurWeighting(D4.roll+1)
                    return totaldamage

            case 'DOUBLE SHOT':
                if not test:
                    caster.doubleShot = 2
                    while caster.doubleShot > 0:
                        caster.checkAbility()
                        caster.useAbility(caster.chooseAbility())
                        caster.doubleShot -= 1
                if test:
                    if self.canCast(caster):
                        dieroll = caster._RWEA.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster) * 2
                        if caster.extraShot:
                            totaldamage *= 100
                        if caster.doubleShot:
                            totaldamage *= 0
                        return totaldamage
            
            case 'FIREBALL':
                if not test:
                    dieroll = D4.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = D4.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
            case 'FIREBALL 2':
                if not test:
                    dieroll = D6.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = D6.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
            case 'FIREBALL 3':
                if not test:
                    dieroll = D8.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} hit {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = D8.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    return totaldamage
            
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
                                        if logEvents:
                                            cLog.record(f"{caster.printName} singed themselves for {totaldamage} damage")
                                        checkDeath(monster)
                                    else:
                                        if logEvents:
                                            cLog.record(f"{caster.printName} singed their ally {monster.printName} for {totaldamage} damage")
                                        checkDeath(monster)
                                                                
                                elif monster == caster.target:
                                    if logEvents:
                                        cLog.record(f"{caster.printName} blasted {monster.printName} for {totaldamage*2} damage")
                                else:
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
                                        if logEvents:
                                            cLog.record(f"{caster.printName} singed {monster.printName} for {totaldamage} damage")
                                        checkDeath(monster)
                                    else:
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
                            totaldamage = totaldamage * 0
                    return totaldamage

            case 'HEADACHE':
                if not test:
                    if not (target.hasHeadache):
                        target.headacheSeverity = 10
                        target.hasHeadache = 3
                        target.headacheSeverityPrintName = 'HEADACHE'
                        totaldamage = target.headacheSeverity
                        if logEvents:
                            cLog.record(f"{caster.printName} inflicted {target.printName} with a painful {target.headacheSeverityPrintName}, causing {target.headacheSeverity} damage")
                if test:
                    if self.canCast(caster):
                        if not (target.hasHeadache):
                            totaldamage = (10 * 3 / self.combatDurWeighting(3))   
                        else:
                            totaldamage = 0
                        return totaldamage
            
            case 'HEADSHOT':
                if not test:
                    dieroll = caster._RWEA.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster) * 4
                    if logEvents:
                        cLog.record(f"{caster.printName} headshot {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._RWEA.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster) * 4
                        if caster.extraShot:
                            totaldamage *= 100
                    return totaldamage
                    
            case 'MIGRAINE':
                if not test:
                    if not (target.hasHeadache or target.headacheSeverity == 10):
                        target.headacheSeverity = 20
                        target.hasHeadache = 5
                        target.headacheSeverityPrintName = 'MIGRAINE'
                        totaldamage = target.headacheSeverity
                        if logEvents:
                            cLog.record(f"{caster.printName} inflicted {target.printName} with a painful {target.headacheSeverityPrintName}, causing {target.headacheSeverity} damage")
                if test:
                    if self.canCast(caster):
                        if not (target.hasHeadache):
                            totaldamage = (20 * 5 / self.combatDurWeighting(5))  
                        elif (target.headacheSeverity == 10):
                            totaldamage = (10 * target.hasHeadache + 20 * (5-target.hasHeadache))/ self.combatDurWeighting(5)
                        else:
                            totaldamage = 0
                        return totaldamage
            
            case 'SHOOT':
                if not test:
                    dieroll = caster._RWEA.roll()
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} shot {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._RWEA.average()
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                        if caster.extraShot:
                            totaldamage *= 100
                        if caster.doubleShot:
                            totaldamage *= 100
                    return totaldamage
            
            case 'SHOOT 2':
                if not test:
                    dieroll = caster._RWEA.roll() + 2
                    totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                    if logEvents:
                        cLog.record(f"{caster.printName} shot {target.printName} for {totaldamage} damage")
                if test:
                    if self.canCast(caster):
                        dieroll = caster._RWEA.average() + 2
                        totaldamage = dieroll * self.statSuccess(self.damStat, caster)
                        if caster.extraShot:
                            totaldamage *= 100
                    return totaldamage
            case _:
                pass
        return totaldamage
#BUFF ABILITIES

allAbilities.append(BuffAbility('BLOCK', 1, 'self', 'END', 20))
allAbilities.append(BuffAbility('BLOCK 2', 2, 'self', 'END', 25))
# allAbilities.append(BuffAbility('CONJURE RAT', 0, 'self', 'NA', 0))
allAbilities.append(BuffAbility('DEAD MAN WALKING', 2, 'self', 'END', 20))
allAbilities.append(BuffAbility('DEAD MAN WALKING 2', 3, 'self', 'END', 25))
allAbilities.append(BuffAbility('DOPPELGANGER', 3, 'self', 'INT', 30))
allAbilities.append(BuffAbility('ENCOURAGE', 1, 'ally', 'END', 0))
allAbilities.append(BuffAbility('EXTRA ACTION', 3, 'self', 'NA', 0))
allAbilities.append(BuffAbility('EXTRA ACTION 2', 5, 'self', 'NOU', 20))
allAbilities.append(BuffAbility('EXTRA SHOT', 1, 'self', 'DEX', 20))
allAbilities.append(BuffAbility('HEAL', 1, 'ally', 'NOU', 20))
allAbilities.append(BuffAbility('HEAL 2', 2, 'ally', 'NOU', 22))
allAbilities.append(BuffAbility('HEAL 3', 4, 'ally', 'NOU', 24))
allAbilities.append(BuffAbility('SHARPEN', 1, 'ally', 'NA', 0))
allAbilities.append(BuffAbility('WEIGHTEN', 1, 'ally', 'NA', 0))
allAbilities.append(BuffAbility('TIGHTEN', 1, 'ally', 'NA', 0))
allAbilities.append(BuffAbility('ROUSING SHOUT', 2, 'ally', 'NA', 0))
allAbilities.append(BuffAbility('ROUSING SONG', 0, 'ally', 'NA', 0))


#MELEE ABILITIES

allAbilities.append(MeleeAbility('BACKSTAB', 1, 'enemy', 'COR', 'NA', 'COR', False))
allAbilities.append(MeleeAbility('DISARM', 3, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('FEINT', 1, 'enemy', 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FEINT 2', 2, 'enemy', 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FEINT 3', 3, 'enemy', 'COR', 'NOU', 'STR', False))
allAbilities.append(MeleeAbility('FLATTEN', 4, 'enemy', 'STR', 'COR', 'NA', False))
allAbilities.append(MeleeAbility('KNOCK BACK', 1, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK BACK 2', 2, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK BACK 3', 3, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('KNOCK OVER', 2, 'enemy', 'STR', 'COR', 'NA', True))
allAbilities.append(MeleeAbility('PIERCING THRUST', 2, 'enemy', 'STR', 'NA', 'STR', False))
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

#DEBUFF ABILITIES
allAbilities.append(DebuffAbility('PANIC', 2, 'enemy', 'WIL', 'WIL'))
allAbilities.append(DebuffAbility('PETRIFY', 3, 'enemy', 'WIL', 'WIL'))
allAbilities.append(DebuffAbility('SCARE', 1, 'enemy', 'WIL', 'WIL'))
allAbilities.append(DebuffAbility('SCARE 2', 1, 'enemy', 'WIL', 'WIL'))
allAbilities.append(DebuffAbility('UNDRESS', 3, 'enemy', 'DEX', 'DEX'))

def constructFighters():
    primedList.clear()
    simState.aliveList.clear()
    simState.deadList.clear()
    for i in chosenList:
        primedList.append(Creature(i))
    numberDuplicates(primedList)
    

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
    combatRound = 1
    while (simState.aliveList.count(1) > 0 and simState.aliveList.count(2) > 0):
        if logEvents:
            cLog.record(f"\nRound {combatRound}\n")
        for monster in monList:
            statusTicker(monster)
            if (monster.isAlive):
                if not monster.isStunned:
                    monster.chooseTarget()
                    monster.chooseAlly()
                    monster.checkAbility()
                    monster.useAbility(monster.chooseAbility())
                    checkDeath(monster.target)
                else:
                    if logEvents:
                        cLog.record(f"{monster.printName} stumbles around stunned taking no actions.")
            if (simState.aliveList.count(1) == 0 or simState.aliveList.count(2) == 0):
                break
        if combatRound > 100:
            simState.staleMate = True
            break
        combatRound += 1
    if logEvents:
        cLog.record(f"\nCombat Ended! Team {simState.aliveList[0]} won!")
    combatRoundList.append(combatRound)
    return (sum(combatRoundList) / len(combatRoundList)), (simState.aliveList[0]-1)

if __name__ == '__main__':
    print(f"Calibrating RNG")
    D20 = Die(20, 'D20')
    D12 = Die(12, 'D12')
    D10 = Die(10, 'D10')
    D8 = Die(8, 'D8')
    D6 = Die(6, 'D6')
    D4 = Die(4, 'D4')
    D2 = Die(2, 'D2')
    D0 = Die(0, 'D0')
    simState = SimState()
    cycleloop = 0
    logEvents = False
    cLog = CombatLog("combat_log.txt", "./logs")
    print(f"Beginning combat!")
    while cycleloop < varianceMinimizer:
        if cycleloop+1 == varianceMinimizer:
            logEvents = True
        constructFighters()
        rollInitiative()
        avgCombatdur, combatVictor = beginCombatLoop(primedList)
        avgCombatdur = avgCombatdur - 1
        winrateList.append(combatVictor)
        if (cycleloop % 10 == 0) and (cycleloop != 0):
                print(f"Simulated {cycleloop} of {varianceMinimizer}...")
        if logEvents:
            cLog.record (f"{combatRoundList}, Average = {avgCombatdur}\n Winning Team: {combatVictor+1}")
        cycleloop += 1
    print(f"Concluding fights")
    print(f"Calculating winrate")
    winrate =  (sum(winrateList) / len(winrateList))
    
    cLog.record (f"\n\nMonster status after final round:")
    for monster in primedList:
        cLog.record (f"\n{monster.printName}")
        cLog.record (f"Initiative: {monster.INIT}")
        cLog.record (f"Team: {monster.TEAM}")
        cLog.record (f"HP: {monster._curHP}")
        cLog.record (f"AP: {monster.AP}")
        cLog.record (f"Abilities: {monster.abilities}")
    
    cLog.record(f"\nOver {varianceMinimizer} rounds:\n")
    cLog.record(f"Team 1 has {(1-winrate)*100}% winrate")
    cLog.record(f"Team 2 has {(winrate)*100}% winrate")
    cLog.record(f"The average number of rounds per combat was {avgCombatdur}")
    if simState.staleMate:
        cLog.record(f"Stalemates detected, winner and winrate may be inaccurate!!")
    print(f"Logging results")
    cLog.writeFile()
    

