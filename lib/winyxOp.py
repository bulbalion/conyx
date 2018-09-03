#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client - Windows Version
#
# Conyx Database Library
#
# version 0.1.0
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
    print("Jsem pripojen...")
    ret=0
  return(ret)

def nyx_list_disc(p_filter,colo):
  buf=[]
  line=""
  params = urllib.urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'bookmarks',
    'l2' : 'all'
  })
  resp = urllib.urlopen(url, params).read()
  res=json.loads(resp)
  #print(res)
  for i in (res['data']['discussions']):
    if p_filter == "":
      line=Fore.BLUE  + i['id_klub'] + Style.DIM + Fore.RED + '|' + Style.NORMAL + Fore.CYAN + i['jmeno'] + Style.DIM + Fore.RED + '|' + Style.DIM + Fore.CYAN + i['unread'] + Style.DIM + Fore.RED + '|' + Style.NORMAL + Fore.CYAN + i['replies'] + Style.DIM + Fore.RED + '|'+ Style.RESET_ALL
      buf.append(line)
    elif p_filter == "nove":
      if int(i['unread']) > 0:
        if colo==1:
          line=Fore.BLUE  + i['id_klub'] + Style.DIM + Fore.RED + '|' + Style.NORMAL + Fore.CYAN + i['jmeno'] + Style.DIM + Fore.RED + '|' + Style.DIM + Fore.CYAN + i['unread'] + Style.DIM + Fore.RED + '|' + Style.NORMAL + Fore.CYAN + i['replies'] + Style.DIM + Fore.RED + '|'+ Style.RESET_ALL
        else:
          line=i['id_klub']+'|'+i['jmeno']+'|'+i['unread']+'|'+i['replies'] 
        buf.append(line)
    else:
      if i['jmeno'].find(p_filter) != -1:
        line=Fore.BLUE  + i['id_klub'] + Style.DIM + Fore.RED + '|' + Style.NORMAL + Fore.CYAN + i['jmeno'] + Style.DIM + Fore.RED + '|' + Style.DIM + Fore.CYAN + i['unread'] + Style.DIM + Fore.RED + '|' + Style.NORMAL + Fore.CYAN + i['replies'] + Style.DIM + Fore.RED + '|'+ Style.RESET_ALL
        buf.append(line)
  return(buf)

def nyx_show_disc_msgs(p_disc_key,colo):
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
  resp = urllib.urlopen(url, params).read()
  res=json.loads(resp)
  #print(res)
  for x in range(len(res["data"])-1,-1,-1):
    cr = res["data"][x]
    if colo==1:
      line=cr["id_wu"] + Style.DIM + Fore.RED + "|" + Style.NORMAL + Fore.BLUE + cr["nick"] + Style.DIM + Fore.RED + '|' + Style.NORMAL + Fore.CYAN + cleanhtml(cr["content"]) + Style.DIM + Fore.RED + '|' + Fore.CYAN + cr["wu_rating"]
      buf.append(line)
    else:
      line=cr["id_wu"]+"|"+cr["nick"]+'|'+cleanhtml(cr["content"])+'|'+cr["wu_rating"]
      buf.append(line)
  return(buf)

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
  res=json.loads(resp)
  if (res["result"]=="ok"):
    print("prispevek zaslan")

# DEBUG    
#if (nyx_auth()==0):
#  # nyx_list_disc()
#  # THERE COULD BE A LOOP HERE
#  # AND THE PRINT FUNCTION SHOULD BE CUSTOMIZED
#  # nyx_send_message("3","BOTH MACHINE OR HUMAN ERROR. SORRY.")
#  nyx_show_disc_msgs('23330')
