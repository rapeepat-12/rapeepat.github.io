import tkinter as tk
import random

# Define rarities
rarities = [
    {"name": "Common", "chance": 50, "lp": 0, "value": 0},
    {"name": "Uncommon", "chance": 25, "lp": 1, "value": 1},
    {"name": "Rare", "chance": 15, "lp": 2, "value": 2},
    {"name": "Epic", "chance": 7, "lp": 3, "value": 3},
    {"name": "Legendary", "chance": 2.5, "lp": 5, "value": 5},
    {"name": "Mythic", "chance": 0.5, "lp": 10, "value": 10}
]

# Points
luck_points = 0
prestige_points = 0
transcendent_points = 0
current_rarity = rarities[0]
roll_history = []

# Functions
def roll_rarity():
    global current_rarity, roll_history
    total_weight = sum(r["chance"] for r in rarities)
    r = random.uniform(0, total_weight)
    selected = rarities[0]

    for rarity in rarities:
        r -= rarity["chance"]
        if r <= 0:
            selected = rarity
            break

    current_rarity = selected
    roll_history.insert(0, f"Rolled {selected['name']}")
    roll_history_display()
    update_status()

def reset_rarity():
    global luck_points, current_rarity
    luck_points += current_rarity["value"]
    current_rarity = rarities[0]
    roll_history_display()
    update_status()

def prestige():
    global prestige_points, luck_points
    if current_rarity["value"] >= 15:
        prestige_points += 1
        luck_points = 0
    update_status()

def transcendent():
    global transcendent_points, prestige_points
    if current_rarity["value"] >= 30:
        transcendent_points += 1
        prestige_points = 0
    update_status()

def update_status():
    status_label.config(text=f"Current Rarity: {current_rarity['name']}\n"
                             f"Luck Points: {luck_points}\n"
                             f"Prestige Points: {prestige_points}\n"
                             f"Transcendent Points: {transcendent_points}")

def roll_history_display():
    history_text = "\n".join(roll_history[:5])
    history_label.config(text=f"Recent Rolls:\n{history_text}")

# GUI setup
root = tk.Tk()
root.title("Luck Simulator")

status_label = tk.Label(root, text="", font=("Arial", 14))
status_label.pack(pady=10)

roll_button = tk.Button(root, text="Roll", command=roll_rarity, width=20)
roll_button.pack(pady=5)

reset_button = tk.Button(root, text="Reset (w)", command=reset_rarity, width=20)
reset_button.pack(pady=5)

prestige_button = tk.Button(root, text="Prestige (e)", command=prestige, width=20)
prestige_button.pack(pady=5)

transcend_button = tk.Button(root, text="Transcend (r)", command=transcendent, width=20)
transcend_button.pack(pady=5)

history_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
history_label.pack(pady=10)

update_status()
root.mainloop()
