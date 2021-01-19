from ..api.api_db import ApiDB
from ..warship.warship_db import WarshipDB


def create_image_db():
	shipsdb = WarshipDB()
	db = ApiDB()
	db.process_images(shipsdb)