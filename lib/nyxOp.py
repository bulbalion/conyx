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
# version 0.2.3
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
# 0.2.4 - notifications
#

import sys, os, traceback
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import json
import re
import datetime
from conyxDBQuery import conyxDBQuery
from conyxDBAuth import conyxDBStoreAuth
from conyxDBUpdNickname import conyxDBUpdNickname
from conyxDBGenDML import conyxDBGenDML
from conyxDBGenDMLVars import conyxDBGenDMLVars
from conyxDBGenDMLVarsMany import conyxDBGenDMLVarsMany
from conyxDBLocation import conyxDBLocation
from tuiBuffer import cleanHtml, print_more, colors, nocolors
from conyxUtils import uts2str
from getConfig import getConfig
from get_auth_nickname import get_auth_nickname
from get_auth_token import get_auth_token

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

#try:
#  from urllib import request as req
#except ImportError:
#  print("Cannot attach files")

import urllib

url='https://www.nyx.cz/api.php'

def get_club_name(id_klub):
  try:
    cols,rows = conyxDBQuery("select jmeno from klub_cache where id_klub = '%s'" % id_klub)
    return(str(rows[0][0]))
  except Exception as e:
    return(id_klub)

#def get_auth_token():
#  cols , rows = conyxDBQuery('select auth_key from auth')
#  return(str(rows[0][0]))

#def get_auth_nickname():
#  cols , rows = conyxDBQuery('select nickname from nick')
#  return(str(rows[0][0]))
#
def cleanhtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def nyx_auth(p_nickname):
  ret=-1
  cols , rows = conyxDBQuery('select auth_key from auth')
  params = urlencode({
    'auth_nick':get_auth_nickname(),
    'auth_token':get_auth_token(),
    'l':'help',
    'l2':'test'
  }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
  except Exception:
    print("Chyba pri pripojeni na server")
    exit()
  #print(resp)
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  if 'system' not in res:
    if res["code"]=="401" and res["error"]!='Not Authorized':
      print("Nejdrive zruste stavajici registraci")
    elif res["code"]=="401" and res["auth_state"]=='AUTH_EXISTING':
      print('Nejprve zruste stavajici registraci')
    elif res["code"]=="401" and res["auth_state"]=='AUTH_INVALID_USERNAME':
      print('Nespravny uzivatel')
      conyxDBUpdNickname('')
    else:
      print("KOD PRO AUTENTIFIKACI: " + res["auth_code"])
      #print ("Storing Auth Code to DB")
      conyxDBStoreAuth(res["auth_token"])
      #print("AUTH TOKEN: " + res["auth_token"])
    input("Autentifikuj se, stiskni ENTER a spust program znovu...")
  else:
    print("Pripojen na server ...")
    ret=0
  return(ret)

def nyx_list_book_reply(p_filter,colo):
  buf=[]
  line=""
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'bookmarks',
    'l2' : 'new'
  }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
  except Exception:
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp.decode('utf-8'))
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

def get_disc_max_klub_id():
  cols , rows = conyxDBQuery('select max(id) mid from klub_cache')
  if (len(rows)>0):
    return(int(rows[0][0]))
  else:
    return(0)

def nyx_disc_header_desc(id_klub):
  buf=[]
  line=""
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'discussion',
    'l2' : 'home',
    'id_klub' : id_klub
  }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
    try:
      res=json.loads(resp.decode('utf-8'))
    except Exception:
      print("Chyba pri zpracovani odpovedi serveru")
      exit()
    #print(res) # DEBUG THE RESPONSE
    ret=res['header']
    ##conyxDBGenDML('delete from klub_cache')
    #ret=""
    #if ('discussion' in res.keys()):
    #  if ('name_main' in res['discussion'].keys()):
    #    ret=res['discussion']['name_main']
    #    try:      
    #      mid=get_disc_max_klub_id()
    #      #print(mid)
    #      cols,rows=conyxDBQuery("select 1 from klub_cache where id_klub = " + str(id_klub))
    #      if (not rows):
    #        conyxDBGenDMLVars("insert into klub_cache values (?,?,?,?,?)",(mid+1,id_klub,res['discussion']['name_main'],0,0,))
    #    except Exception:
    #      traceback.print_exc(file=sys.stdout)  
    #      print("Nemuzu vlozit zahlavi klubu do databaze.")
    #      sleep
    #  err=1
    return(ret) 
  except Exception:
    traceback.print_exc(file=sys.stdout)  
    print("Nemuzu stahnout jmeno klubu ze serveru.")
 
