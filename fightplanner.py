import pickle
import tkinter as tk

# Name, Health | Strength, Endurance, Coordination, Dexterity, Intelligence, Nouse, Will | Weapon, Ranged Weapon | Armour, Ability Points



class MonsterSelectGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Monster Select")
        self.teamOne = []
        self.teamTwo = []
        self.chosenList = []
        self.teamList = []
        self.creatureDict = {'giantRat' : {'Name': 'Giant Rat', 'HP' : 50, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 8, 'INT' : 2, 'NOU' : 4, 'WIL' : 3, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 0, 'AP' : 0},

        'meleeSkeleton' : {'Name' : 'Skeleton', 'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 2, 'AP' : 0},

        'meleeSkeletonH' : {'Name' : 'Skeleton (Hard)', 'HP' : 140, 'STR' : 11, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 2, 'AP' : 9},

        'rangedSkeleton' : {'Name': 'Skeleton Archer', 'HP' : 110, 'STR' : 8, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 4, 'ARM' : 0, 'AP' : 9},

        'rangedSkeletonH' : {'Name' : 'Skeleton Archer(Hard)', 'HP' : 110, 'STR' : 8, 'END' : 14, 'COR' : 11, 'DEX' : 10, 'INT' : 5, 'NOU' : 8, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 6, 'ARM' : 0, 'AP' : 7},

        'wizardSkeleton' : {'Name': 'Skeleton Wizard', 'HP' : 100, 'STR' : 7, 'END' : 8, 'COR' : 8, 'DEX' : 7, 'INT' : 11, 'NOU' : 6, 'WIL' : 2, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 10},

        'meleeKobold' : {'Name': 'Kobold Warrior', 'HP' : 60, 'STR' : 9, 'END' : 6, 'COR' : 8, 'DEX' : 5, 'INT' : 5, 'NOU' : 6, 'WIL' : 4, 'WEA' : 4, 'RWEA' : 0, 'ARM' : 1, 'AP' : 0},

        'wizardKobold' : {'Name': 'Kobold Mage', 'HP' : 40, 'STR' : 6, 'END' : 6, 'COR' : 7, 'DEX' : 7, 'INT' : 10, 'NOU' : 7, 'WIL' : 8, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 7},

        'rangedKobold' : {'Name': 'Kobold Archer', 'HP' : 40, 'STR' : 8, 'END' : 5, 'COR' : 8, 'DEX' : 9, 'INT' : 8, 'NOU' : 6, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 4, 'ARM' : 0, 'AP' : 6},

        'priestKobold' : {'Name': 'Kobold Healer', 'HP' : 30, 'STR' : 3, 'END' : 5, 'COR' : 8, 'DEX' : 9, 'INT' : 7, 'NOU' : 6, 'WIL' : 7, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 7},

        'summonerKobold' : {'Name' : 'Kobold Summoner', 'HP' : 100, 'STR' : 5, 'END' : 5, 'COR' : 10, 'DEX' : 10, 'INT' : 10, 'NOU' : 9, 'WIL' : 10, 'WEA' : 0, 'RWEA' : 0, 'ARM' : 0, 'AP' : 0},

        'slowGolem' : {'Name': 'Golem', 'HP' : 300, 'STR' : 14, 'END' : 30, 'COR' : 8, 'DEX' : 4, 'INT' : 2, 'NOU' : 2, 'WIL' : 2, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 5, 'AP' : 0},

        'thinBilly' : {'Name' : 'Thin Billy', 'HP' : 200, 'STR' : 13, 'END' : 20, 'COR' : 13, 'DEX' : 13, 'INT' : 13, 'NOU' : 17, 'WIL' : 13, 'WEA' : 8, 'RWEA' : 0, 'ARM' : 2, 'AP' : 10},
                
        'bossSkeleton' : {'Name' : 'Captain Boney', 'HP' : 250, 'STR' : 15, 'END' : 25, 'COR' : 15, 'DEX' : 12, 'INT' : 17, 'NOU' : 12, 'WIL' : 13, 'WEA' : 6, 'RWEA' : 0, 'ARM' : 5, 'AP' : 12},
                
        'testMonster' : {'Name' : 'Jack', 'HP' : 400, 'STR' : 20, 'END' : 30, 'COR' : 20, 'DEX' : 20, 'INT' : 20, 'NOU' : 20, 'WIL' : 20, 'WEA' : 8, 'RWEA' : 8, 'ARM' : 10, 'AP' : 25}}

        self.hasAbilityDict = {'giantRat' : ['STRIKE'],

        'meleeSkeleton' : ['STRIKE'],

        'meleeSkeletonH' : ['STRIKE', 'FEINT'],

        'rangedSkeleton' : ['SHOOT'],

        'rangedSkeletonH' : ['SHOOT'],

        'wizardSkeleton' : ['FIREBALL 2'],

        'meleeKobold' : ['STRIKE'],

        'wizardKobold' : ['FIREBALL'],

        'rangedKobold' : ['SHOOT'],

        'priestKobold' : ['HEADACHE'],

        'summonerKobold' : ['CONJURE RAT'],

        'slowGolem' : ['STRIKE'],

        'thinBilly' : ['STRIKE', 'HEAL'],
                
        'bossSkeleton' : ['STRIKE', 'FIREBALL', 'HEAL'],
                
        'testMonster' : ['STRIKE', 'FIREBALL 2', 'FIREBALL 3', 'FIREBALL', 'FIRESTORM', 'HEAL', 'HEAL 2', 'ENCOURAGE', 'FLATTEN', 'STUN 2', 'BLOCK 2', 'DEAD MAN WALKING', 'ROUSING SHOUT', 'ROUSING SONG']}


        # Create the monster listbox
        self.monsterListBox = tk.Listbox(self.window, selectmode=tk.MULTIPLE)
        for name in self.creatureDict:
            self.monsterListBox.insert(tk.END, self.creatureDict[name]['Name'])
        self.monsterListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the add/remove buttons
        self.addLeftButton = tk.Button(self.window, text="Add to Left Team", command=self.addLeft)
        self.addRightButton = tk.Button(self.window, text="Add to Right Team", command=self.addRight)
        self.removeLeftButton = tk.Button(self.window, text="Remove from Left Team", command=self.removeLeft)
        self.removeRightButton = tk.Button(self.window, text="Remove from Right Team", command=self.removeRight)
        self.addLeftButton.pack(side=tk.TOP, padx=5, pady=5)
        self.addRightButton.pack(side=tk.TOP, padx=5, pady=5)
        self.removeLeftButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.removeRightButton.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create the export button
        self.exportButton = tk.Button(self.window, text="Export Teams", command=self.exportTeams)
        self.exportButton.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create the team listboxes
        self.teamOneListBox = tk.Listbox(self.window)
        self.teamTwoListBox = tk.Listbox(self.window)
        self.teamOneListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.teamTwoListBox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
        # Export the lists
        for item in self.teamOne:
            self.chosenList.append(item)
            self.teamList.append(1)
        for item in self.teamTwo:
            self.chosenList.append(item)
            self.teamList.append(2)
        data = {'teamList': self.teamList, 'chosenList': self.chosenList, 'creatureDict': self.creatureDict, 'hasAbilityDict': self.hasAbilityDict}
        with open('fightplannerinfo.pkl', 'wb') as f:
            pickle.dump(data, f)


if __name__ == '__main__':
    MonsterSelectGUI().window.mainloop()

