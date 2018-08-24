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
import curses, locale
from curses.textpad import Textbox, rectangle
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from conyxDBQuery import conyxDBQuery
from tuiBuffer import tuiBuffer 
from tuiFile import tuiFile
from nyxOp import *
from conyxDBLast import conyxDBLast

boxtext=""
tui_klub_id=-1

def maketextbox(h,w,y,x,value="zvolklub",deco=None,textColorpair=0,decoColorpair=0):
  #curses.noecho()
  #curses.cbreak()
  #stdscr.keypad(1)
  #stdscr.clear()
  #stdscr.refresh()
  win = curses.newwin(5, 60, 5, 10)
  tb = curses.textpad.Textbox(win)
  text = tb.edit()
  nw = curses.newwin(h,w,y,x)
  txtbox = curses.textpad.Textbox(nw)
  screen.attron(decoColorpair)
  curses.textpad.rectangle(screen,y-1,x-1,y+h,x+w)
  screen.attroff(decoColorpair)
  nw.addstr(0,0,value,textColorpair)
  nw.attron(textColorpair)

def stripDia(in_str):
  return(in_str.encode('ascii','ignore'))

def draw_menu(stdscr):
  global tui_klub_id
  k = 0
  cursor_x = 0
  cursor_y = 0

  encoding = locale.getpreferredencoding()
  locale.setlocale(locale.LC_ALL, '')

  #stdscr = curses.initscr()

  # Clear and refresh the screen for a blank canvas
  stdscr.clear()
  stdscr.refresh()

  # Start colors in curses
  curses.start_color()
  curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

  # Loop where k is the last character pressed
  while (k != ord('q')):

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    if k == curses.KEY_DOWN:
      cursor_y = cursor_y + 1
    elif k == curses.KEY_UP:
      cursor_y = cursor_y - 1
    elif k == curses.KEY_RIGHT:
      cursor_x = cursor_x + 1
    elif k == curses.KEY_LEFT:
      cursor_x = cursor_x - 1
    elif k == 122: # Z - zmeny
      try:
        tuiFile("CHANGELOG") 
      except Exception:
        print("Nemuzu zobrazit seznam zmen.")
    elif k == 115: # S - sledovane
      try:
        disp=""
        buf=nyx_list_disc('nove',0)
        for ln in buf:
          disp+=ln+'\n' 
        tuiBuffer('Sledovane nove',disp,0) # ZACNI OD SHORA
      except Exception:
        traceback.print_exc(file=sys.stdout)
        input("Zmackni Enter ...")
        print("Nemuzu zobrazit seznam sledovanych.")
    elif k == 99: # C - cti
      try:
        disp=""
        buf=nyx_show_disc_msgs(str(tui_klub_id),0) ### TODO FROM INPUT
        for ln in buf:
          disp+=ln+'\n' 
        tuiBuffer('klub',disp,1) # ZACNI ODSPODA
      except Exception:
        traceback.print_exc(file=sys.stdout)
        input("Zmackni Enter ...")
        print("Nelze zobrazit seznam sledovanych.")
    elif k == 112: # P - pis
      try:
        stdscr.refresh()
        curses.cbreak()
        stdscr.addstr(1,3,"Tvuj prispevek: [ ctrl+g nebo zaplneni okenka pro odeslani ]".encode("utf-8"))
        #start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        # x=4;y=4;h=int(height//2);w=int(width-4)
        x=4;y=4;h=18;w=int(70)
        rectangle(stdscr,x-1,y-1,y+h,x+w)
        editwin = curses.newwin(h,w,x,y)
        stdscr.refresh()
        box=Textbox(editwin)
        box.edit()
        text=box.gather()
        try:
          if (text!=""): 
            nyx_send_message(tui_klub_id,text[:-2]) 
            stdscr.addstr(4, 4, "Prispevek odeslan do klubu: " + str(tui_klub_id ))
            #traceback.print_exc(file=sys.stdout)
            stdscr.getch()
        except Exception:
          stdscr.addstr(0, 0, "Nepodarilo se odeslat prispevek")
          #traceback.print_exc(file=sys.stdout)
          stdscr.getch()
        stdscr.refresh()
        stdscr.clear()
      except Exception:
        traceback.print_exc(file=sys.stdout)
        input("Zmackni Enter ...")
        print("Problem pri ziskani cisla klubu.")
    elif k == 107: # K - klub
      try:
        stdscr.refresh()
        curses.cbreak()
        stdscr.addstr(1,3,"Vyber klub (cislo):".encode("utf-8"))
        x=4;y=4;h=1;w=12
        rectangle(stdscr,x-1,y-1,y+h,x+w)
        editwin = curses.newwin(h,w,x,y)
        stdscr.refresh()
        box=Textbox(editwin)
        box.edit()
        text=box.gather()
        try:
          if (text!=""): 
            tui_klub_id=int(text)
            conyxDBLast(tui_klub_id)
        except Exception:
          stdscr.addstr(0, 0, "Neplatny vyber klubu")
          traceback.print_exc(file=sys.stdout)
          stdscr.getch()    
        stdscr.refresh()
        stdscr.clear()
      except Exception:
        traceback.print_exc(file=sys.stdout)
        input("Zmackni Enter ...")
        print("Problem pri ziskani cisla klubu.")

    cursor_x = max(0, cursor_x)
    cursor_x = min(width-1, cursor_x)

    cursor_y = max(0, cursor_y)
    cursor_y = min(height-1, cursor_y)

    # Declaration of strings
    title = "C O N Y X"[:width-1]
    subtitle = "CONSOLE NYX CLIENT"[:width-1]
    #keystr = "Posledni klavesa: {}".format(k)[:width-1] + " KLUB: " + str(tui_klub_id)
    keystr = " KLUB: " + str(tui_klub_id)
    #statusbarstr = "(q)uit | (k)lub (s)ledovane (c)ti | (z)meny | Pos: {}, {}".format(cursor_x, cursor_y)
    statusbarstr = "(q)uit | (k)lub (s)ledovane (c)ti (p)is | (z)meny |"
    credits = "GIOMIKY MMXVIII"
    if k == 0:
      keystr = "Vitej zpet do klubu {}".format(str(tui_klub_id))

    # Centering calculations
    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
    start_x_credits = int((width // 2) - (len(credits) // 2) - len(credits) % 2)
    start_y = int((height // 2) - 4)

    # Rendering some text
    #whstr = "Width: {}, Height: {}".format(width, height)
    #stdscr.addstr(0, 0, whstr, curses.color_pair(1))

    # Render status bar
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    stdscr.addstr(start_y, start_x_title, title)

    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    # Print rest of text
    stdscr.addstr(start_y + 2, start_x_subtitle, subtitle)
    #stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
    stdscr.addstr(start_y + 4, start_x_keystr, keystr)
    stdscr.addstr(start_y + 6, start_x_credits, credits)
    stdscr.move(cursor_y, cursor_x)

    # Refresh the screen
    stdscr.refresh()

    # Wait for next input
    k = stdscr.getch()

def tuiMainScreen():
  encoding = locale.getpreferredencoding()
  global tui_klub_id
  cols, rows = conyxDBQuery('select * from last where rowid = (select max(rowid) from last)')
  tui_klub_id = rows[0][0]
  curses.wrapper(draw_menu)

# DEBUG
#tuiMainScreen()
