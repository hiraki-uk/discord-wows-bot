import json

remove_list = [
    'costCR', 'costGold', 'group', 'id', 'index', 'typeinfo'
]

class Module:
    def __init__(self, d:dict):
            self.name = d['name']
            self.shiplevel = d['shiplevel']
            self.ships = d['ships']
            self.nation = d['nation']
            self.shiptype = d['shiptype']
            self.excludes = d['excludes']
            self.slot = d['slot']
            self.text = d['text']
            self.stats = d['stats']


    def to_dict(self):
        temp = {
            'name': self.name,
            'shiplevel': self.shiplevel,
            'ships': self.ships,
            'nation': self.nation,
            'shiptype': self.shiptype,
            'excludes': self.excludes,
            'slot': self.slot,
            'text': self.text,
            'stats': self.stats
        }
        return temp


    def simplified(self, i18n):
        """
        Returns simplified data for storing in database.
        """
        
        d = {'name': i18n.get_msgstr(self.name), 
            'slot': self.slot, 
            'stats': self.stats
        }
        return d


    @classmethod
    def from_data(cls, data:dict):
        """
        Creates module instance of given data.
        Use for creating mods from data in gameparams database.
        """
        with open('res/base_module.json' ,'r') as f:
            temp = f.read()
        base_module = json.loads(temp)
        name = ''
        shiplevel = []
        ships = []
        nation = []
        shiptype = []
        excludes = []
        
        slot = -2
        text = None
        stats = []

        for key, value in data.items():
            # for key, compare with base value
            base_value = base_module[key]
            if base_value != value:
                if key == 'shiplevel':
                    shiplevel = value
                elif key == 'ships':
                    ships = value
                elif key == 'nation':
                    nation = value
                elif key == 'shiptype':
                    shiptype = value
                elif key == 'excludes':
                    excludes = value
                elif key == 'slot':
                    slot = value
                elif key == 'name':
                    name = value
                else:
                    # remove unneccesary data
                    if key not in remove_list:
                        stats.append((key, value))

        with open('res/stats_translation.json', 'r', encoding='utf8') as f:
            translations = json.load(f)
        # fill text
        text = ','.join([f'{translations[stat[0]]}:{stat[1]}' for stat in stats])
        temp = {
            'name': name,
            'shiplevel': shiplevel,
            'ships': ships,
            'nation': nation,
            'shiptype': shiptype,
            'excludes': excludes,
            'slot': slot,
            'text': text,
            'stats': stats
        }    
        mod = cls(temp)
        return mod