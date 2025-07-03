class InitiativeTracker:
  def __init__(self):
    """Initializes the Initiative Tracker."""
    self.initative = []  # List to hold characters in initiative order

  def add_to_initiative(self, character):
    """Adds a object to the initiative list. (Monster or Player)"""
    self.initative.append(character)  # Adds the character to the initiative list
    self.initative.sort(key=lambda x: x.initiative, reverse=True) # sorts the initiative list in descending order based on the initiative value

  def list_initative(self):
    """Lists the characters in initiative order."""
    return [character.name for character in self.initative]  # Returns a list of character names in initiative order