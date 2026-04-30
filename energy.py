class EnergyManager:
    def __init__(self, total_energy):
        self.total = total_energy
        self.remaining = total_energy

    def allocate(self, amount):
        if self.remaining >= amount:
            self.remaining -= amount
            return True
        return False

    def reset(self):
        self.remaining = self.total