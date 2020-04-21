#-*- coding: utf-8 -*-
#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Operations Library
#
# version 0.1.9e
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
from nyxOp import *
from conyxDBLast import conyxDBLast
from nyxMail import * 
from conyxDBQuery import conyxDBQuery
from conyxDBGenDML import conyxDBGenDML
from conyxDBGenDMLVars import conyxDBGenDMLVars
from conyxDBUpdNickname import conyxDBUpdNickname
#from tuiFile import *
from tuiBuffer import *
import readline

def cacheVypisPrispevky():
  cols,rows=conyxDBQuery("select id_prispevek, prisp_from ||'|'||prisp_text||'|'||prisp_hodnoceni from prispevek_cache")
  return(cols,rows)

def getKlubNameFromID(id_klub):
  cols,rows=conyxDBQuery("select jmeno from klub_cache where id_klub = '" + str(id_klub)+"'")
  return(rows[0][0])

def ctiKlub(klub_id):
  print("Nacitam klub do databaze " + str(klub_id))
  try:
    buf=nyx_show_disc_msgs(str(klub_id))
    conyxDBGenDML('update klub_cache set unread = "0" where id_klub="'+str(klub_id)+'"')
    #cacheVypisPrispevky()
  except Exception:
    traceback.print_exc(file=sys.stdout)
    print("Nepodarilo se ulozit prispevky z aktualni diskuze do databaze")

def cleanHtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', text)
  cleantext=cleantext.replace('\n','')
  cleantext=cleantext.replace('\r','')
  return cleantext

def conyxOpsTuiBuffer(name,buffer):
  locale.setlocale(locale.LC_ALL, '')
  tuiScrollContent(name,buffer)

def zobrazDiskuzi(klub_id,screen,onTerm=0,id_wu=None,dir="older",filter_user=None,filter_keyword=None):
  #print("Nacitam klub do databaze " + str(i_klub_id))
  try:
    if filter_user:
      buf=nyx_show_disc_msgs_filter(str(klub_id),filter_user)
    elif filter_keyword:
      buf=nyx_show_disc_msgs_filter(str(klub_id),None,filter_keyword)
    elif id_wu:
      buf=nyx_show_disc_msgs_from(str(klub_id),id_wu,dir)
    else:
      buf=nyx_show_disc_msgs(str(klub_id))
    #print("posledni prispevek: " + str(int(res[1][0][0])))
    conyxDBGenDML('update klub_cache set unread = "0" where id_klub="'+str(klub_id)+'"')
  except Exception:
    traceback.print_exc(file=sys.stdout)
    print("Nepodarilo se ulozit prispevky z aktualni diskuze do databaze")
  #
  #buf=nyx_show_disc_msgs(str(klub_id))
  cols, rows = conyxDBQuery('select prisp_from || "|" || prisp_text || "|" ||  prisp_hodnoceni wu_rating from prispevek_cache')
  buffer=[]
  for i in rows:
    buffer.append(i[0])
  if rows:
    if onTerm==0:
      print(rows)
      print(len(rows))
    if len(rows[0])>0:
      #klub_name=getKlubNameFromID(klub_id)[:width-10]
      klub_name=""
      try:
        klub_name=getKlubNameFromID(klub_id)[:-10]
      except Exception:
        1==1
      conyxOpsTuiBuffer(klub_name,buffer)
  else:
    screen.clear()
    screen.refresh()
    screen.addstr(1,3,"Nic nenalezeno...")
    screen.getch()
  screen.clear()
  screen.refresh()
 

#print(getKlubNameFromID(3))
