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
# version 0.0.9 gamma 
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
from conyxDBLast import conyxDBLast
from conyxDBQuery import conyxDBQuery
from conyxDBUpdNickname import conyxDBUpdNickname
from tuiFile import *
from tuiMainScreen import *

if __name__ == '__main__':
  locale.setlocale(locale.LC_ALL, '')
  p_nickname = get_auth_nickname()
  if p_nickname == "":
    p_nickname=raw_input("Zadej ID: ")
    conyxDBUpdNickname(p_nickname)
  if (nyx_auth(p_nickname)==0):
    try:
      tuiMainScreen()
    except Exception:
      print("Chyba pri inicializaci textoveho grafickeho rozhrani.")
      traceback.print_exc(file=sys.stdout)
