#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Command Line
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
#from tuiMainScreen import *
import readline

i_klub_id=1
i_klub_name=""

def cleanHtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def zvol_klub(inp):
  i_klub_id = inp 

def aktualni_klub():
  return (i_klub_id)

def cacheVypisPrispevky():
  cols,rows=conyxDBQuery('select id_prispevek, prisp_from, prisp_text, prisp_hodnoceni wu_rating from prispevek_cache')
  if len(rows) > 0:
    for r in (rows):
      print(str(r[0])+"|"+str(r[1])+"|"+cleanHtml(r[2])+"|"+str(r[3]));

def rlinput(prompt, prefill=''):
  readline.set_startup_hook(lambda: readline.insert_text(prefill))
  try:
    return raw_input(prompt)
  finally:
    readline.set_startup_hook()

def odhadniKomuJePrispevekUrcen(id_prisp):
  cols,rows=conyxDBQuery('select prisp_from, prisp_text from prispevek_cache where id_prispevek = ' + id_prisp)
  if len(rows) > 0:
    for r in (rows):
      print(cleanHtml(r[1]));
      return(r[0])

def nactiNazevKlubu(p_klub_id):
  p_klub_name="?"
  cols,rows=conyxDBQuery('select jmeno from klub_cache where id_klub = "' + str(p_klub_id) + '"')
  if len(rows)>0:
    p_klub_name=rows[0][0].encode("utf-8")
  return(p_klub_name)
  
def zmenKlub(p_klub_id):
  try:
    if p_klub_id != "":
      global i_klub_id
      global i_klub_name
      i_klub_id=int(p_klub_id)
      conyxDBLast(i_klub_id)
      try:
        cols,rows=conyxDBQuery('select jmeno from klub_cache where id_klub = "' + str(i_klub_id) + '"')
        if len(rows)>0:
          i_klub_name=rows[0][0].encode("utf-8")
        else:
          i_klub_name='?'
      except Exception:
        traceback.print_exc(file=sys.stdout)
        print("Tento klub nemam v cache.")
      print("Zvolen klub: " + str(i_klub_id))
    else:
      print("Musis zadat cislo klubu (napr. k 532)")
  except Exception:
    traceback.print_exc(file=sys.stdout)
    print("Nepodarilo se zvolit klub.")
 
class cli(cmd2.Cmd):
  prompt = '|-> '

  def preloop(self):
    print("[ KLUB: " + str(i_klub_id) + " " + nactiNazevKlubu(i_klub_id) + " ]")
    cmd2.Cmd.preloop(self)

  def postloop(self):
    print('[ Loucim se s tebou ]') 

  def precmd(self,line):
    line = cmd2.Cmd.precmd(self, line)
    return line

  # postcmd
  def postcmd(self,stop,line):
    print("[ KLUB: " + str(i_klub_id) + " " + nactiNazevKlubu(i_klub_id) + " ]")
    return(cmd2.Cmd.postcmd(self,stop,line))

  def do_stahniKluby(self, line):
    try:
      nr,buf=nyx_list_disc("",0) # barvicky 1
      print("Stazeno " + str(nr) + " zahlavi klubu.")
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nemuzu stahnout kluby ze serveru")


  def do_odpovez(self,line):
    # priklad: |-> odpovez xxxxxxxx:nickname:odpoved na prispevek
    #p_msg_id=line.split(':')[0]
    p_msg_id=raw_input("Zadej ID prispevku pro odpoved: ")
    #p_usr_id=line.split(':')[1]
    if len(p_msg_id) == 0:
      return (0)
    p_usr_est=odhadniKomuJePrispevekUrcen(p_msg_id)
    #print("Myslim, ze chces odpovedet " + p_usr_est)
    p_usr_id=rlinput("Komu chces odpovedet: ",p_usr_est)
    # p_message=line.split(':')[2]
    p_message=raw_input("Text odpovedi: ")
    if len(p_message) > 0:
      nyx_reply_message(i_klub_id,p_message,p_msg_id,p_usr_id)
    else:
      print("Prispevek neodeslan.")

  def do_pis(self, line):
    if len(line) > 0:
      nyx_send_message(i_klub_id,line)

  def do_ctiKlub(self,line):
    print("Nacitam klub do databaze " + str(i_klub_id))
    try:
      buf=nyx_show_disc_msgs(str(i_klub_id))
      print(buf)
      conyxDBGenDML('update klub_cache set unread = "0" where id_klub="'+str(i_klub_id)+'"')
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nepodarilo se ulozit prispevky z aktualni diskuze do databaze")
    cacheVypisPrispevky()

  def do_klub(self,line):
    zmenKlub(line)

