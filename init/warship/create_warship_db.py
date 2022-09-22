from ..api.api_db import ApiDB
from ..gp.gp_db import GameparamsDB
from ..i18n.i18n_db import I18NDb
from .warship_db import WarshipDB

path = 'res/warships.sqlite'


def create_warships_db():
	apidb = ApiDB()
	gpm = GameparamsDB()
	warshipdb = WarshipDB()
	i18n = I18NDb()
	warshipdb.init_db()

	ship_ids = apidb.list_all_ships()
	ships = []
	for name, ship_id_str in ship_ids:
		ship = gpm.search_ship(ship_id_str, i18n)
		ships.append((ship, name))
	warshipdb.insert_data(ships)
