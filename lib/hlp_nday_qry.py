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

# -*- coding: utf-8 -*-

import sys, os, traceback
import sqlite3
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'./lib'))
from conyxDBLocation import conyxDBLocation

con = None

def hlp_nday_qry(qry):
  try:
    if ('CONYX') in os.environ:
      nday_db=(os.environ['CONYX'] + "/db/jmeniny.db")
    else:
      if (os.path.isfile('jmeniny.db')):
        nday_db="jmeniny.db"
      elif (os.path.isfile('../db/jmeniny.db')):
        nday_db="../db/jmeniny.db"
    con = sqlite3.connect(nday_db)
    con.row_factory=sqlite3.Row
    c = con.cursor()
    c.execute(qry)
    rows = c.fetchall()
    #print (cols)
    #print (rows)
    return (rows)
  except Exception:
    traceback.print_exc(file=sys.stdout)
    print ("ERR [ CONYX FAILED TO READ FROM DATABASE ] 001040x0010 (1) : CONYX Failed to Connect to DB")	

#DEBUG
#rows = hlp_nday_qry("select name from jmeniny where date = '01-01'")
#print (rows[0][0])

