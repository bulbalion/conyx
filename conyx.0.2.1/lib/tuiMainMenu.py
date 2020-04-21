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
# version 0.2.1
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
#reload(sys)
#sys.setdefaultencoding('utf8')
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from math import *
import curses
from conyxDBQuery import conyxDBQuery
import locale
import sys
import re
from conyxOps import *
from tuiBuffer import * 

actual_char='>'
height=0
width=0

#def nactiSeznamKlubu():

# BUGS
# ukazuje i mimo posledni prvek
def tuiMainMenu(typ_klubu=0):
  global tui_klub_id
  nr,buf=nyx_list_disc("",0) # stahni zahlavi klubu
  strings=[]
  screen = curses.initscr()
  curses.noecho()
  curses.cbreak()
  curses.start_color()
  screen.keypad(1)
  curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
  global width
  global height
  height,width=screen.getmaxyx()
  last_pos=1
  last_page=1
  encoding = locale.getpreferredencoding()
  locale.setlocale(locale.LC_ALL, '')
  x=""
  pages=0
  page=0
  row_num=0
  try:

    if 1==1: # last_pos!=0 and row_num>0:
      highlightText=curses.color_pair(1)
      normalText=curses.A_NORMAL
      max_row=height-2
      box=curses.newwin(height+1,width+1,0,0)
      pages=int(ceil(row_num/max_row))
      position=last_pos 
      page=last_page
        
      while x != ord('q'): # dokud neni stisknuta klavesa 'q'

        box.erase()

        # POKUS NACIST KLUBY PRED KAZDYM NAVRATEM Z KLUBU
        if typ_klubu==1:
          cols,rows=conyxDBQuery("select id_klub, id_klub||'|'||jmeno||'|'||unread||'|'||replies txt from klub_cache where unread != '0' order by jmeno asc")
          #box.addstr(0,0,"Nacten seznam neprectenych klubu")
        elif typ_klubu==2:
          cols,rows=conyxDBQuery("select id_klub, id_klub||'|'||jmeno||'|'||unread||'|'||replies txt from klub_cache where unread != '0' and replies != '0' order by jmeno asc")
        elif typ_klubu==3:
          cols,rows=conyxDBQuery("select distinct id_klub, id_klub||'|'||jmeno||'|'||unread||'|'||replies txt from klub_cache, last where last.forum_id = klub_cache.id_klub")
        elif typ_klubu==4:
          cols,rows=nyx_bookmarks_history()
        else:
          cols,rows=conyxDBQuery("select id_klub, id_klub||'|'||jmeno||'|'||unread||'|'||replies txt from klub_cache order by jmeno asc")
        strings=[]
        refs=[]
        ret=0
        row_num=len(strings)
        for i in rows:
          strings.append(cleanHtml(i[1].replace('\n',' ')))
          refs.append(i[0])
        row_num=len(strings)
        #if last_pos!=0 and row_num>0:
        tmp=[] 
        for i in strings:
          tmp.append(i[:width-10])
        strings=tmp
        # highlightText=curses.color_pair(1)
        pages=int(ceil(row_num/max_row))
        

        box.addstr(height-1,0,"pos " + str(position) + " page " + str(page) + " mr " + str(max_row) + " row_num " + str(row_num))

        for i in range(1+(max_row*(page-1)),max_row+1+(max_row*(page-1))):
          if row_num == 0:
            if typ_klubu==1:
              box.addstr(1,1,"Zadny dalsi neprecteny klub.",highlightText)
            elif typ_klubu==2:
              box.addstr(1,1,"Zadny dalsi klub s reakci.",highlightText)
            else:
              box.addstr(1,1,"Zadna data.",highlightText)
          else:
            if (i+(max_row*(page-1))==position+(max_row*(page-1))):
              box.addstr(i-(max_row*(page-1)),2,actual_char+" "+cleanHtml(sutf8(strings[i-1])), highlightText)
            else:
              box.addstr(i-(max_row*(page-1)),2,"  "+cleanHtml(sutf8(strings[i-1])),normalText)
          if i==row_num:
            break;

        screen.refresh()
        box.refresh()
        x = screen.getch()
 
        ret=0
        if ( x==curses.KEY_DOWN or x==106 ) and position < row_num: # j - down
          if position<max_row+(max_row*(page-1)):
            position=position+1
          else:
            if page<=pages:
              page=page+1
              position=1+(max_row*(page-1))
        if ( x == curses.KEY_UP or x==107 ) and position > 1: # k - up
          if position>1+(max_row*(page-1)):
            position=position-1
          else:
            page=page-1
            position=max_row+(max_row*(page-1))
        if x == curses.KEY_LEFT or x == 104: # h - left
          if page > 1:
            page=page-1
            position=1+(max_row*(page-1))
        if x == curses.KEY_RIGHT or x == 108: # l - right
          if page<=pages: 
            page=page+1
            position=1+(max_row*(page-1))
        if x == ord( "\n" ) and row_num != 0:
          screen.erase()
          ret=refs[position-1] 
        
        if ret!=0:
          buf=nyx_show_disc_msgs(str(ret))
          cols, rows = conyxDBQuery('select prisp_from || "|" || prisp_text || "|" ||  prisp_hodnoceni wu_rating from prispevek_cache')
          buffer=[]
          for i in rows:
            buffer.append(i[0])
          #if len(rows)>0:
          #  klub_name=getKlubNameFromID(ret)[:width-10]
          #  tuiBuffer(klub_name,buffer)
          #conyxDBGenDML('update klub_cache set unread = "0" where id_klub="'+str(ret)+'"')
          #if (ret):
          tui_klub_id = ret
          conyxDBLast(tui_klub_id)
          #else:
          #  tui_klub_id = orig_tui_klub_id
          #screen.addstr(0,0,"Vybran klub: " + tui_klub_id) # DEBUG
          #screen.getch()
          return(tui_klub_id)
    else:
      screen.addstr(0,0,"Nemas zadne neprectene kluby.")
      screen.getch()
    curses.endwin()
  except Exception:
    curses.endwin()
    traceback.print_exc(file=sys.stdout)
    print("Problem s textovym uzivatelskym rozhranim")
    print("Na strance: " + str(page))
    #input("Stiskni klavesu...")
    #time.sleep(5)

# DEBUG
#tuiMainMenu()
