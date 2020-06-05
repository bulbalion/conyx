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

import sys, os, traceback
#reload(sys)
#sys.setdefaultencoding('utf8')
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from math import *
import curses
from conyxDBQuery import conyxDBQuery
import locale
import sys
import re
from conyxOps import *
from tuiBuffer import * 
import unicodedata # HERE # IS IT DEFAULT
from ugetch import ugetch
from conyxDBLast import conyxDBLast
from conyxDBSetForumLast import conyxDBSetForumLast
from nyxOp import *
from sutf8 import sutf8

actual_char='>'
height=0
width=0

#def nactiSeznamKlubu():

def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
    if unicodedata.category(c) != 'Mn')

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
  code = locale.getpreferredencoding()
  x=""
  pages=0
  page=0
  row_num=0
  smode=0
  try:
    if 1==1: # last_pos!=0 and row_num>0:
      highlightText=curses.color_pair(1)
      normalText=curses.A_NORMAL
      max_row=height-2
      box=curses.newwin(height,width,0,0)
      pages=int(ceil(row_num/max_row))
      position=last_pos 
      page=last_page
      search_substr=""  
      # POKUS NACIST KLUBY PRED KAZDYM NAVRATEM Z KLUBU
      while x != ord('q'): # neni stisknuta klavesa 'q'
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
 

        box.erase()

        strings=[]
        refs=[]
        ret=0
        row_num=len(strings)
        for i in rows:
          strings.append(cleanHtml(i[1].replace('\n',' ')))
          refs.append(i[0])
        row_num=len(strings)
        tmp=[]
        refs_tmp=[]
        try:
          if (len(search_substr)>0):
            for i in strings:
              if (search_substr.upper() in strip_accents(i).upper()):
                tmp.append(i[:width-3])
          else:
            for i in strings:
              tmp.append(i[:width-3])
        except Exception as e:
          #curses.endwin()
          traceback.print_exc(file=sys.stdout)
          print("Problem s textovym uzivatelskym rozhranim")
          print("Na strance: " + str(page))
          #height,width=screen.getmaxyx()
	   
        row_num=len(tmp)
        strings=tmp
        # highlightText=curses.color_pair(1)
        pages=int(ceil(row_num/max_row))

        footer="pos " + str(position) + " page " + str(page) + " mr " + str(max_row) + " row_num " + str(row_num) + " | -=[ f - vyhledej, j,k,l,h - pohyb, q - zpet, p - pis ]=-"
        if len(footer)>=width-1:
          footer="-=[ f hledej, j,k,l,h pohyb, p pis, q zpet ]=-"
        box.addstr(height-1,0,footer)

        for i in range(1+(max_row*(page-1)),max_row+1+(max_row*(page-1))):
          if row_num == 0:
            if typ_klubu==1:
              box.addstr(1,0,"Zadny dalsi neprecteny klub.",highlightText)
            elif typ_klubu==2:
              box.addstr(1,0,"Zadny dalsi klub s reakci.",highlightText)
            else:
              box.addstr(1,0,"Zadna data.",highlightText)
          else:
            if (i+(max_row*(page-1))==position+(max_row*(page-1))):
              box.addstr(i-(max_row*(page-1)),0,actual_char+" "+cleanHtml(sutf8(strings[i-1])), highlightText)
            else:
              box.addstr(i-(max_row*(page-1)),0,"  "+cleanHtml(sutf8(strings[i-1])),normalText)
          if i==row_num:
            break;

        search_str="Hledat: "+str(search_substr) 
        box.addstr(0,2,search_str) # y,x
        screen.refresh()
        box.refresh()
        x = ugetch(screen)
 
        ret=0
        try:
          if x in (curses.KEY_DOWN,ord('j')) and smode==0 and position < row_num: # j - down
            if position<max_row+(max_row*(page-1)):
              position=position+1
            else:
              if page<=pages:
                page=page+1
                position=1+(max_row*(page-1))
          elif x in (curses.KEY_UP,ord('k')) and smode==0 and position > 1: # k - up
            if position>1+(max_row*(page-1)):
              position=position-1
            else:
              page=page-1
              position=max_row+(max_row*(page-1))
          elif x in (curses.KEY_LEFT,ord('h'),ord('u')) and smode==0: # h - left
            if page > 1:
              page=page-1
              position=1+(max_row*(page-1))
          elif x in (curses.KEY_RIGHT,ord('l'),ord('n')) and smode==0: # l - right
            if page<pages: 
              page=page+1
              position=1+(max_row*(page-1))
          elif x == ord("f"):
            smode=1 # TURN ON SEARCH MODE
          elif x in (curses.KEY_BACKSPACE, 263, 127) and smode==1: # backspace
            if (len(search_substr)>0):
              search_substr=search_substr[:-1]
          elif x == ord("\n"):
            if (len(strings)>0 and row_num != 0):
              screen.erase()
              strings_split = strings[position-1].split("|")
              try:
                ret=int(strings_split[0])
              except Exception as e:
                ret=1
          else:
            if (smode==1):
              try:
                search_substr+=chr(x)
              except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print("Problem s textovym uzivatelskym rozhranim")
                print("Stisknuta klavesa " + str(ord(x)))
                #height,width=screen.getmaxyx()
                curses.endwin()
                #screen.getch()
                ugetch(screen)
        except Exception as e:
          traceback.print_exc(file=sys.stdout)
          print("Problem s textovym uzivatelskym rozhranim")
          print("Stisknuta klavesa " + str(ord(x)))
        if ret!=0:
          tui_klub_id = ret
          conyxDBLast(tui_klub_id)
          conyxDBSetForumLast(tui_klub_id)
          zobrazDiskuzi(str(tui_klub_id),screen,1)
          screen.clear()      
          #return(tui_klub_id)
    else:
      screen.addstr(0,0,"Nemas zadne neprectene kluby.")
      #screen.getch()
      ugetch(screen)
    curses.endwin()
  except Exception:
    curses.endwin()
    traceback.print_exc(file=sys.stdout)
    print("Problem s textovym uzivatelskym rozhranim")
    print("Na strance: " + str(page))
    input("Stiskni klavesu...")

# DEBUG
#tuiMainMenu()
