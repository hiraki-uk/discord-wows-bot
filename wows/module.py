import json
torp_ids_path = 'wows/torp_ids.txt'
torp_path = 'wows/torps.json'

def get_torp(name:str):
	with open(torp_path, 'r') as f:
		s = f.read()
	s_jsn = json.loads(s)
	return s_jsn[name.strip()]