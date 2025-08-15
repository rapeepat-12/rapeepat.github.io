import random

# Define rarities
rarities = [
    {"name": "Common", "chance": 50, "lp": 1, "pp": 0, "tp": 0},
    {"name": "Uncommon", "chance": 25, "lp": 5, "pp": 0, "tp": 0},
    {"name": "Rare", "chance": 15, "lp": 25, "pp": 1, "tp": 0},
    {"name": "Epic", "chance": 7, "lp": 125, "pp": 5, "tp": 0},
    {"name": "Legendary", "chance": 2.5, "lp": 625, "pp": 25, "tp": 1},
    {"name": "Mythic", "chance": 0.5, "lp": 3125, "pp": 125, "tp": 5},
]

# Initialize points and history
luck_points = 0
prestige_points = 0
transcendent_points = 0
roll_history = []

def roll_rarity():
    global luck_points, prestige_points, transcendent_points, roll_history

    # Lucky Skip (1% chance)
    if random.random() < 0.01:
        roll_history.insert(0, "🍀 Lucky Skip! Skipped this roll")
        roll_history = roll_history[:5]
        print("Lucky Skip! Roll skipped.")
        return

    # Weighted random selection
    total_weight = sum(r["chance"] for r in rarities)
    r = random.uniform(0, total_weight)
    selected = rarities[0]

    for rarity in rarities:
        r -= rarity["chance"]
        if r <= 0:
            selected = rarity
            break

    # Award points
    luck_points += selected["lp"]
    prestige_points += selected["pp"]
    transcendent_points += selected["tp"]

    # Update history
    roll_history.insert(0, f"Rolled {selected['name']}")
    roll_history = roll_history[:5]

    print(f"You rolled: {selected['name']}")

def show_status():
    print("\nCurrent Status:")
    print(f"Luck Points: {luck_points}")
    print(f"Prestige Points: {prestige_points}")
    print(f"Transcendent Points: {transcendent_points}")
    print("Recent Rolls:")
    for r in roll_history:
        print(f" - {r}")
    print()

# Main loop
def main():
    print("Welcome to the Luck Simulator!\n")
    while True:
        action = input("Press Enter to roll, 's' to show status, or 'q' to quit: ").lower()
        if action == 'q':
            print("Thanks for playing!")
            break
        elif action == 's':
            show_status()
        else:
            roll_rarity()

if __name__ == "__main__":
    main()
