from get_auth_nickname import get_auth_nickname
from get_auth_token import get_auth_token

import urllib
import json

url='https://www.nyx.cz/api.php'

def nyx_send_message(p_disc_key, p_message,p_attachment=None):
  from mpart import mpart
  from mpart import boundary
  body=mpart(get_auth_nickname(), get_auth_token(), p_disc_key, p_message,p_attachment)
  req=urllib.request.Request(url)
  req.add_header('content-type' , 'multipart/form-data; boundary="' + boundary + '"')
  req.add_header('content-length' , str(len(body)))
  req.data=body
  #print(req.data)
  resp=urllib.request.urlopen(req).read()
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri zpracovani odpovedi serveru")
    return(-1)
  if (res["result"]=="ok"):
    print("prispevek zaslan")
    return(0)

