
# ----------- parent class ---------------
class Character:
  def __init__(self, name: str, health: int) -> None:
    self.name = name
    self.health = health
    self.max_health = health