# SLURPS simulator

this sim aims to assist in planning a slurps adventure

## Usage

Use fightplanner.py to create two teams and fill them with monsters, just export your team and give it a name. There is a folder named fightplans where some existing templates exist.

Monsters can be saved to the extramonsters folder and loaded back in to the fight planner.
When exporting a monster, remember to also click 'add monster' as exporting does not automatically add it to the dictionary.

Once you have exported, run the slurps.py file and choose your exported fightplan. The fight will run simulations equal to the number specified and generate a log in the logs folder of the final fight, along with a winrate.

## Fields

Name = Name of the creature - String
HP = Health maximum - Integer
STR = Strength - Integer
END = Endurance - Integer
COR = Coordination - Integer
DEX = Dexterity - Integer
INT = Intelligence - Integer
NOU = Nouse - Integer
WIL = Will - Integer
WEA = Melee Weapon - Integer (0, 2, 4, 6, 8, 10, 12 or 20)
RWEA = Ranged Weapon - Integer (0, 2, 4, 6, 8, 10, 12 or 20)
ARM = Armour - Integer
AP = Action points maximum -  Integer

