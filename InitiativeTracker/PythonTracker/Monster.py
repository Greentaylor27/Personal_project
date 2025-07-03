class Monster:

    def __init__(self, name, health, initiative):
        self.name = name
        self.health = health
        self.initiative = initiative
        self.is_alive = True
    
    def __str__(self):
        status = "Alive" if self.is_alive else "Dead"
        return f"{self.name} (Health: {self.health}, Initiative: {self.initiative}, Status: {status})"

    