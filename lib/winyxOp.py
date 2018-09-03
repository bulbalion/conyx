#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Database Library
#
# version 0.1.6
#
# You can do whatever You want with Conyx.
# But I don't take reponsbility nor even
# implied responsibility for the harm,
# damage, loss or anything negative
# You cause using Conyx.
#
# There is no service provided. The program
# is AS-IS and there is ABSOLUTELY no warranty
# provided.
#

import sys, os, traceback
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import urllib
import json
import re
import datetime
from colorama import Fore, Style
from conyxDBQuery import conyxDBQuery
from conyxDBAuth import conyxDBStoreAuth
from conyxDBUpdNickname import conyxDBUpdNickname
from conyxDBGenDML import conyxDBGenDML
from conyxDBGenDMLVars import conyxDBGenDMLVars

url='http://www.nyx.cz/api.php'

def get_auth_token():
  cols , rows = conyxDBQuery('select auth_key from auth')
  return(str(rows[0][0]))

def get_auth_nickname():
  cols , rows = conyxDBQuery('select nickname from nick')
  return(str(rows[0][0]))

def cleanhtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def nyx_auth(p_nickname):
  ret=-1
  cols , rows = conyxDBQuery('select auth_key from auth')
  params = urllib.urlencode({
    'auth_nick':get_auth_nickname(),
    'auth_token':get_auth_token(),
    'l':'help',
    'l2':'test'
  })
  try:
    resp = urllib.urlopen(url, params).read()
  except Exception:
    print("Chyba pri pripojeni na server")
    exit()
  #print(resp)
  try:
    res=json.loads(resp)
  except Exception:
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  if not res.has_key("system"):
    if res["code"]=="401" and res["error"]!='Not Authorized':
      print("Nejdrive zruste stavajici registraci")
    elif res["code"]=="401" and res["auth_state"]=='AUTH_EXISTING':
      print('Nejprve zruste stavajici registraci')
    elif res["code"]=="401" and res["auth_state"]=='AUTH_INVALID_USERNAME':
      print('Nespravny uzivatel')
      conyxDBUpdNickname('')
    else:
      print("AUTH CODE: " + res["auth_code"])
      #print ("Storing Auth Code to DB")
      conyxDBStoreAuth(res["auth_token"])
      #print("AUTH TOKEN: " + res["auth_token"])
  else:
    print("Pripojen na server ...")
    ret=0
  return(ret)

def nyx_list_book_reply(p_filter,colo):
  buf=[]
  line=""
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'bookmarks',
    'l2' : 'new'
  })
  try:
    resp = urllib.urlopen(url, params).read()
  except Exception:
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp)
  except Exception:
    print("Chyba pri zpracovani odpovedi server")
    exit()
  #print(res) # DEBUG THE RESPONSE
  conyxDBGenDML('delete from klub_cache')
  rx=0
  for i in (res['data']['discussions']):
    conyxDBGenDMLVars("insert into klub_cache values (?,?,?,?,?)",(rx,i['id_klub'],i['jmeno'],i['unread'],i['replies'],))
    rx+=1
  return(buf)

def nyx_list_disc(p_filter,colo):
  buf=[]
  line=""
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'bookmarks',
    'l2' : 'all'
  })
  try:
    resp = urllib.urlopen(url, params).read()
    try:
      res=json.loads(resp)
    except Exception:
      print("Chyba pri zpracovani odpovedi serveru")
      exit()
    # print(res) # DEBUG THE RESPONSE
    conyxDBGenDML('delete from klub_cache')
    rx=0
    err=0
    for i in (res['data']['discussions']):
      if err==0:
        try:      
          conyxDBGenDMLVars("insert into klub_cache values (?,?,?,?,?)",(rx,i['id_klub'],i['jmeno'],i['unread'],i['replies'],))
        except Exception:
          print("Nemuzu vlozit zahlavi klubu do databaze.")
          err=1
      rx+=1
  except Exception:
    traceback.print_exc(file=sys.stdout)  
    print("Nemuzu stahnout seznam klubu ze serveru.")
  return(rx,buf)

def nyx_show_disc_msgs(p_disc_key):
  buf=[]
  line=""
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'discussion',
    'l2' : 'messages',
    'id' : p_disc_key,
    'direction' : 0
  })
  try:
    resp = urllib.urlopen(url, params).read()
  except Exception:
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp)
  except Exception:
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  # print(res)
  if not 'data' in res: 
    print("Bud nemas pristup nebo se neco pokazilo.")
    return (buf)
  rx=0
  err=0
  conyxDBGenDML('delete from prispevek_cache')
  for i in range(len(res["data"])-1,-1,-1):
    if err==0:
      cr = res["data"][i]
      try:
        conyxDBGenDMLVars("insert into prispevek_cache values (?,?,?,?,?)",(rx,cr['id_wu'],cr['nick'],cr['content'],cr['wu_rating'],))
      except Exception:
        err=1
  return(rx,buf)

def nyx_send_message(p_disc_key, p_message):
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'discussion',
    'l2' : 'send',
    'id' : p_disc_key,
    'message' : p_message
  })
  resp = urllib.urlopen(url, params).read()
  res=json.loads(resp)
  if (res["result"]=="ok"):
    print(" ... prispevek zaslan")

def nyx_reply_message(p_disc_key,p_message,p_msg_id,p_usr_id):
  p_message='{reply '+p_usr_id+'|'+p_msg_id+'}:'+p_message
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'discussion',
    'l2' : 'send',
    'id' : p_disc_key,
    'message' : p_message
  })
  resp = urllib.urlopen(url, params).read()
  try:
    res=json.loads(resp)
  except Exception:
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  if (res["result"]=="ok"):
    print("prispevek zaslan")

# DEBUG    
#if (nyx_auth()==0):
#  # nyx_list_disc()
#  # THERE COULD BE A LOOP HERE
#  # AND THE PRINT FUNCTION SHOULD BE CUSTOMIZED
#  # nyx_send_message("3","BOTH MACHINE OR HUMAN ERROR. SORRY.")
#  nyx_show_disc_msgs('23330')
