import json

from utils.database import Database

from gameparams.warship import Warship

path = 'res/warships.db'


class WarshipDB:
    def __init__(self) -> None:
        self.db = Database(path)
    

    def init_db(self):
        """
        Initialize database.
        """
        # clear data
        with open(path, 'w') as f:
            f.write('')
        
        # create table
        command = 'CREATE TABLE warship(' \
            'nickname TEXT,' \
            'idx TEXT,' \
            'shipid INTEGER PRIMARY KEY,' \
            'tier INTGER,' \
            'species TEXT,' \
            'nation TEXT,' \
            'mods TEXT,' \
            'artilleries TEXT,' \
            'engines TEXT,' \
            'firecontrols TEXT,' \
            'hulls TEXT,' \
            'torpedoes TEXT)'
        self.db.execute(command)
        

    def insert_data(self, ships:list):
        """
        Insert data into database.
        """
        # list for command, value
        l = []
        for ship, nickname in ships:
            # some ships not implemented yet
            if not ship:
                continue
            values = (
                nickname,
                ship.index,
                ship.shipid,
                ship.tier,
                ship.species,
                ship.nation,
                json.dumps(ship.mods, indent=4),
                json.dumps(ship.artilleries, indent=4),
                json.dumps(ship.engines, indent=4),
                json.dumps(ship.firecontrols, indent=4),
                json.dumps(ship.hulls, indent=4),
                json.dumps(ship.torpedoes, indent=4))
            command = 'INSERT INTO warship(' \
                'nickname,' \
                'idx,' \
                'shipid,' \
                'tier,' \
                'species,' \
                'nation,' \
                'mods,' \
                'artilleries,' \
                'engines,' \
                'firecontrols,' \
                'hulls,' \
                'torpedoes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
            l.append((command, values))
        self.db.insertmany(l)


    