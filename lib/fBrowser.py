# encoding=utf-8
#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Text User Interface Main Menu Library
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

import curses
from math import *

actual_char='>'
  
import sys, os, traceback
#reload(sys)
#sys.setdefaultencoding('utf8')
from conyxOps import *
from sutf8 import sutf8
import locale
import re
from tuiConfig import getConfig, updateConfig

if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from ls import ls

def fBrowser(strings,last_pos,last_page):
  #def fBrowser():
  screen = curses.initscr()
  curses.start_color()
  curses.noecho()
  row_num = len(strings)
  height,width=screen.getmaxyx()
  tmp=[] 
  for i in strings:
    tmp.append(i[:width-4])
  strings=tmp
  curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
  hiTe=curses.color_pair(1)
  noTe=curses.A_NORMAL
  max_row=height-1
  box=curses.newwin(max_row+2,width,0,0)
  #box.box()
 
  pages=int(ceil(row_num/max_row))
  position=last_pos 
  page=last_page
  
  screen.refresh()
  box.refresh()

  x = None 
  page=0
  while x != ord('q'): # dokud neni stisknuta klavesa 'q'
    if x==curses.KEY_DOWN or x==ord('j'):
      if (position%max_row<max_row-1 and position<row_num-1): 
        position=position+1
    elif x == curses.KEY_UP or x==ord('k'):
      if (position%max_row>0 and position>0): position = position - 1
    elif x == curses.KEY_LEFT or x==ord('h'):
      if (page>0): page-=1; position=max_row*page+max_row-1
    elif x == curses.KEY_RIGHT or x==ord('l'):
      if (page<pages-1): page+=1; position=max_row*page
    elif x == ord('r'):
      dir=str(getConfig('soubory')[0][0])
      os.chdir(dir)
      strings = ls('.','py')
      pages=int(ceil(row_num/max_row))
      row_num = len(strings)
      position=0
      page=0
    elif x == ord('d'):
      y=None
      dir=str(getConfig('soubory')[0][0])
      while y!=ord('\n'):
        box.addstr(height-1,0,(" "*(width-1)))
        box.addstr(height-1,0,"Directory: "+str(dir))
        screen.refresh()
        box.refresh()
        y=screen.getch()
        if y in (curses.KEY_BACKSPACE,263,127):
          dir=dir[:-1]
        else:
          dir+=chr(y)
      if (len(dir)>0):
        dir=dir[:-1]
        updateConfig('soubory',dir)
        strings = ls(dir,'')
        pages=int(ceil(row_num/max_row))
        row_num=len(strings)
        position=0
        page=0
    elif x == ord('f'):
      y=None
      filter=""
      while y!=ord('\n'):
        box.addstr(height-1,0,(" "*(width-1)))
        box.addstr(height-1,0,"Filter: "+str(filter))
        screen.refresh()
        box.refresh()
        y=screen.getch()
        if y in (curses.KEY_BACKSPACE,263,127):
          filter=filter[:-1]
        else:
          filter+=chr(y)
      if (len(filter)>0):
        filter=filter[:-1]
      tmp=[]
      for i in strings:
        if filter in i:
          tmp.append(i)
      strings=tmp
      if filter=="":
        strings = ls('.','')
      pages=int(ceil(row_num/max_row))
      row_num=len(strings)
      position=0
      page=0
    elif x == ord("\n"):
      screen.erase()
      if not (strings[position] is None and position < row_num):
        return(strings[position])
      else:
        return(None)
  
    box.erase()

    shift=page*max_row
    for i in range(0,max_row):
      if row_num == 0:
        box.addstr(1,1,"Zadna data.",hiTe)
      elif i+shift==row_num:
        break
      else:
        if (i+shift==position):
          box.addstr(i,2,actual_char+" "+sutf8(strings[i+shift][:width-5]), hiTe)
        else:
          box.addstr(i,2,"  "+sutf8(strings[i+shift][:width-5]),noTe)
  
    footer="-=[ Keys: j,k,l,h,q,f,r,d,ENTER shift: "+str(shift) + " i: " + str(i) + " pos: " + str(position) + "]=-"
    if (len(footer)>=height-1):
      footer="-=[ Keys: j,k,l,h,q,f,r,d,ENTER ]=-"
    box.addstr(height-1,0,footer,noTe)
    screen.refresh()
    box.refresh()
    x = screen.getch()
  

## DEBUG
#strings = ls('..','py')
#sel=fBrowser(strings,0,0)
#curses.endwin()
#print("Vyber souboru: " + sel)