def nyx_disc_header(id_klub):
  buf=[]
  line=""
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'discussion',
    'l2' : 'home',
    'id_klub' : id_klub
  }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
    try:
      res=json.loads(resp.decode('utf-8'))
    except Exception:
      print("Chyba pri zpracovani odpovedi serveru")
      exit()
    #print(res['discussion']['name_main']) # DEBUG THE RESPONSE
    #conyxDBGenDML('delete from klub_cache')
    ret=""
    if ('discussion' in res.keys()):
      if ('name_main' in res['discussion'].keys()):
        ret=res['discussion']['name_main']
        try:      
          mid=get_disc_max_klub_id()
          #print(mid)
          cols,rows=conyxDBQuery("select 1 from klub_cache where id_klub = " + str(id_klub))
          if (not rows):
            conyxDBGenDMLVars("insert into klub_cache values (?,?,?,?,?)",(mid+1,id_klub,res['discussion']['name_main'],0,0,))
        except Exception:
          traceback.print_exc(file=sys.stdout)  
          print("Nemuzu vlozit zahlavi klubu do databaze.")
          sleep
      err=1
    return(ret) 
  except Exception:
    traceback.print_exc(file=sys.stdout)  
    print("Nemuzu stahnout jmeno klubu ze serveru.")
    return(ret)

def nyx_search_writeups(filter_user=None,filter_text=None,position=None):
  buf=[]
  line=""
  params=None
  if filter_text:
    params = urlencode({
      'auth_nick': get_auth_nickname(),
      'auth_token': get_auth_token(),
      'l' : 'search',
      'l2' : 'writeups',
      'filter_text' : filter_text
    }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  #print(res)
  #for i in res["data"]:
  #  cr = i["klub_jmeno"]+"|"+i["nick"]+"|"+cleanhtml(i["content"])
  #  print(cr)
  #if not 'data' in res: 
  #  print("Bud nemas pristup nebo se neco pokazilo.")
  #  return (buf)
  rx=0
  err=0
  #conyxDBGenDML('delete from prispevek_cache')
  #for i in range(len(res["data"])-1,-1,-1):
  #  if err==0:
  #    cr = res["data"][i]
  #    try:
  #      conyxDBGenDMLVars("insert into prispevek_cache values (?,?,?,?,?)",(rx,cr['id_wu'],cr['nick'],cr['content'],cr['wu_rating'],))
  #    except Exception:
  #      err=1
  return(rx,res)
  #return(rx,buf)

def nyx_show_disc_msgs_filter(p_disc_key,filter_user,filter_keyword):
  buf=[]
  line=""
  params=None
  if filter_user:
    params = urlencode({
      'auth_nick': get_auth_nickname(),
      'auth_token': get_auth_token(),
      'l' : 'discussion',
      'l2' : 'messages',
      'id' : p_disc_key,
      'filter_user' : filter_user
    }).encode('utf-8')
  elif filter_keyword:
    params = urlencode({
      'auth_nick': get_auth_nickname(),
      'auth_token': get_auth_token(),
      'l' : 'discussion',
      'l2' : 'messages',
      'id' : p_disc_key,
      'filter_text' : filter_keyword
    }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  for i in range(len(res["data"])-1,-1,-1):
    cr = res["data"][i]
    #print(cr['id_wu']+' '+cr['content'])
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


def nyx_show_disc_msgs_from(p_disc_key,id_wu,dir="older"):
  buf=[]
  line=""
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'discussion',
    'l2' : 'messages',
    'id' : p_disc_key,
    'direction' : dir,
    'id_wu' : str(id_wu),
    'n' : '00'
  }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  for i in range(len(res["data"])-1,-1,-1):
    cr = res["data"][i]
    #print(cr['id_wu']+' '+cr['content'])
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

def nyx_list_disc(p_filter,colo):
  buf=[]
  line=""
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'bookmarks',
    'l2' : 'all'
  }).encode('utf-8')
  rx=0
  try:
    resp = urlopen(url, params).read()
    try:
      res=json.loads(resp.decode('utf-8'))
    except Exception:
      print("Chyba pri zpracovani odpovedi serveru")
      exit()
    # print(res) # DEBUG THE RESPONSE
    conyxDBGenDML('delete from klub_cache')
    err=0
    vars=[]
    qry="insert into klub_cache values (?,?,?,?,?)"
    for i in (res['data']['discussions']):
      if err==0:
        try:      
          vars.append((rx,i['id_klub'],i['jmeno'],i['unread'],i['replies'],))
        except Exception:
          err=1
      rx+=1
    conyxDBGenDMLVarsMany(qry,vars)
  except Exception:
    traceback.print_exc(file=sys.stdout)  
    print("Nemuzu stahnout seznam klubu ze serveru.")
    exit()
  return(rx,buf)

