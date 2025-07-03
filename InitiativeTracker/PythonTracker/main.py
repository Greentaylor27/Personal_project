from Monster import Monster
from Tracker import InitiativeTracker

tracker = InitiativeTracker()

num_monsters = int(input("Enter the number of monsters: "))
monster_name = input("Enter the name of the monster: ")
monster_health = int(input("Enter the health of the monster: "))
if num_monsters <= 0:
    print("Number of monsters must be greater than 0.")
    exit()
elif num_monsters == 1:

    monster_initiative = int(input("Enter the initiative of the monster: "))

for i in range(num_monsters):
    m = Monster(f"{monster_name} {i + 1}", monster_health, monster_initiative)
    tracker.add_to_initiative(m)

if __name__ == "__main__":
    tracker.add_to_initiative(Monster(monster_name, monster_health, monster_initiative, monster_status="Alive"))
    print("\nInitiative:")
    tracker.list_initiative()
    