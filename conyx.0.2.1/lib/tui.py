#-*- coding: utf-8 -*-

import sys, os, traceback
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from nyxOp import *
from conyxDBLast import conyxDBLast
from nyxMail import * 
from conyxDBQuery import conyxDBQuery
from conyxDBGenDML import conyxDBGenDML
from conyxDBGenDMLVars import conyxDBGenDMLVars
from conyxDBUpdNickname import conyxDBUpdNickname
from tuiFile import *
from tuiMainScreen import *
import readline

import sys, os, traceback
sys.path.insert(0, (os.environ['CONYX']+'/lib'))

global i_klub_id

def do_tui():
    try:
      tuiMainScreen()
    except Exception:
      print("Chyba pri inicializaci textoveho grafickeho rozhrani.")
      traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
  global i_klub_id
  p_nickname = get_auth_nickname()
  if p_nickname == "":
    p_nickname=input("Zadej ID: ") # v0.1.9 raw_input -> input
    conyxDBUpdNickname(p_nickname)
  if (nyx_auth(p_nickname)==0):
    cols, rows = conyxDBQuery('select * from last where rowid = (select max(rowid) from last)')
    if len(rows)>0:
      i_klub_id = rows[0][0]
    else:
      i_klub_id = 1
    do_tui()
