#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Mail Library
#
# version 0.2.2
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
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import json
import re
import curses
import datetime
from conyxDBQuery import conyxDBQuery
from conyxDBAuth import conyxDBStoreAuth
from conyxDBUpdNickname import conyxDBUpdNickname
from conyxDBGenDML import conyxDBGenDML
from conyxDBGenDMLVars import conyxDBGenDMLVars
from conyxDBGenDMLVarsMany import conyxDBGenDMLVarsMany

# import urllib.parse # v0.1.9b
try:
  from urllib.parse import urlencode
except ImportError:
  from urllib import urlencode

# import urllib.request # v0.1.9b
try:
  from urllib.request import urlopen
except ImportError:
  from urllib import urlopen

url='https://www.nyx.cz/api.php'

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

#def nyx_auth(p_nickname):
#  ret=-1
#  cols , rows = conyxDBQuery('select auth_key from auth')
#  # https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3
#  params = urlencode({
#    'auth_nick':get_auth_nickname(),
#    'auth_token':get_auth_token(),
#    'l':'help',
#    'l2':'conyx'
#  }).encode("utf-8") # v0.1.9
#  try:
#    # https://stackoverflow.com/questions/3969726/attributeerror-module-object-has-no-attribute-urlopen
#    # https://stackoverflow.com/questions/30760728/python-3-urllib-produces-typeerror-post-data-should-be-bytes-or-an-iterable-of?noredirect=1
#    resp = urlopen(url, params).read()
#  except Exception:
#    # traceback.print_exc(file=sys.stdout) # v0.1.9
#    print("Chyba pri pripojeni na server")
#    exit()
#  try:
#    res=json.loads(resp.decode('utf-8'))
#  except Exception:
#    # https://www.reddit.com/r/learnpython/comments/9bbyny/typeerror_the_json_object_must_be_str_not_bytes/
#    traceback.print_exc(file=sys.stdout) # v0.1.9
#    print(res) # v0.1.9
#    print("Chyba pri zpracovani odpovedi serveru")
#    exit()
#    #print(res)
#  # print(res) # v0.1.9
#  # https://stackoverflow.com/questions/33727149/dict-object-has-no-attribute-has-key
#  if "system" not in res:
#    if res["code"]=="401" and res["error"]!='Not Authorized':
#      print("Nejdrive zruste stavajici registraci")
#    elif res["code"]=="401" and res["auth_state"]=='AUTH_EXISTING':
#      print('Nejprve zruste stavajici registraci')
#    elif res["code"]=="401" and res["auth_state"]=='AUTH_INVALID_USERNAME':
#      print('Nespravny uzivatel')
#      conyxDBUpdNickname('')
#    else:
#      print("AUTH CODE: " + res["auth_code"])
#      #print ("Storing Auth Code to DB")
#      conyxDBStoreAuth(res["auth_token"])
#      #print("AUTH TOKEN: " + res["auth_token"])
#  else:
#    print("Pripojen na server ...")
#    ret=0
#  return(ret)


def nyx_filter_mail(p_user,p_text):
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'mail',
    'l2' : 'messages',
    'filter_user': p_user,
    'filter_text': p_text
  }).encode('utf-8')
  resp = urlopen(url, params).read()
  res=json.loads(resp.decode('utf-8'))
  #print(res) # DEBUG THE RESPONSE
  rx=0
  conyxDBGenDML('delete from mail')
  vars=[]
  qry="insert into mail values (?,?,?,?,?)"
  for i in res['data']:
    vars.append((i['id_mail'],i['content'],i['direction'],i['other_nick'],i['time']))
    rx+=1
  conyxDBGenDMLVarsMany(qry,vars)
  return(rx)

def nyx_list_mail():
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'mail',
    'l2' : 'messages'
  }).encode("utf-8") # v0.1.9
  resp = urlopen(url, params).read()
  res=json.loads(resp.decode('utf-8'))
  #print(res) # DEBUG THE RESPONSE
  conyxDBGenDML('delete from mail')
  rx=0
  vars=[]
  qry="insert into mail values (?,?,?,?,?)"
  for i in (res['data']):
    #vars.append((rx,(i['id_mail'],i['content'],i['direction'],i['other_nick'],i['time'])))
    vars.append((i['id_mail'],i['content'],i['direction'],i['other_nick'],i['time']))
  conyxDBGenDMLVarsMany(qry,vars)
  return(rx)

def nyx_send_mail(p_recipient, p_message):
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'mail',
    'l2' : 'send',
    'recipient' : p_recipient,
    'message' : p_message
  }).encode("utf-8") # v0.1.9
  #resp = urllib.urlopen(url, params).read()
  resp = urlopen(url, params).read()
  res=json.loads(resp.decode('utf-8'))
  if (res["result"]=="ok"):
    #print(" ... dopis zaslan")
    return(0)
  else:
    return(-1)

# DEBUG    
#if (nyx_auth(get_auth_nickname())==0):
#  nyx_last_conv()
#  nyx_list_mail()
#  nyx_filter_mail('HANT','')
