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

# -*- coding: utf-8 -*-

import sys, os, traceback
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from conyxDBLocation import conyxDBLocation
import sqlite3
import datetime


def conyxDBStoreAuth(p_auth_key):

  try:
    conn=sqlite3.connect(conyxDBLocation())
    cur = conn.cursor()
    cur.execute("update auth set auth_key = ?",(p_auth_key,))
    conn.commit()
    conn.close()
  except Exception:
    traceback.print_exc(file=sys.stdout)
    print ("ERR [ FAILED STORE AUTH KEY ] 001040x0010 (1) : Cannot store Authorization Key")

#DEBUG
#print conyxDBStoreAuth('123')
