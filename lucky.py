import tkinter as tk
import random
import math

# Generate rarities
rarities = []
chance = 50.0
for i in range(1, 101):
    rarities.append({"name": f"Rarity {i}", "tier": i, "chance": chance})
    chance /= 3  # each rarity 3x rarer

# Player stats
LP = 0
PP = 0
TP = 0
best_rarity = 1
roll_history = []

# Multipliers
def calculate_multipliers():
    luck_multiplier = 1 + LP * 2
    lp_multiplier = 1
    pp_multiplier = 1
    
    if PP > 0:
        lp_multiplier += math.ceil(PP ** 0.5)
        luck_multiplier = luck_multiplier ** math.ceil(PP ** 0.5)
    if TP > 0:
        pp_multiplier += math.ceil(TP ** 0.5)
        lp_multiplier += math.ceil(1 + TP ** (2/3))
        luck_multiplier += math.ceil(TP ** (3/4))
    return luck_multiplier, lp_multiplier, pp_multiplier

# Roll rarity
def roll():
    global best_rarity, roll_history
    luck_multiplier, _, _ = calculate_multipliers()
    total_weight = sum(r["chance"] * luck_multiplier for r in rarities)
    r = random.uniform(0, total_weight)
    selected = rarities[0]
    for rarity in rarities:
        r -= rarity["chance"] * luck_multiplier
        if r <= 0:
            selected = rarity
            break
    roll_history.insert(0, f"Rolled {selected['name']}")
    roll_history[:] = roll_history[:10]
    if selected["tier"] > best_rarity:
        best_rarity = selected["tier"]
    update_display()

# Reset LP
def reset_lp():
    global LP, best_rarity
    LP += best_rarity - 1  # Common gives 0, Uncommon 1, etc.
    update_display()

# Prestige at tier 15
def prestige():
    global PP, best_rarity, LP
    if best_rarity >= 15:
        PP += 1
        best_rarity = 1
        LP = 0
        update_display()

# Transcend at tier 30
def transcend():
    global TP, best_rarity, LP, PP
    if best_rarity >= 30:
        TP += 1
        best_rarity = 1
        LP = 0
        PP = 0
        update_display()

# Display
def update_display():
    luck_multiplier, lp_multiplier, pp_multiplier = calculate_multipliers()
    status_text.set(
        f"LP: {LP} | PP: {PP} | TP: {TP} | Best Rarity: {best_rarity}\n"
        f"Luck Multiplier: {luck_multiplier} | LP Multiplier: {lp_multiplier} | PP Multiplier: {pp_multiplier}\n"
        f"Recent Rolls: {', '.join(roll_history[:5])}"
    )

# Key bindings
def key_press(event):
    if event.char.lower() == 'w':
        reset_lp()
    elif event.char.lower() == 'e':
        prestige()
    elif event.char.lower() == 'r':
        transcend()

# GUI setup
root = tk.Tk()
root.title("Luck Simulator")
root.geometry("600x300")
status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text, justify="left", font=("Consolas", 12))
status_label.pack(pady=20)

roll_button = tk.Button(root, text="Roll", command=roll, font=("Consolas", 14))
roll_button.pack()

root.bind("<Key>", key_press)

update_display()
root.mainloop()
