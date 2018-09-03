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
# version 0.1.1
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
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import urllib
import json
import re
import curses
import datetime
from colorama import Fore, Style
from conyxDBQuery import conyxDBQuery
from conyxDBAuth import conyxDBStoreAuth
from conyxDBUpdNickname import conyxDBUpdNickname
from conyxDBGenDML import conyxDBGenDML
from conyxDBGenDMLVars import conyxDBGenDMLVars

