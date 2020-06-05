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

import os

resp = "EMPTY"

def conyxDBLocation():
  if ('CONYX') in os.environ:
    resp=(os.environ['CONYX'] + "/db/conyx.db")
  else:
    if (os.path.isfile('conyx.db')):
      resp="conyx.db"      
    elif (os.path.isfile('../db/conyx.db')):
      resp="../db/conyx.db"
  return(resp)

# DEBUG
#resp = conyxDBLocation()
#print resp
