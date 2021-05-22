from os import path
from utils.database import Database

from ..api.api import Api

path = 'res/maps.db'
def create_map_db():
    """
    Create maps.db file.
    """
    db = MapDB()
    db.init_db()
    api = Api()
    maps = api.fetch_maps()
    db.insert_data(maps)


class MapDB:
    def __init__(self) -> None:
        self.db = Database(path)
    

    def init_db(self):
        self.db.execute('DROP TABLE IF EXISTS maps')
        self.db.executescript("""
        CREATE TABLE maps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            img BLOB)""")
    
    
    def insert_data(self, maps):
        command = 'INSERT INTO maps (name, img) VALUES (?,?)'
        l = [
            (command, (name, img)) for name, img in maps.items()
        ]
        self.db.insertmany(l)


    def get_image(self, name):
        results = self.db.fetchall(
            f'SELECT name, img FROM maps WHERE name LIKE ?',
            (f'%{name}%',))
        # one hit, return it
        if len(results) == 1:
            img = results[0][1]
            return img
        else:
            names = [result[0] for result in results]
            # if exact match found
            for result in results:
                if name.lower() == result[0].lower():
                    img = result[1]
                    return img
            return names