#  def do_zmeny(self,line):
#    try:
#      tuiFile('CHANGELOG')
#    except Exception:
#      print("Chyba pri zobrazovani souboru zmen.")
#      traceback.print_exc(file=sys.stdout)

  def do_cache(self,line): # CACHE
    cols,rows=conyxDBQuery('select * from klub_cache where ')
    if len(rows) > 0:
      for r in (rows):
        print(str(r[0]) + "|" + str(r[2]));

  def do_neprectene(self,line): # NEPRECTENE
    cols,rows=conyxDBQuery('select * from klub_cache where unread != "0"')
    if len(rows) > 0:
      for r in (rows):
        print(r[1]+"|"+r[2]+"|"+r[3]+"|"+r[4]);
    else:
      print("Nemas zadne neprectene prispevky v klubech")

  def do_dalsiNeprecteny(self,line): # NEPRECTENE
    cols,rows=conyxDBQuery('select id_klub from klub_cache where cast(unread as decimal) > 0 limit 1')
    if len(rows) > 0:
      for r in (rows):
        print(r[0]);
        zmenKlub(r[0])
    else:
      print("Nemas zadny neprecteny diskuzni klub")
     
  def do_dalsiReakce(self,line): # DALSI KLUB URCENY K REAKCI
    cols,rows=conyxDBQuery('select id_klub from klub_cache where cast(unread as decimal) > 0 and cast(replies as decimal) > 0 limit 1')
    if len(rows) > 0:
      for r in (rows):
        print(r[0]);
        zmenKlub(r[0])
    else:
      print("Nemas zadny neprecteny diskuzni klub s reakci")
 
  def do_reakce(self,line): # REAKCE - PRISPEVKY PRO REAKCI
    cols,rows=conyxDBQuery('select * from klub_cache where unread != "0" and replies != "0"')
    if len(rows) > 0:
      for r in (rows):
        print(r[1]+"|"+r[2]+"|"+r[3]+"|"+r[4]);
    else:
      print("Nikdo vam v klubech nepise")

  def do_historie(self,line): # HISTORIE
    try:
      print("Historie navstivenych klubu")
      cols,rows=conyxDBQuery('select id_klub || " " || klub_cache.jmeno line from last, klub_cache where last.forum_id = id_klub order by last.rowid desc limit 10')
      if len(rows)>0:
        for r in rows:
          print(r[0])
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nemuzu zobrazit posledni navstivene podle docasne pameti")

  def do_posledniAdresati(self,line): # HISTORIE ADRESATU
    try:
      print("Naposledy jsi psal")
      rx=nyx_filter_mail(p_user,p_text)
      if rx>0:
        print("Nasel jsem "+str(rx)+" dopisu. Muzes je precit pomoci cp (ctiPostu)")
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nemuzu najit hledany dopis.")


  def do_hledejDopis(self,line): # HISTORIE
    try:
      print("Hledam dopis")
      p_user=raw_input("Od koho hledas dopis: ")
      p_text=raw_input("Text, ktery obsahuje dopisu: ")
      rx=nyx_filter_mail(p_user,p_text)
      if rx>0:
        print("Nasel jsem "+str(rx)+" dopisu. Muzes je precit pomoci cp (ctiPostu)")
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nemuzu najit hledany dopis.")


  def do_napisDopis(self,line): # HISTORIE
    try:
      print("Napis dopis")
      p_recipient=raw_input("Komu je urcen: ")
      if len(p_recipient)>0:
        p_message=raw_input("Text dopisu: ")
        if len(p_message)>0:
          nyx_send_mail(p_recipient,p_message)
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nemuzu zaslat dopis.")

  def do_ctiPostu(self,line): # HISTORIE
    try:
      print("Dorucena posta")
      cols,rows=conyxDBQuery("select case when direction = 'from' then 'od' else 'komu' end || ' ' || other_nick || '|' || content from mail order by rowid desc")
      if len(rows)>0:
        for r in rows:
          print(r[0])
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nemuzu zobrazit stazenou postu")


  def do_stahniPostu(self, line):
    try:
      nr=nyx_list_mail()
      print("Stazeno " + str(nr) + " postovanich zprav.")
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nemuzu stahnout postu ze serveru")


  do_sp=do_stahniPostu
  do_hd=do_hledejDopis
  do_cp=do_ctiPostu
  do_np=do_napisDopis

  do_sk=do_stahniKluby
  do_n=do_neprectene
  do_r=do_reakce
  do_k=do_klub
  do_c=do_ctiKlub
  do_cti=do_ctiKlub
  do_cist=do_ctiKlub
  do_o=do_odpovez
  do_p=do_pis
  do_h=do_historie
  do_nnp=do_dalsiNeprecteny
  do_nr=do_dalsiReakce

#  def do_tui(self,line):
#    try:
#      tuiMainScreen()
#    except Exception:
#      print("Chyba pri inicializaci textoveho grafickeho rozhrani.")
#      traceback.print_exc(file=sys.stdout)

def conyx_main():
  global i_klub_id
  p_nickname = get_auth_nickname()
  if p_nickname == "":
    p_nickname=raw_input("Zadej ID: ")
    conyxDBUpdNickname(p_nickname)
  if (nyx_auth(p_nickname)==0):
    cols, rows = conyxDBQuery('select * from last where rowid = (select max(rowid) from last)')
    if len(rows)>0:
      i_klub_id = rows[0][0]
    else:
      i_klub_id = 1
    #print (str(rows[0][0]))
    cli().cmdloop()
