class Artillery:
    """
    Artillery class, for AP, HE, SAP projectiles not main guns.
    """
    def __init__(self, d:dict) -> None:
        self.alphadmg = d['alphadmg']
        self.ammotype = d['ammotype']
        self.ricochet = d['ricochet']
        self.speed = d['speed']
        self.burnprob = d['burnprob']
        self.dmg = d['dmg']
        self.index = d['index']
    

    def to_dict(self):
        d = {
            'alphadmg': self.alphadmg,
            'ammotype': self.ammotype,
            'ricochet': self.ricochet,
            'speed': self.speed,
            'burnprob': self.burnprob,
            'dmg': self.dmg,
            'index': self.index
        }
        return d


    @classmethod
    def from_data(cls, data):
        d = {
            'alphadmg': data['alphaDamage'],
            'ammotype': data['ammoType'],
            'ricochet': data['bulletRicochetAt'],
            'speed': data['bulletSpeed'],
            'burnprob': data['burnProb'],
            'dmg': data['damage'],
            'index': data['index']
        }
        art = cls(d)
        return art