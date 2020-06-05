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
import sqlite3
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'./lib'))
from conyxDBLocation import conyxDBLocation

con = None

def conyxDBQuery(qry):
  try:
    cols = []
    con = sqlite3.connect(conyxDBLocation())
    con.row_factory=sqlite3.Row
    c = con.cursor()
    c.execute(qry)
    rows = c.fetchall()
    #print (cols)
    #print (rows)
    return (cols, rows)
  except Exception:
    traceback.print_exc(file=sys.stdout)
    print ("ERR [ CONYX FAILED TO READ FROM DATABASE ] 001040x0010 (1) : CONYX Failed to Connect to DB")	

#DEBUG
#cols, rows = conyxDBQuery('select auth_key from auth')
#print (str(rows[0][0]))

