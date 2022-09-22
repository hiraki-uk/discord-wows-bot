import polib
from utils.database import Database

path = 'res/i18n.sqlite'
mopath = 'res/global.mo'

def create_i18n_db():
    """
    Creates i18n db.
    """
    db = I18NDb()
    db.init_db()
    po = polib.mofile(mopath)
    # list for storing i18n data
    entries = [(entry.msgid, entry.msgstr) for entry in po]
    db.insert_data(entries)


class I18NDb:
    def __init__(self) -> None:
        self.db = Database(path)
    

    def init_db(self):
        """
        Initialize database.
        """
        # clear data
        self.db.execute('DROP TABLE IF EXISTS message')
        
        # create table
        command = 'CREATE TABLE message(' \
            'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
            'msgid TEXT,' \
            'msgstr TEXT)'
        self.db.execute(command)

    
    def insert_data(self, entries):
        command = 'INSERT INTO message (msgid, msgstr) VALUES (?,?)'
        l = [(command, entry) for entry in entries]
        self.db.insertmany(l)
        
    
    def get_msgstr(self, msgid):
        command = 'SELECT msgstr from message WHERE msgid LIKE ?'
        result = self.db.fetchone(command, (f'IDS_TITLE_{msgid}%',))
        if not result:
            return
        if not len(result) == 1:
            return
        return result[0]
