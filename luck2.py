import tkinter as tk
import random

# --- Generate 100 rarities ---
rarities = []
base_chance = 50
for i in range(1, 101):
    name = f"Rarity {i}"
    chance = max(base_chance * (0.95 ** (i-1)), 0.01)
    value = i
    lp = i // 2  # Luck Points gained on reset
    rarities.append({
        "name": name,
        "chance": chance,
        "value": value,
        "lp": lp
    })

# --- Player state ---
current_rarity = rarities[0]
best_rarity_value = 0
luck_points = 0
prestige_points = 0
transcendent_points = 0
roll_history = []

# --- Functions ---
def roll_rarity():
    global current_rarity, best_rarity_value, roll_history
    total_weight = sum(r["chance"] for r in rarities)
    r = random.uniform(0, total_weight)
    selected = rarities[0]
    for rarity in rarities:
        r -= rarity["chance"]
        if r <= 0:
            selected = rarity
            break
    current_rarity = selected
    if selected["value"] > best_rarity_value:
        best_rarity_value = selected["value"]
    roll_history.insert(0, f"Rolled {selected['name']}")
    roll_history[:] = roll_history[:10]  # keep last 10
    update_display()

def reset_best_rarity():
    global luck_points, best_rarity_value
    # Find rarity index
    rarity_index = best_rarity_value - 1
    if rarity_index < 0:
        return
    # Gain LP based on rarity
    lp_gain = rarities[rarity_index]["lp"]
    luck_points += lp_gain
    roll_history.insert(0, f"Reset {rarities[rarity_index]['name']} -> +{lp_gain} LP")
    # Reset best rarity
    best_rarity_value = 0
    update_display()

def prestige():
    global prestige_points, best_rarity_value
    if best_rarity_value >= 15:
        prestige_points += 1
        roll_history.insert(0, f"Prestige! +1 PP")
        # Reset best rarity
        best_rarity_value = 0
        update_display()

def transcend():
    global transcendent_points, best_rarity_value
    if best_rarity_value >= 30:
        transcendent_points += 1
        roll_history.insert(0, f"Transcend! +1 TP")
        # Reset best rarity
        best_rarity_value = 0
        update_display()

def update_display():
    rarity_label.config(text=f"Current Rarity: {current_rarity['name']}")
    best_label.config(text=f"Best Rarity: {best_rarity_value}")
    lp_label.config(text=f"Luck Points: {luck_points}")
    pp_label.config(text=f"Prestige Points: {prestige_points}")
    tp_label.config(text=f"Transcendent Points: {transcendent_points}")
    history_text.config(state="normal")
    history_text.delete("1.0", tk.END)
    for entry in roll_history:
        history_text.insert(tk.END, entry + "\n")
    history_text.config(state="disabled")

def on_key(event):
    key = event.keysym.lower()
    if key == "w":
        reset_best_rarity()
    elif key == "e":
        prestige()
    elif key == "r":
        transcend()

# --- GUI ---
root = tk.Tk()
root.title("Luck Simulator")

roll_button = tk.Button(root, text="Roll", command=roll_rarity, width=20, height=2)
roll_button.pack(pady=5)

rarity_label = tk.Label(root, text=f"Current Rarity: {current_rarity['name']}")
rarity_label.pack()

best_label = tk.Label(root, text=f"Best Rarity: {best_rarity_value}")
best_label.pack()

lp_label = tk.Label(root, text=f"Luck Points: {luck_points}")
lp_label.pack()

pp_label = tk.Label(root, text=f"Prestige Points: {prestige_points}")
pp_label.pack()

tp_label = tk.Label(root, text=f"Transcendent Points: {transcendent_points}")
tp_label.pack()

history_label = tk.Label(root, text="Roll History:")
history_label.pack()

history_text = tk.Text(root, height=10, width=40, state="disabled")
history_text.pack()

root.bind("<Key>", on_key)

update_display()
root.mainloop()
