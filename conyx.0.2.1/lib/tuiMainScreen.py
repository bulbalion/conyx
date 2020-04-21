# encoding=utf-8
#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Text User Interface Main Screen Library
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
# reload(sys) # v0.1.9
#sys.setdefaultencoding('utf8') # v0.1.9
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import curses, locale
from curses.textpad import Textbox, rectangle
from conyxDBQuery import conyxDBQuery
from tuiBuffer import *
from tuiFile import tuiFile
from nyxOp import *
from conyxDBLast import conyxDBLast
from tuiMainMenu import tuiMainMenu
from conyxOps import *

boxtext=""
global tui_klub_id

def cleanHtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', text)
  cleantext=cleantext.replace('\n',' ')
  cleantext=cleantext.replace('\r',' ')
  return(cleantext)

def nactiNazevKlubu(p_klub_id):
  p_klub_name="?"
  cols,rows=conyxDBQuery('select jmeno from klub_cache where id_klub = "' + str(p_klub_id) + '"')
  if len(rows)>0:
    p_klub_name=rows[0][0]
  else:
    p_klub_name=nyx_disc_header(p_klub_id)
  return(p_klub_name)
 
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
  return(in_str)
  # return(in_str.encode('ascii','ignore'))


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
  klub_strana=1
  # Loop where k is the last character pressed
  while (k != ord('q')):

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    if k == curses.KEY_DOWN:
      cursor_y = cursor_y + 1
    elif k == ord("1"): # 1 - napoveda
      tuiFile("napoveda.txt")
    elif k == curses.KEY_UP:
      cursor_y = cursor_y - 1
    elif k == curses.KEY_RIGHT:
      cursor_x = cursor_x + 1
    elif k == curses.KEY_LEFT:
      cursor_x = cursor_x - 1
    elif k == ord("z"): # Z - zmeny
      try:
        tuiFile("CHANGELOG") 
      except Exception:
        print("Nemuzu zobrazit seznam zmen.")
    elif k == ord("n"): # N - neprectene kluby
      retVal=tuiMainMenu(1)
      if (retVal):
        tui_klub_id=retVal
      stdscr.clear()      
    elif k == ord("r"): # R - kluby s reakci
      retVal=tuiMainMenu(2)
      if (retVal):
        tui_klub_id=retVal
      stdscr.clear()      
    elif k == ord("h"): # H - historie
      retVal=tuiMainMenu(4)
      #retVal=nyx_bookmarks_history()
      if (retVal):
        tui_klub_id=retVal
        conyxDBLast(tui_klub_id)
      klub_strana=1
      stdscr.clear()      
    elif k == ord("s"): # S - sledovane
      retVal=tuiMainMenu(0)
      if (retVal):
        tui_klub_id=retVal
      stdscr.clear()      
    elif k == ord("c"): # C - cti prispevky 
      zobrazDiskuzi(str(tui_klub_id),stdscr,1)
      stdscr.clear()      
    elif k == ord("o"): # O - cti predchozi od nejstarsiho prispevku
      res=conyxDBQuery('select min(id_prispevek) prid from prispevek_cache')
      ret=zobrazDiskuzi(str(tui_klub_id),stdscr,1,res[1][0][0],"older")
      res_aft=conyxDBQuery('select min(id_prispevek) prid from prispevek_cache')
      if (res!=res_aft):
        klub_strana+=1      
      stdscr.clear()      
    elif k == ord("w"): # W - vyhledej writeup na celem Nyxu
      stdscr.addstr(1,3,"Hledej klicove slovo na celem Nyxu: [ ctrl+g pro odeslani ]")
      x=4;y=4;h=18;w=int(70)
      rectangle(stdscr,x-1,y-1,y+h,x+w)
      editwin = curses.newwin(h,w,x,y)
      stdscr.refresh()
      box=Textbox(editwin)
      box.edit()
      text=box.gather()
      if text:
        rx,res=nyx_search_writeups(None,text,None)
        buffer=[]
        for i in res["data"]:
          buffer.append(i["klub_jmeno"]+"|"+i["nick"]+"|"+cleanhtml(i["content"]))
        tuiBuffer("Vysledek hledani",buffer)
    elif k == ord("v"): # V - vyhledat klicove slovo
      stdscr.addstr(1,3,"Hledej klicove slovo v prispevcich:")
      x=4;y=4;h=18;w=int(70)
      rectangle(stdscr,x-1,y-1,y+h,x+w)
      editwin = curses.newwin(h,w,x,y)
      stdscr.refresh()
      box=Textbox(editwin)
      box.edit()
      text=box.gather()
      ret=zobrazDiskuzi(str(tui_klub_id),stdscr,1,None,None,None,text)
      stdscr.clear()     
    elif k == ord("l"): # B - vyhledat prispevky uzivatele
      stdscr.addstr(1,3,"Hledej prispevky od: [ ctrl+g pro odeslani ]")
      x=4;y=4;h=18;w=int(70)
      rectangle(stdscr,x-1,y-1,y+h,x+w)
      editwin = curses.newwin(h,w,x,y)
      stdscr.refresh()
      box=Textbox(editwin)
      box.edit()
      text=box.gather()
      ret=zobrazDiskuzi(str(tui_klub_id),stdscr,1,None,None,text)
      stdscr.clear()     
    elif k == ord("e"): # U - cti nasledujici od nejnovejsiho prispevku
      res=conyxDBQuery('select max(id_prispevek) prid from prispevek_cache')
      ret=zobrazDiskuzi(str(tui_klub_id),stdscr,1,res[1][0][0],"newer")
      if (klub_strana>1):
        klub_strana-=1      
      stdscr.clear() 
    elif k == ord("p"): # P - pis
      try:
        stdscr.refresh()
        curses.cbreak()
        stdscr.addstr(1,3,"Tvuj prispevek: [ ctrl+g nebo zaplneni okenka pro odeslani ]")
        x=4;y=4;h=18;w=int(70)
        rectangle(stdscr,x-1,y-1,y+h,x+w)
        editwin = curses.newwin(h,w,x,y)
        stdscr.refresh()
        box=Textbox(editwin)
        box.edit()
        text=box.gather()
        try:
          if (text!=""): 
            text.replace('\n','')
            text.replace('\r','')
            nyx_send_message(tui_klub_id,text[:-2]) 
            stdscr.addstr(4, 4, "Prispevek odeslan do klubu: " + sutf8(str(tui_klub_id)))
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
    elif k == ord("i"): # I - informace ze zahlavi klubu
      retVal=nyx_disc_header_desc(str(tui_klub_id))
      if (retVal):
        stdscr.addstr(0,0,sutf8(cleanHtml(nactiNazevKlubu(tui_klub_id))),curses.color_pair(0))
        stdscr.addstr(2,0,sutf8(cleanHtml(retVal[0])))
      else:
        stdscr.addstr(0,0,sutf8("Bez zahlavi"))
      stdscr.refresh()
      stdscr.getch()    
      stdscr.clear()      
    elif k == ord("k"): # K - klub
      try:
        stdscr.refresh()
        curses.cbreak()
        stdscr.addstr(1,3,"Vyber klub (cislo): [ ctrl+g pro odeslani ]")
        x=4;y=4;h=1;w=12
        rectangle(stdscr,x-1,y-1,h+x+1,w+y+1)
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
        klub_strana=1
        stdscr.refresh()
        stdscr.clear()
      except Exception:
        traceback.print_exc(file=sys.stdout)
        input("Zmackni Enter ...")
        print("Problem pri ziskani cisla klubu.")

    stdscr.refresh()
    stdscr.clear()
    cursor_x = max(0, cursor_x)
    cursor_x = min(width-1, cursor_x)

    cursor_y = max(0, cursor_y)
    cursor_y = min(height-1, cursor_y)

    # Declaration of strings
    title = "C O N Y X"[:width-1]
    subtitle = "CONSOLE NYX CLIENT"[:width-1]
    #keystr = "Posledni klavesa: {}".format(k)[:width-1] + " KLUB: " + str(tui_klub_id) + " str.: " + str(klub_strana)
    keystr = " KLUB ["+str(klub_strana)+"] : " + str(tui_klub_id)
    nazev_klubu = nactiNazevKlubu(tui_klub_id)[:width-1]
    #statusbarstr = "(q)uit |                          | (1) napoveda| Pos: {}, {}".format(cursor_x, cursor_y)
    #statusbarstr = "(q)uit | (s)ledovane (k)lub (c)ti (p)is (n)eprectene (r)eakci | (z)meny |"
    pre_sbar="(q)uit |"
    post_sbar="| (1) napoveda"
    fill_len=width-len(pre_sbar)-len(post_sbar)-1
    statusbarstr = pre_sbar+("_"*fill_len)+post_sbar
    credits = "MMXVIII-MMXX"
    if k == 0:
      credits = "MMXVIII-MMXX"
      keystr = u"Vítej zpět do klubu {}".format(str(tui_klub_id))

    # Centering calculations
    start_x_title=int((width//2)-(len(title)//2)-len(title)%2)
    start_x_subtitle=int((width//2)-(len(subtitle)//2)-len(subtitle)%2)
    start_x_keystr=int((width//2)-(len(keystr)//2)-len(keystr)%2)
    start_x_credits=int((width//2)-(len(credits)//2)-len(credits)%2)
    start_x_nazev_klubu=int((width//2)-(len(nazev_klubu)//2)-len(nazev_klubu)%2)
    start_y=int((height//2)-4)

    # Rendering some text
    #whstr = "Width: {}, Height: {}".format(width, height)
    #stdscr.addstr(0, 0, whstr, curses.color_pair(1))

    # Render status bar
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, sutf8(statusbarstr))
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    stdscr.addstr(start_y, start_x_title, sutf8(title))

    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    # Print rest of text
    stdscr.addstr(start_y+2,start_x_subtitle, sutf8(subtitle))
    #stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
    stdscr.addstr(start_y+4,start_x_keystr, sutf8(keystr))
    stdscr.addstr(start_y+6,start_x_nazev_klubu, sutf8(nazev_klubu))
    stdscr.addstr(start_y+8,start_x_credits, sutf8(credits))
    stdscr.move(cursor_y,cursor_x)

    # Refresh the screen
    stdscr.refresh()

    # Wait for next input
    k = stdscr.getch()

def tuiMainScreen():
  global tui_klub_id
  tui_klub_id=-1
  locale.setlocale(locale.LC_ALL,"")
  encoding = "utf-8"
  cols, rows = conyxDBQuery('select * from last where rowid = (select max(rowid) from last)')
  tui_klub_id = rows[0][0]
  curses.wrapper(draw_menu)

# DEBUG
#tuiMainScreen()
