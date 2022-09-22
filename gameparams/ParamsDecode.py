"""
ParamsDecode.py module.
Run to create gameparams.json from gameparams.data file.
"""

import pickle
import json
import zlib

class GPEncode(json.JSONEncoder):
    def default(self, o):
        res = getattr(o, '__dict__', {})
        tp_k = self._find_tuple_keys(res)
        if tp_k:
            for i in tp_k:
                k1, k2 = i[0], i[1]
                res[k1][str(k2)] = res[k1][k2] #copy?
                del res[k1][k2]
        return res
        #return getattr(o, '__dict__', {})

    def _find_tuple_keys(self, obj):
        """ネストされた辞書のうち、キーがタプルであるものを探す。それぞれのキーセットを返す"""
        return [
                    (k, s)
                    for k in obj if isinstance(obj[k], dict)
                    for s in obj[k].keys() if isinstance(s, tuple)
                ]
        
def EncodeStrings(s_scr):
    s_str = zlib.decompress(s_scr[::-1]).decode()
    return s_str.replace('\\x', '%').replace('\r', '').encode()

try:
    with open('../res/GameParams.data', 'rb') as f:
        s = f.read()

    s_bin = EncodeStrings(s)
    s_pkl = pickle.loads(s_bin)

    s_jsn = json.dumps(s_pkl, cls=GPEncode, sort_keys=True, indent=4, separators=(',', ': '))

    with open('../res/gameparams.json', 'w', newline="\n") as f:
        f.write(s_jsn)
        

except Exception as e:
    with open('error.txt', 'w') as f:
        f.write("%s" % e)
