import json

torp_path = 'wows/torps.json'

def get_torp(name:str):
	"""
	Get torp:dict of given name.
	"""
	with open(torp_path, 'r') as f:
		s = f.read()
	s_jsn = json.loads(s)
	return s_jsn[name.strip()]
