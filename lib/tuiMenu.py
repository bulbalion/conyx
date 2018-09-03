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
# version 0.1.5
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
reload(sys)
sys.setdefaultencoding('utf8')
import locale
import sys
import re

sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from conyxDBQuery import conyxDBQuery
from conyxOps import *

buffer=[]
cols, rows = conyxDBQuery('select id_klub,jmeno from klub_cache')
for i in rows:
  buffer.append(i[1])

def tuiMenu(refs,strings,last_pos,last_page):
  row_num = len(strings)
  screen = curses.initscr()
  height,width=screen.getmaxyx()
  tmp=[] 
  for i in strings:
    tmp.append(i[:width-4])
  strings=tmp
  curses.noecho()
  curses.cbreak()
  curses.start_color()
  screen.keypad(1)
  curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
  highlightText=curses.color_pair(1)
  normalText=curses.A_NORMAL
  max_row=height-2
  box=curses.newwin(max_row+2,width,0,0)
  #box.box()
 
  pages=int(ceil(row_num/max_row))
  position=last_pos 
  page=last_page
  #for i in range(1+(max_row*(page-1)),max_row+1+(max_row*(page-1))):
  #for i in range(1,max_row+1):
  #  if row_num == 0:
  #    box.addstr(1,1,"There aren't strings", highlightText )
  #  else:
  #    #if (i == position):
  #    if (i+(max_row*(page-1))==position+(max_row*(page-1))):
  #      box.addstr(i,2,actual_char+" "+cleanHtml(strings[i-1]),highlightText )
  #    else:
  #      box.addstr(i-(max_row*(page-1)),2,"  "+cleanHtml(strings[i-1]),normalText)
  #      #box.addstr(i,2,"  "+cleanHtml(strings[i-1]),normalText)
  #    if i == row_num:
  #      break
  for i in range(1+(max_row*(page-1)),max_row+1+(max_row*(page-1))):
    if row_num == 0:
      box.addstr(1,1,"Zadna data.",highlightText)
    else:
      if (i+(max_row*(page-1))==position+(max_row*(page-1))):
        box.addstr(i-(max_row*(page-1)),2,actual_char+" "+cleanHtml(strings[i-1]), highlightText)
      else:
        box.addstr(i-(max_row*(page-1)),2,"  "+cleanHtml(strings[i-1]),normalText)
    if i == row_num:
      break
  
  screen.refresh()
  box.refresh()
  
  x = screen.getch()
  while x != 113: # dokud neni stisknuta klavesa 'q'
    if x==curses.KEY_DOWN:
       if page==1:
         if position<i:
           position=position+1
         else:
           if pages>1:
             page=page+1
             position=1+(max_row*(page-1))
       elif page==pages:
         if position<row_num:
           position=position+1
       else:
         if position<max_row+(max_row*(page-1)):
           position=position+1
         else:
           page=page+1
           position=1+(max_row*(page-1))
    if x == curses.KEY_UP:
      if page == 1:
          if position > 1:
            position = position - 1
      else:
          if position > ( 1 + ( max_row * ( page - 1 ) ) ):
            position = position - 1
          else:
            page = page - 1
            position = max_row + ( max_row * ( page - 1 ) )
    if x == curses.KEY_LEFT:
      if page > 1:
         page=page-1
         position=1+(max_row*(page-1))
  
    if x == curses.KEY_RIGHT:
      if page < pages:
         page = page + 1
         position = ( 1 + ( max_row * ( page - 1 ) ) )
    if x == ord( "\n" ) and row_num != 0:
      screen.erase()
      #screen.addstr(2,1,"Polozka "+str(refs[position-1]))
      #screen.getch()
      return(refs[position-1],position+1,page)
  
    box.erase()

    for i in range(1+(max_row*(page-1)),max_row+1+(max_row*(page-1))):
      if row_num == 0:
        box.addstr(1,1,"Zadna data.",highlightText)
      else:
        if (i+(max_row*(page-1))==position+(max_row*(page-1))):
          box.addstr(i-(max_row*(page-1)),2,actual_char+" "+cleanHtml(strings[i-1]), highlightText)
        else:
          box.addstr(i-(max_row*(page-1)),2,"  "+cleanHtml(strings[i-1]),normalText)
      if i == row_num:
        break
  
  
  
    screen.refresh()
    box.refresh()
    x = screen.getch()
  
  curses.endwin()

# BUGS
# ukazuje i mimo posledni prvek
# DEBUG
#encoding = locale.getpreferredencoding()
#locale.setlocale(locale.LC_ALL, '')
#try:
#  tuiMenu(buffer)
#except Exception:
#  curses.endwin()
#  traceback.print_exc(file=sys.stdout)
#  print("Problem s textovym uzivatelskym rozhranim")
#  exit()
