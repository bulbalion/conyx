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
# version 0.1.5
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

#-*- coding: utf-8 -*-

import sys, os, traceback
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from nyxOp import *
import cmd2 as cmd2
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

def zobrazDiskuzi(klub_id,screen):
  buf=nyx_show_disc_msgs(str(klub_id))
  cols, rows = conyxDBQuery('select prisp_from || "|" || prisp_text || "|" ||  prisp_hodnoceni wu_rating from prispevek_cache')
  buffer=[]
  for i in rows:
    buffer.append(i[0])
  if len(rows)>0:
    #klub_name=getKlubNameFromID(klub_id)[:width-10]
    klub_name=getKlubNameFromID(klub_id)[:-10]
    conyxOpsTuiBuffer(klub_name,buffer)
  screen.clear()
  screen.refresh()
 

#print(getKlubNameFromID(3))
