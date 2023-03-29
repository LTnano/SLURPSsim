import pickle

# load the dictionary from the file using pickle
with open('fightplannerinfo.pkl', 'rb') as f:
    data = pickle.load(f)

# access the lists using their keys
list1 = data['teamList']
list2 = data['chosenList']
list3 = data['creatureDict']
list4 = data['hasAbilityDict']

# print the lists
print(list1)
print(list2)
print(list3)
print(list4)