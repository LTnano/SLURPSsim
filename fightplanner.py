import pickle
import webbrowser
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class MonsterSelectGUI:
    def __init__(self, master):
        self.teamOne = []
        self.teamTwo = []
        self.chosenList = []
        self.teamList = []
        # Name, Health | Strength, Endurance, Coordination, Dexterity, Intelligence, Nouse, Will | Weapon, Ranged Weapon | Armour, Ability Points
        self.creatureDict = {
        'giantRat' : {'Name': 'Giant Rat', 'HP' : 50, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 8, 'INT' : 2, 'NOU' : 4, 'WIL' : 3, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 0},

        'meleeSkeleton' : {'Name' : 'Skeleton', 'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 2, 'AP' : 0},

        'meleeSkeletonH' : {'Name' : 'Skeleton (Hard)', 'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 9},

        'rangedSkeleton' : {'Name': 'Skeleton Archer', 'HP' : 110, 'STR' : 8, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 4, 'ARM' : 0, 'AP' : 9},

        'rangedSkeletonH' : {'Name' : 'Skeleton Archer(Hard)', 'HP' : 110, 'STR' : 8, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 6, 'ARM' : 0, 'AP' : 7},

        'wizardSkeleton' : {'Name': 'Skeleton Wizard', 'HP' : 100, 'STR' : 7, 'END' : 8, 'COR' : 8, 'DEX' : 7, 'INT' : 11, 'NOU' : 6, 'WIL' : 2, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'meleeKobold' : {'Name': 'Kobold Warrior', 'HP' : 60, 'STR' : 9, 'END' : 6, 'COR' : 8, 'DEX' : 5, 'INT' : 5, 'NOU' : 6, 'WIL' : 4, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 1, 'AP' : 0},

        'wizardKobold' : {'Name': 'Kobold Mage', 'HP' : 40, 'STR' : 6, 'END' : 6, 'COR' : 7, 'DEX' : 7, 'INT' : 10, 'NOU' : 7, 'WIL' : 8, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 7},

        'rangedKobold' : {'Name': 'Kobold Archer', 'HP' : 40, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 9, 'INT' : 8, 'NOU' : 6, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 4, 'ARM' : 0, 'AP' : 6},

        'priestKobold' : {'Name': 'Kobold Healer', 'HP' : 30, 'STR' : 3, 'END' : 5, 'COR' : 8, 'DEX' : 9, 'INT' : 7, 'NOU' : 6, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 7},

        'slowGolem' : {'Name': 'Golem', 'HP' : 300, 'STR' : 14, 'END' : 30, 'COR' : 8, 'DEX' : 4, 'INT' : 2, 'NOU' : 2, 'WIL' : 2, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 5, 'AP' : 0},

        'thinBilly' : {'Name' : 'Thin Billy', 'HP' : 200, 'STR' : 13, 'END' : 20, 'COR' : 13, 'DEX' : 13, 'INT' : 13, 'NOU' : 17, 'WIL' : 13, 'WEA' : 8, 'RWEA' : 0, 'ARM' : 2, 'AP' : 10},
                
        'bossSkeleton' : {'Name' : 'Captain Boney', 'HP' : 250, 'STR' : 15, 'END' : 25, 'COR' : 15, 'DEX' : 12, 'INT' : 17, 'NOU' : 12, 'WIL' : 13, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 5, 'AP' : 12},
        
        'humanlvl1' : {'Name' : 'Human Novice Adventurer', 'HP' : 100, 'STR' : 10, 'END' : 10, 'COR' : 10, 'DEX' : 10, 'INT' : 10, 'NOU' : 10, 'WIL' : 10, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'trolllvl1' : {'Name' : 'Troll Novice Adventurer', 'HP' : 100, 'STR' : 13, 'END' : 10, 'COR' : 10, 'DEX' : 7, 'INT' : 10, 'NOU' : 10, 'WIL' : 10, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'dwarflvl1' : {'Name' : 'Dwarf Novice Adventurer', 'HP' : 130, 'STR' : 10, 'END' : 13, 'COR' : 10, 'DEX' : 10, 'INT' : 7, 'NOU' : 10, 'WIL' : 10, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'ranilvl1' : {'Name' : 'Rani Novice Adventurer', 'HP' : 100, 'STR' : 7, 'END' : 10, 'COR' : 13, 'DEX' : 10, 'INT' : 10, 'NOU' : 10, 'WIL' : 10, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'elflvl1' : {'Name' : 'Elf Novice Adventurer', 'HP' : 100, 'STR' : 10, 'END' : 10, 'COR' : 10, 'DEX' : 13, 'INT' : 10, 'NOU' : 7, 'WIL' : 10, 'WEA' : 4, 'RWEA' : 4, 'ARM' : 0, 'AP' : 10},

        'sagelvl1' : {'Name' : 'Sage Novice Adventurer', 'HP' : 100, 'STR' : 10, 'END' : 10, 'COR' : 10, 'DEX' : 10, 'INT' : 13, 'NOU' : 10, 'WIL' : 7, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 11},
        
        'goblinlvl1' : {'Name' : 'Goblin Novice Adventurer', 'HP' : 70, 'STR' : 10, 'END' : 7, 'COR' : 10, 'DEX' : 10, 'INT' : 10, 'NOU' : 13, 'WIL' : 10, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'faylvl1' : {'Name' : 'Fay Novice Adventurer', 'HP' : 100, 'STR' : 10, 'END' : 10, 'COR' : 7, 'DEX' : 10, 'INT' : 10, 'NOU' : 10, 'WIL' : 13, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'humanlvl4' : {'Name' : 'Human Adventurer', 'HP' : 134, 'STR' : 16, 'END' : 12, 'COR' : 12, 'DEX' : 10, 'INT' : 10, 'NOU' : 12, 'WIL' : 10, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 13},

        'trolllvl4' : {'Name' : 'Troll Adventurer', 'HP' : 136, 'STR' : 15, 'END' : 14, 'COR' : 10, 'DEX' : 7, 'INT' : 10, 'NOU' : 10, 'WIL' : 10, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 13},

        'dwarflvl4' : {'Name' : 'Dwarf Adventurer', 'HP' : 153, 'STR' : 15, 'END' : 18, 'COR' : 12, 'DEX' : 10, 'INT' : 7, 'NOU' : 10, 'WIL' : 10, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 13},

        'ranilvl4' : {'Name' : 'Rani Adventurer', 'HP' : 130, 'STR' : 13, 'END' : 10, 'COR' : 19, 'DEX' : 10, 'INT' : 10, 'NOU' : 10, 'WIL' : 10, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 13},

        'elflvl4' : {'Name' : 'Elf Adventurer', 'HP' : 130, 'STR' : 15, 'END' : 10, 'COR' : 10, 'DEX' : 20, 'INT' : 10, 'NOU' : 7, 'WIL' : 10, 'WEA' : 4, 'RWEA' : 6, 'ARM' : 1, 'AP' : 13},

        'sagelvl4' : {'Name' : 'Sage Adventurer', 'HP' : 130, 'STR' : 10, 'END' : 10, 'COR' : 10, 'DEX' : 13, 'INT' : 22, 'NOU' : 10, 'WIL' : 7, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 14},
        
        'goblinlvl4' : {'Name' : 'Goblin Adventurer', 'HP' : 121, 'STR' : 10, 'END' : 7, 'COR' : 12, 'DEX' : 10, 'INT' : 14, 'NOU' : 19, 'WIL' : 10, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 13},

        'faylvl4' : {'Name' : 'Fay Adventurer', 'HP' : 142, 'STR' : 10, 'END' : 16, 'COR' : 7, 'DEX' : 10, 'INT' : 10, 'NOU' : 10, 'WIL' : 19, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 13}
        }

        self.keyList = ['Name', 'HP', 'STR', 'END', 'COR', 'DEX', 'INT', 'NOU', 'WIL', 'WEA', 'RWEA', 'ARM', 'AP']
        self.hasAbilityDict = {
        'giantRat' : ['STRIKE'],

        'meleeSkeleton' : ['STRIKE'],

        'meleeSkeletonH' : ['STRIKE', 'FEINT'],

        'rangedSkeleton' : ['SHOOT'],

        'rangedSkeletonH' : ['SHOOT'],

        'wizardSkeleton' : ['FIREBALL 2'],

        'meleeKobold' : ['STRIKE'],

        'wizardKobold' : ['FIREBALL'],

        'rangedKobold' : ['SHOOT'],

        'priestKobold' : ['HEADACHE'],

        'slowGolem' : ['STRIKE'],

        'thinBilly' : ['STRIKE', 'HEAL'],
                
        'bossSkeleton' : ['STRIKE', 'FIREBALL', 'HEAL'],

        'humanlvl1' : ['STRIKE', 'HEAL'],

        'trolllvl1' : ['STRIKE', 'STUN'],

        'dwarflvl1' : ['STRIKE', 'TAUNT'],

        'ranilvl1' : ['STRIKE', 'FEINT'],

        'elflvl1' : ['STRIKE', 'SHOOT'],

        'sagelvl1' : ['STRIKE', 'FIREBALL'],

        'goblinlvl1' : ['STRIKE', 'HEAL'],

        'faylvl1' : ['STRIKE', 'SCARE'],

        'humanlvl4' : ['STRIKE', 'HEAL', 'ENCOURAGE', 'SHARPEN', 'KNOCK OVER', 'DEAD MAN WALKING', 'HEAL 2', 'STUN'],

        'trolllvl4' : ['STRIKE', 'STUN', 'SCARE', 'HEAL', 'KNOCK OVER', 'SHARPEN', 'STUN 2', 'BLOCK'],

        'dwarflvl4' : ['STRIKE', 'BLOCK', 'HEAL', 'DEAD MAN WALKING', 'SHARPEN', 'ENCOURAGE'],

        'ranilvl4' : ['STRIKE', 'FEINT', 'SCARE', 'SHARPEN', 'STUN', 'FEINT 2', 'HEADACHE'],

        'elflvl4' : ['STRIKE', 'SHOOT', 'STUN', 'FEINT', 'TIGHTEN', 'EXTRA SHOT', 'ENCOURAGE'],

        'sagelvl4' : ['STRIKE', 'FIREBALL', 'HEADACHE', 'SCARE', 'FIREBALL 2'],

        'goblinlvl4' : ['STRIKE', 'HEAL', 'FIREBALL', 'SHARPEN', 'HEAL 2', 'HEADACHE'],

        'faylvl4' : ['STRIKE', 'SCARE', 'ENCOURAGE', 'HEAL', 'PANIC', 'SHARPEN', 'BLOCK']
        }
        self.fields = {}
        self.possibleAbilities = ['BACKSTAB', 'BLOCK', 'BLOCK 2', 'CURSE OF CLUMSINESS',
                                  'DEAD MAN WALKING', 'DEAD MAN WALKING 2', 'DISARM', 'DOUBLE SHOT',
                                  'ENCOURAGE', 'EXTRA SHOT', 'FEINT', 'FEINT 2', 'FEINT 3', 'FIREBALL', 'FIREBALL 2',
                                  'FIREBALL 3', 'FIRESTORM', 'FLATTEN', 'FOOT SHOT', 'HEAD SHOT',
                                  'HEADACHE', 'HEAL', 'HEAL 2', 'HEAL 3', 'KNOCK BACK', 'KNOCK BACK 2',
                                  'KNOCK BACK 3', 'KNOCK OVER', 'MIGRAINE', 'PANIC', 'PETRIFY',
                                  'PIERCING THRUST', 'ROUSING SHOUT', 'ROUSING SONG', 'SCARE', 'SCARE 2',
                                  'SHARPEN', 'SHOOT', 'SHOOT 2', 'STRIKE', 'STUN',
                                  'STUN 2', 'STUN 3', 'TIGHTEN', 'UNDRESS', 'WEIGHTEN']
        self.creatureAbilities = []
        self.window = master
        self.window.title("Monster Manager")

        self.mainFrame = tk.Frame(master)
        self.monsterSelectionButton = tk.Button(self.mainFrame, text="Monster Selection", command=self.monsterSelection)
        self.monsterSelectionButton.pack()

        self.monsterEditorButton = tk.Button(self.mainFrame, text="Monster Editor", command=self.monsterEditor)
        self.monsterEditorButton.pack()

        self.helpButton = tk.Button(self.mainFrame, text="Help", command=self.help)
        self.helpButton.pack()
        self.mainFrame.pack()

    def monsterSelection(self):
        
        # forget mainframe
        self.mainFrame.pack_forget()
        # Create the monster listbox
        self.selectionFrame = tk.Frame(self.window)
        self.monsterListBox = tk.Listbox(self.selectionFrame, selectmode=tk.MULTIPLE)
        for name in self.creatureDict:
            self.monsterListBox.insert(tk.END, self.creatureDict[name]['Name'])
        self.monsterListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the return button
        self.returnMenuButton = tk.Button(self.selectionFrame, text="Return to Menu", command=lambda: self.returnMenu(self.selectionFrame))
        self.returnMenuButton.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create the add/remove buttons
        self.addLeftButton = tk.Button(self.selectionFrame, text="Add to Left Team", command=self.addLeft)
        self.addRightButton = tk.Button(self.selectionFrame, text="Add to Right Team", command=self.addRight)
        self.iterationsLabel = tk.Label(self.selectionFrame, text="Number of Iterations")
        self.numOfIterationsEntry = tk.Entry(self.selectionFrame)
        self.removeLeftButton = tk.Button(self.selectionFrame, text="Remove from Left Team", command=self.removeLeft)
        self.removeRightButton = tk.Button(self.selectionFrame, text="Remove from Right Team", command=self.removeRight)
        self.addLeftButton.pack(side=tk.TOP, padx=5, pady=5)
        self.addRightButton.pack(side=tk.TOP, padx=5, pady=5)
        self.iterationsLabel.pack(side=tk.TOP)
        self.numOfIterationsEntry.pack(side=tk.TOP, padx=5, pady=5)
        self.removeLeftButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.removeRightButton.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create the export button
        self.exportButton = tk.Button(self.selectionFrame, text="Export Teams", command=self.exportTeams)
        self.exportButton.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create the team listboxes
        self.teamOneListBox = tk.Listbox(self.selectionFrame)
        self.teamTwoListBox = tk.Listbox(self.selectionFrame)
        self.teamOneListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.teamTwoListBox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #pack
        self.selectionFrame.pack()
        
    def addLeft(self):
        for index in self.monsterListBox.curselection():
            name = list(self.creatureDict.keys())[index]
            monster = self.creatureDict[name]
            self.teamOne.append(name)
            self.teamOneListBox.insert(tk.END, monster['Name'])

    def addRight(self):
        for index in self.monsterListBox.curselection():
            name = list(self.creatureDict.keys())[index]
            monster = self.creatureDict[name]
            self.teamTwo.append(name)
            self.teamTwoListBox.insert(tk.END, monster['Name'])

    def removeLeft(self):
        for index in self.teamOneListBox.curselection():
            self.teamOne.pop(index)
            self.teamOneListBox.delete(index)

    def removeRight(self):
        for index in self.teamTwoListBox.curselection():
            self.teamTwo.pop(index)
            self.teamTwoListBox.delete(index)

    def exportTeams(self):
        self.chosenList = []
        self.teamList = []
        # Export the lists
        for item in self.teamOne:
            self.chosenList.append(item)
            self.teamList.append(1)
        for item in self.teamTwo:
            self.chosenList.append(item)
            self.teamList.append(2)
        try:
            numIterations = int(self.numOfIterationsEntry.get())
        except ValueError:
            # If the entry is empty or contains non-integer characters,
            # display an error message and set num_iterations to a default value
            messagebox.showerror("Error", "Iterations must be an integer, defaulting to 100")
            numIterations = 100
        data = {
            'teamList': self.teamList, 'chosenList': self.chosenList,
            'creatureDict': self.creatureDict, 'hasAbilityDict': self.hasAbilityDict,
            'testIterations': numIterations
            }
        filePath = filedialog.asksaveasfilename(defaultextension='.pkl')
        with open(filePath, 'wb') as f:
            pickle.dump(data, f)

    def returnMenu(self, widget):
        widget.destroy()
        self.mainFrame.pack()

    def monsterEditor(self):

        # reset creature abilities
        self.creatureAbilities = []

        # forget mainframe
        self.mainFrame.pack_forget()
        
        # create container
        self.inputFramesContainer = tk.Frame(self.window)
        self.inputFramesContainer.pack()

        # Create sides
        self.inputFramesRight = tk.Frame(self.inputFramesContainer)
        self.inputFramesLeft = tk.Frame(self.inputFramesContainer)

        # Create the return button
        self.returnMenuButton = tk.Button(self.inputFramesContainer, text="Return to Menu", command=lambda: self.returnMenu(self.inputFramesContainer))
        self.returnMenuButton.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create buttons to add, import and export monsters
        self.addMonsterButton = tk.Button(self.inputFramesContainer, text="Add Monster", command=lambda: self.addMonster('add'))
        self.addMonsterButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.importMonsterButton = tk.Button(self.inputFramesContainer, text="Import", command=self.importMon)
        self.importMonsterButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.exportMonsterButton = tk.Button(self.inputFramesContainer, text="Export", command=lambda: self.addMonster('export'))
        self.exportMonsterButton.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create the ability dropdown (right)
        self.abilityLabel = tk.Label(self.inputFramesRight, text="Choose Abilities")
        self.abilityLabel.pack()
        self.abilityFieldVal = tk.StringVar(self.inputFramesRight)
        self.abilityFieldVal.set(self.possibleAbilities[0])
        self.abilityDropdown = tk.OptionMenu(self.inputFramesRight, self.abilityFieldVal, *self.possibleAbilities)
        self.abilityDropdown.pack()

        # Create add/remove ability buttons (right)
        self.addAbilityButton = tk.Button(self.inputFramesRight, text="Add", command=self.addAbility)
        self.removeAbilityButton = tk.Button(self.inputFramesRight, text="Remove", command=self.removeAbility)
        self.addAbilityButton.pack(side=tk.RIGHT, padx=5, pady=5)
        self.removeAbilityButton.pack(side=tk.LEFT, padx=5, pady=5)        
        
        # Create list for abilities
        self.abilityListBox = tk.Listbox(self.inputFramesRight)
        self.abilityListBox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create fields for stats
        for key in self.keyList:
            label = tk.Label(self.inputFramesLeft, text=key)
            label.grid(row=self.keyList.index(key), column=0)
            if key in ["WEA", "RWEA"]:
                field = ttk.Combobox(self.inputFramesLeft, values=[0, 4, 6, 8, 10, 12, 20])
            else:
                field = tk.Entry(self.inputFramesLeft)
            field.grid(row=self.keyList.index(key), column=1)
            self.fields[key] = field
            
        # Pack right side
        self.inputFramesRight.pack(side=tk.RIGHT)
        self.inputFramesLeft.pack(side=tk.LEFT)

    def addMonster(self, type):
        if not self.creatureAbilities:
            messagebox.showerror(f"Error: creature abilities list is empty")
            return
        name = self.fields['Name'].get()
        if not isinstance(name, str):
            messagebox.showerror(f"Error: Name field must be a string")
            return
        newMonster = {'Name': name}
        for key in self.keyList:
            if key != 'Name':
                try:
                    newMonster[key] = int(self.fields[key].get())
                except ValueError:
                    messagebox.showerror(f"Error: {key} field must be a float")
                    return
                if self.fields[key].get() == "":
                    messagebox.showerror(f"Error: {key} field is empty")
                    return
        if type == 'add':
            dickey = newMonster['Name']
            self.creatureDict[dickey] = newMonster
            self.hasAbilityDict[dickey] = self.creatureAbilities
        if type == 'export':
            monData = {'monster':newMonster, 'monsterAbilities':self.creatureAbilities}
            filePath = filedialog.asksaveasfilename(defaultextension='.pkl')
            with open(filePath, 'wb') as f:
                pickle.dump(monData, f)

    def importMon(self):
        monData = {}
        filePath = filedialog.askopenfilename()
        if filePath:
            with open(filePath, 'rb') as f:
                monData = pickle.load(f)
        self.creatureAbilities = monData['monsterAbilities']
        newMonster = monData['monster']
        dickey = newMonster['Name']
        self.creatureDict[dickey] = newMonster
        self.hasAbilityDict[dickey] = self.creatureAbilities
    
    def addAbility(self):
        ability = self.abilityFieldVal.get()
        if ability not in self.creatureAbilities:
            self.creatureAbilities.append(ability)
            self.abilityListBox.insert(tk.END, ability)
        print(self.creatureAbilities)

    def removeAbility(self):
        selectedIndex = self.abilityListBox.curselection()
        if selectedIndex:
            selectedAbility = self.abilityListBox.get(selectedIndex[0])
            self.abilityListBox.delete(selectedIndex[0])
            if selectedAbility in self.creatureAbilities:
                self.creatureAbilities.remove(selectedAbility)
        print(self.creatureAbilities)


    def help(self):
        readme_file = "README.md"
        if os.path.isfile(readme_file):
            webbrowser.open(readme_file)
        else:
            messagebox.showerror(f"Error: {readme_file} not found")

            return
        
if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(400, 300)
    app = MonsterSelectGUI(root)
    root.mainloop()


