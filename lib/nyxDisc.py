#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Discussions Library
#
# version 0.1.4
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
import curses
import datetime
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
    'l2':'conyx'
  })
  resp = urllib.urlopen(url, params).read()
  res=json.loads(resp)
  #print(res)
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

def nyx_filter_discussion(p_user,p_text):
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'mail',
    'l2' : 'messages',
    'filter_user': p_user,
    'filter_text': p_text
  })
  resp = urllib.urlopen(url, params).read()
  res=json.loads(resp)
  #print(res) # DEBUG THE RESPONSE
  rx=0
  #conyxDBGenDML('delete from mail_last_seen')
  for i in res['data']:
    if (i['direction']=='to'):
      conyxDBGenDMLVars("insert into filter_mail values (?,?,?,?,?,?)",(i['message_status'],i['content'],i['direction'],i['other_nick'],i['id_mail'],i['time']))
    rx+=1
  return(rx)

def nyx_list_mail():
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'mail',
    'l2' : 'messages'
  })
  resp = urllib.urlopen(url, params).read()
  res=json.loads(resp)
  #print(res) # DEBUG THE RESPONSE
  conyxDBGenDML('delete from mail')
  rx=0
  for i in (res['data']):
    if (i['direction']=='from'):
      conyxDBGenDMLVars("insert into mail values (?,?,?,?,?)",(i['id_mail'],i['content'],i['direction'],i['other_nick'],i['time']))
    if (i['direction']=='to'):
      conyxDBGenDMLVars("insert into mail values (?,?,?,?,?)",(i['id_mail'],i['content'],i['direction'],i['other_nick'],i['time']))
    rx+=1
  return(rx)

def nyx_send_mail(p_recipient, p_message):
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'mail',
    'l2' : 'send',
    'recipient' : p_recipient,
    'message' : p_message
  })
  resp = urllib.urlopen(url, params).read()
  res=json.loads(resp)
  if (res["result"]=="ok"):
    print(" ... prispevek zaslan")

# DEBUG    
if (nyx_auth(get_auth_nickname())==0):
  #nyx_list_mail()
  nyx_filter_mail('HANT','')