def nyx_bookmarks_history():
  buf=[]
  id_wus=[]
  line=""
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'bookmarks',
    'l2' : 'history'
  }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  cols=[]
  rows=[]
  for khist in res["data"]["discussions"]:
    cols=("id_klub","txt")
    rows.append((khist["id_klub"],khist["id_klub"]+'|'+khist["jmeno"]))
  return(cols,rows)
  if not 'data' in res: 
    print("Bud nemas pristup nebo se neco pokazilo.")
    return (buf)
  rx=0
  err=0
  conyxDBGenDML('delete from prispevek_cache')
  vars=[]
  qry="insert into prispevek_cache values (?,?,?,?,?)"
  for i in range(len(res["data"])-1,-1,-1):
    if err==0:
      cr = res["data"][i]
      try:
        vars.append((rx,cr['id_wu'],cr['nick'],cr['content'],cr['wu_rating'],))
        #conyxDBGenDMLVars("insert into prispevek_cache values (?,?,?,?,?)",(rx,cr['id_wu'],cr['nick'],cr['content'],cr['wu_rating'],))
      except Exception:
        err=1
        print("Chyba pri zpracovani odpovedi serveru")
        exit()
  conyxDBGenDMLVarsMany(qry,vars)
  return(rx,buf)

def nyx_show_disc_msgs(p_disc_key,discFrom=None):
  buf=[]
  id_wus=[]
  line=""
  if discFrom: 
    params = urlencode({
      'auth_nick': get_auth_nickname(),
      'auth_token': get_auth_token(),
      'l' : 'discussion',
      'l2' : 'messages',
      'id' : p_disc_key,
      'direction' : 0,
      'id_wu' : discFrom
    }).encode('utf-8')
  else:
    params = urlencode({
      'auth_nick': get_auth_nickname(),
      'auth_token': get_auth_token(),
      'l' : 'discussion',
      'l2' : 'messages',
      'id' : p_disc_key,
      'direction' : 0
    }).encode('utf-8')
  try:
    resp = urlopen(url, params).read()
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri pripojeni na server")
    exit()
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    traceback.print_exc(file=sys.stdout) # v0.1.9
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  #print(res)
  if not 'data' in res: 
    print("Bud nemas pristup nebo se neco pokazilo.")
    return (buf)
  rx=0
  err=0
  conyxDBGenDML('delete from prispevek_cache')
  vars=[]
  qry="insert into prispevek_cache values (?,?,?,?,?)"
  for i in range(len(res["data"])-1,-1,-1):
    if err==0:
      cr = res["data"][i]
      try:
        vars.append((rx,cr['id_wu'],cr['nick'],cr['content'],cr['wu_rating'],))
      except Exception:
        err=1
        traceback.print_exc(file=sys.stdout)  
        exit()
  conyxDBGenDMLVarsMany(qry,vars)
  return(rx,buf)

#def nyx_send_message(p_disc_key, p_message,p_attachment=None):
#  from mpart import mpart
#  from mpart import boundary
#  body=mpart(get_auth_nickname(), get_auth_token(), p_disc_key, p_message,p_attachment)
#  req=urllib.request.Request(url)
#  req.add_header('content-type' , 'multipart/form-data; boundary="' + boundary + '"')
#  req.add_header('content-length' , str(len(body)))
#  req.data=body
#  #print(req.data)
#  resp=urllib.request.urlopen(req).read()
#  try:
#    res=json.loads(resp.decode('utf-8'))
#  except Exception:
#    print("Chyba pri zpracovani odpovedi serveru")
#    return(-1)
#  if (res["result"]=="ok"):
#    print("prispevek zaslan")
#    return(0)

