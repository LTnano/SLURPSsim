import tkinter as tk
import random

# created entirely with prompts into chatGPT to learn tkinter
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

D100 = Die(100, 'D100')
D20 = Die(20, 'D20')
D12 = Die(12, 'D12')
D10 = Die(10, 'D10')
D8 = Die(8, 'D8')
D6 = Die(6, 'D6')
D4 = Die(4, 'D4')
D2 = Die(2, 'D2/COIN')

class DiceRoller:
    def __init__(self, master):
        self.master = master
        master.title("Dice Roller")

        self.dice_label = tk.Label(master, text="Select dice:")
        self.dice_label.pack()

        self.dice_var = tk.StringVar()
        self.dice_var.set("D20")

        self.dice_options = [(D100.name, D100), (D20.name, D20), (D12.name, D12), (D10.name, D10), (D8.name, D8), (D6.name, D6), (D4.name, D4), (D2.name, D2)]
        for name, die in self.dice_options:
            tk.Radiobutton(master, text=name, variable=self.dice_var, value=name).pack()

        self.num_dice_label = tk.Label(master, text="Number of dice:")
        self.num_dice_label.pack()

        self.num_dice_entry = tk.Entry(master)
        self.num_dice_entry.pack()

        self.roll_button = tk.Button(master, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack()

        self.results_label = tk.Label(master, text="Results:")
        self.results_label.pack()

        self.results_text = tk.Text(master, height=10, width=30)
        self.results_text.pack()

        self.total_label = tk.Label(master, text="Total:")
        self.total_label.pack()

        self.total_text = tk.Label(master, text="0")
        self.total_text.pack()

        self.average_label = tk.Label(master, text="Average:")
        self.average_label.pack()

        self.average_text = tk.Label(master, text="0")
        self.average_text.pack()

    def roll_dice(self):
        dice_name = self.dice_var.get()
        num_dice = int(self.num_dice_entry.get())
        die = None

        for name, d in self.dice_options:
            if name == dice_name:
                die = d
                break

        if die is None:
            return

        results = []
        total = 0
        for i in range(num_dice):
            result = die.roll()
            results.append(result)
            total += result

        average = round(die.average(), 2) * num_dice
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, str(results))
        self.total_text.config(text=str(total))
        self.average_text.config(text=str(average))

root = tk.Tk()
app = DiceRoller(root)
root.mainloop()
