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

import sys, os, traceback
if ('CONYX') in os.environ:
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

import sys, os, traceback


global i_klub_id

def do_tui():
    try:
      tuiMainScreen()
    except Exception:
      print("Chyba pri inicializaci textoveho grafickeho rozhrani.")
      traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
#def main():
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