def nyx_reply_message(p_disc_key,p_message,p_msg_id,p_usr_id):
  p_message='{reply '+p_usr_id+'|'+p_msg_id+'}:'+p_message
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'discussion',
    'l2' : 'send',
    'id' : p_disc_key,
    'message' : p_message
  }).encode('utf-8')
  resp = urlopen(url, params).read()
  try:
    res=json.loads(resp.decode('utf-8'))
  except Exception:
    print("Chyba pri zpracovani odpovedi serveru")
    exit()
  if (res["result"]=="ok"):
    print("prispevek zaslan")

def nyx_feed_notices():
  clrz=getConfig("barvicky")
  c = nocolors
  if (clrz[0][0]=="A"): c = colors 
  buf=[]
  line=""
  params = urlencode({
    'auth_nick': get_auth_nickname(),
    'auth_token': get_auth_token(),
    'l' : 'feed',
    'l2' : 'notices',
    'keep_new' : '1'
  }).encode('utf-8')
  rx=0
  try:
    resp = urlopen(url, params).read()
    try:
      res=json.loads(resp.decode('utf-8'))
    except Exception:
      traceback.print_exc(file=sys.stdout)  
      print("Chyba pri zpracovani odpovedi serveru")
      exit()
    lvis_str=uts2str(res['data']['notice_last_visit'])
    print_str=c[2]+'==---..\ '+c[14]+'Posledni zobrazeni '+c[10]+lvis_str+c[2]+' /..---=='
    printed_lines=0
    current_page=1
    printed_lines,current_page=print_more(print_str,printed_lines,current_page)
    for i in res['data']['items']:
      if (i):
        print_str=c[2]+i['section']+'|'+i['id_wu']+'|'+get_club_name(i['id_klub'])+'|'+i['nick']+'|'+uts2str(i['time'])+'|'+i['wu_rating']+'|'+cleanHtml(i['content'])
        printed_lines,current_page=print_more(print_str,printed_lines,current_page)
      if ('thumbs_up' in i):
        for j in (i['thumbs_up']):
          if (j):
            print_str=c[14]+' +1: '+'|'+j['nick']+'|'+uts2str(j['time'])
            printed_lines,current_page=print_more(print_str,printed_lines,current_page)
      if ('replies' in i):
        for k in (i['replies']):
          if (k):
            print_str=c[10]+' |-> '+'|'+k['nick']+'|'+uts2str(k['time'])+'|'+k['id_wu']+'|'+get_club_name(k['id_klub'])+'|'+cleanHtml(k['text'])
            printed_lines,current_page=print_more(print_str,printed_lines,current_page)
    print(c['r'])
    # print(res) # DEBUG THE RESPONSE
    #conyxDBGenDML('delete from klub_cache')
    #err=0
    #vars=[]
    #qry="insert into klub_cache values (?,?,?,?,?)"
    #for i in (res['data']['discussions']):
    #  if err==0:
    #    try:      
    #      vars.append((rx,i['id_klub'],i['jmeno'],i['unread'],i['replies'],))
    #      #conyxDBGenDMLVars("insert into klub_cache values (?,?,?,?,?)",(rx,i['id_klub'],i['jmeno'],i['unread'],i['replies'],))
    #    except Exception:
    #      err=1
    #  rx+=1
    #conyxDBGenDMLVarsMany(qry,vars)
  except Exception:
    traceback.print_exc(file=sys.stdout)  
    print("Nemuzu stahnout notifikace.")
    exit()
  return(rx,buf)


# DEBUG    
#if (nyx_auth()==0):
# # nyx_list_disc()
# # THERE COULD BE A LOOP HERE
# # AND THE PRINT FUNCTION SHOULD BE CUSTOMIZED
# # nyx_send_message("3","BOTH MACHINE OR HUMAN ERROR. SORRY.")
# nyx_show_disc_msgs('23330')
# nyx_disc_header(1)
