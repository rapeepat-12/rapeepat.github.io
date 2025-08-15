import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import math

SAVE_FILE = "progress.json"

# Initialize rarities: each rarity 3x rarer than the previous
rarities = []
base_chance = 0.5  # Example starting chance for rarity 1
for i in range(1, 1001):
    rarities.append({
        "name": f"Rarity {i}",
        "base_chance": base_chance,
    })
    base_chance /= 3  # each rarity 3x rarer

# Initialize or load progress
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        progress = json.load(f)
else:
    progress = {
        "lp": 0,
        "pp": 0,
        "tp": 0,
        "best_rarity": 1
    }

def save_progress():
    with open(SAVE_FILE, "w") as f:
        json.dump(progress, f)

def calculate_actual_chances():
    actual_chances = []
    luck_multiplier = progress["lp"]
    for r in rarities:
        actual = r["base_chance"] * luck_multiplier
        actual_chances.append(actual)
    return actual_chances

def get_roll_result():
    actual_chances = calculate_actual_chances()
    # Apply cap rule: if actual chance >=1, pick highest below 1
    capped_chances = [ac if ac < 1 else 0 for ac in actual_chances]
    total_weight = sum(capped_chances)
    if total_weight == 0:  # fallback if all ≥1
        return len(rarities)
    r = random.uniform(0, total_weight)
    for i, ac in enumerate(capped_chances):
        r -= ac
        if r <= 0:
            return i + 1
    return len(rarities)

def roll():
    rarity_index = get_roll_result()
    # Update best rarity if higher
    if rarity_index > progress["best_rarity"]:
        progress["best_rarity"] = rarity_index
    # Apply LP boost: LP gives +2×LP luck (for simplicity, 1 LP = 2 luck multiplier)
    progress["lp"] += 1  # Example increment per roll
    # Update GUI
    update_display()
    save_progress()

def reset_best():
    best = progress["best_rarity"]
    if best <= 1:
        messagebox.showinfo("Reset", "No rarity to reset!")
        return
    # LP gain: Common=0, Uncommon=1, Rare=2, etc.
    lp_gain = best - 1
    progress["lp"] += lp_gain
    # Prestige boosts
    if best >= 10:
        pp_gain = math.ceil(best ** 0.5)
        progress["pp"] += pp_gain
    if best >= 20:
        tp_gain = math.ceil((best ** 0.75) + 1)
        progress["tp"] += tp_gain
    # Reset best rarity
    progress["best_rarity"] = 1
    update_display()
    save_progress()

def update_display():
    actual_chances = calculate_actual_chances()
    chance_text = "\n".join([f"{r['name']}: {min(ac,1):.3f}" for r, ac in zip(rarities, actual_chances)])
    display_text.set(
        f"Best Rarity: {progress['best_rarity']}\n"
        f"LP: {progress['lp']} | PP: {progress['pp']} | TP: {progress['tp']}\n\n"
        f"Actual Chances (top 10 shown):\n" + "\n".join(chance_text.split("\n")[:10])
    )

# GUI setup
root = tk.Tk()
root.title("Luck Simulator")
root.geometry("500x600")

display_text = tk.StringVar()
label = tk.Label(root, textvariable=display_text, justify="left", font=("Consolas", 12))
label.pack(pady=20)

roll_btn = tk.Button(root, text="Roll", command=roll, width=20, height=2)
roll_btn.pack(pady=5)

reset_btn = tk.Button(root, text="Reset Best (W)", command=reset_best, width=20, height=2)
reset_btn.pack(pady=5)

# Key bindings for W/E/R
def key_press(event):
    if event.char.lower() == "w":
        reset_best()
    elif event.char.lower() == "e":
        # Prestige if best rarity >=15
        if progress["best_rarity"] >= 15:
            messagebox.showinfo("Prestige", "Prestige applied!")
    elif event.char.lower() == "r":
        if progress["best_rarity"] >= 30:
            messagebox.showinfo("Transcend", "Transcend applied!")

root.bind("<Key>", key_press)

update_display()
root.mainloop()

