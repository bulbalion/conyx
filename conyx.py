#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Nyx Human Interface 
#
# version 0.0.8 beta
#
# You can do whatever You want with Conyx.
# But I don't take reponsbility nor even
# implied responsibility for the negative
# impact of Your acting.
#

#-*- coding: utf-8 -*-

import sys, os, traceback
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from nyxOp import *
import cmd2 as cmd2
from conyxDBLast import conyxDBLast
from conyxDBQuery import conyxDBQuery
from conyxDBUpdNickname import conyxDBUpdNickname
from tuiFile import *
from tuiMainScreen import *

i_klub_id=-1

def zvol_klub(inp):
  i_klub_id = inp 

def aktualni_klub():
  return (i_klub_id)

def do_posledni(self,line):
  rows=conyxDBQuery('select forum_id from last order by rowid desc limit 16')
  res=""
  for r in rows:
    for v in r:
      res+=str(v[0])+ " " 
  print(res)

class cli(cmd2.Cmd):
  prompt = '|-> '

  def preloop(self):
     cmd2.Cmd.preloop(self)   ## sets up command completion
     print("[ KLUB: " + str(i_klub_id) + " ]")

  def precmd(self,line):
    print("[ KLUB: " + str(i_klub_id) + " ]") # possibly add error processing here
    line = cmd2.Cmd.precmd(self, line)
    return line

  def do_sledovane(self, line):
    if line!="": 
      buf=nyx_list_disc(line,0) # barvicky 1
      for row in buf:
        print(row)
      print('pouzit filtr nad sledovanymi ' + line)
    else:
     buf=nyx_list_disc(line,0) # barvicky 1
     for row in buf:
       print(row)

  def do_posledni(self,line):
    rows=conyxDBQuery('select distinct forum_id from last order by rowid desc limit 16')
    res=""
    for r in rows:
      for v in r:
        res+=str(v[0])+ " " 
    print(res)

  def do_odpoved(self,line):
    p_msg_id=line.split(':')[0]
    p_usr_id=line.split(':')[1]
    p_message=line.split(':')[2]
    nyx_reply_message(i_klub_id,p_message,p_msg_id,p_usr_id)

  def do_pis(self, line):
    nyx_send_message(i_klub_id,line)

  def do_cti(self,line):
    print("Ctu klub " + str(i_klub_id))
    buf=nyx_show_disc_msgs(str(i_klub_id),0)
    for ln in buf:
      print(ln)

  def do_klub(self,line):
    try:
      global i_klub_id
      i_klub_id=int(line)
      print("Zvolen klub: " + str(i_klub_id))
      conyxDBLast(i_klub_id)
    except Exception:
      traceback.print_exc(file=sys.stdout)
      print("Nepodarilo se zvolit klub.")

  def do_zmeny(self,line):
    try:
      tuiFile('CHANGELOG')
    except Exception:
      print("Chyba pri zobrazovani souboru zmen.")
      traceback.print_exc(file=sys.stdout)

  def do_tui(self,line):
    try:
      tuiMainScreen()
    except Exception:
      print("Chyba pri inicializaci textoveho grafickeho rozhrani.")
      traceback.print_exc(file=sys.stdout)



def conyx_main():
  global i_klub_id
  p_nickname = get_auth_nickname()
  if p_nickname == "":
    p_nickname=raw_input("Zadej ID: ")
    conyxDBUpdNickname(p_nickname)
  if (nyx_auth(p_nickname)==0):
    cols, rows = conyxDBQuery('select * from last where rowid = (select max(rowid) from last)')
    i_klub_id = rows[0][0]
    #print (str(rows[0][0]))
    cli().cmdloop()

if __name__ == '__main__':
  conyx_main()
