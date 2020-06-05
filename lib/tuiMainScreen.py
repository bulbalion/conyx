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
# version 0.2.4
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
#sys.setdefaultencoding('utf8') # v0.2.2
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import curses, locale
from curses.textpad import Textbox, rectangle
from conyxDBQuery import conyxDBQuery
from tuiBuffer import *
from tuiFile import tuiFile
from tuiConfig import tuiConfig
from nyxOp import *
from conyxDBLast import conyxDBLast
from tuiMainMenu import tuiMainMenu
from conyxOps import *
from ugetch import ugetch
from inputBox import inputBox
from tuiMail import tuiMail
from fBrowser import fBrowser
from ls import ls
from tuiConfig import getConfig
from hlp_moon_phase import moon_phase
from hlp_sunset import sunrise, sunset
from hlp_nday_qry import hlp_nday_qry
from hlp_zodiac_qry import zodiac
from hlp_day import hlp_day
from tuiWritePost import tuiWritePost
from conyxDBSetForumLast import conyxDBSetForumLast
from sutf8 import sutf8
from nyx_send_message import nyx_send_message

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

def getParentalLockStatus():
  cols,rows=conyxDBQuery('select value from config where key = "rodicovsky_zamek"')
  rodzam=int(rows[0][0])
  return(rodzam)

def getParentalLockClub():
  cols,rows=conyxDBQuery('select value from config where key = "rodicovsky_zamek_klub"')
  rodzamkl=int(rows[0][0])
  return(rodzamkl)

def getLastVisitedClub():
  klub_id = 1
  cols, rows = conyxDBQuery('select * from last where rowid = (select max(rowid) from last)')
  if (rows):
    klub_id = rows[0][0]
  return(klub_id)

def draw_menu(stdscr):
  global tui_klub_id
  k = 0
  cursor_x = 0
  cursor_y = 0

  encoding = locale.getpreferredencoding()
  locale.setlocale(locale.LC_ALL, '')

  stdscr = curses.initscr()

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

    # RODICOVSKY ZAMEK
    rodzam=getParentalLockStatus()
    #print(str(rodzam))
    if (rodzam==1):
      rodzamkl=getParentalLockClub()
      conyxDBLast(rodzamkl)
      tui_klub_id=rodzamkl

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    tui_klub_id=getLastVisitedClub()
    club_changed=0

    if rodzam == 1:
      if k == ord("0"): # k - konfigurace
        tuiConfig()
      elif k == ord("c") or k == ord("\n"): # C - cti prispevky 
        zobrazDiskuzi(str(tui_klub_id),stdscr,1)
        stdscr.clear()      
      elif k == ord("p"): # P - pis
        try:
          stdscr.refresh()
          curses.cbreak()
          stdscr.addstr(0,3,"Tvuj novy prispevek: [ ctrl+g nebo zaplneni okenka pro odeslani ]")
          height, width = stdscr.getmaxyx()
          x=2;y=2;h=height-y;w=width-x;
          rectangle(stdscr,x-1,y-1,h+1,w)
          editwin = curses.newwin(h-1,w-2,x,y)
          stdscr.refresh()
          #box=Textbox(editwin)
          box=inputBox(editwin)
          box.edit()
          text=box.gather()
          try:
            if (text!=""): 
              text=text[:-1]
              curses.nocbreak()
              orig_text=text
              tmp=orig_text.strip().split('\n')
              text=""
              for i in tmp:
                text+=i
                if (len(i)!=width-4):
                  text+='\n'
              nazev_klubu = nactiNazevKlubu(tui_klub_id)[:width-1]
              if (nyx_send_message(tui_klub_id,text)==0):
                stdscr.addstr(0, 0, " "*width)
                stdscr.addstr(0, 0, "*** Prispevek odeslan do klubu: " + sutf8(str(tui_klub_id)) + " " + nazev_klubu)
              else:
                stdscr.addstr(0, 0, " "*width)
                stdscr.addstr(0, 0, "!   Chyba pri odesilani prispevku do klubu" + nazev_klubu)
              #stdscr.getch()
              x = ugetch(stdscr)
              curses.cbreak()
          except Exception:
            stdscr.addstr(0, 0, "Nepodarilo se odeslat prispevek")
            #traceback.print_exc(file=sys.stdout)
            #stdscr.getch()
            x = ugetch(stdscr)
          stdscr.refresh()
          stdscr.clear()
        except Exception:
          traceback.print_exc(file=sys.stdout)
          input("Zmackni Enter ...")
          print("Problem pri ziskani cisla klubu.")
    else:
      if k == curses.KEY_DOWN:
        cursor_y = cursor_y + 1
      elif k == ord("0"): # k - konfigurace
        tuiConfig()
      elif k == ord("1"): # 1 - napoveda
        tuiFile("napoveda.txt")
      elif k == ord("m"): # m - ozna(m)eni
        curses.endwin()
        nyx_feed_notices()
        stdscr.clear()      
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
          conyxDBLast(tui_klub_id)
          club_changed=1
        klub_strana=1
        stdscr.clear()      
      elif k == ord("r"): # R - kluby s reakci
        retVal=tuiMainMenu(2)
        if (retVal):
          tui_klub_id=retVal
          conyxDBLast(tui_klub_id)
          club_changed=1
        klub_strana=1
        stdscr.clear()      
      elif k == ord("h"): # H - historie
        retVal=tuiMainMenu(4)
        #retVal=nyx_bookmarks_history()
        if (retVal):
          tui_klub_id=retVal
          conyxDBLast(tui_klub_id)
          club_changed=1
        klub_strana=1
        stdscr.clear()      
      elif k == ord("s"): # S - sledovane
        retVal=tuiMainMenu(0)
        if (retVal):
          tui_klub_id=retVal
          conyxDBLast(tui_klub_id)
          club_changed=1
        stdscr.clear()      
      elif k == ord("c") or k == ord("\n"): # C - cti prispevky 
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
        stdscr.addstr(0,1,"Hledej na celem Nyxu:")
        footer="-=[ klavesy: CTRL+G odeslat, CTRL+X zrusit ]=-" 
        if (len(footer)>=height-1):
          footer="-=[ ^G, ^X ]=-"
        stdscr.addstr(height-1,0,footer)
        x=1;y=1;h=height-3;w=width-3
        rectangle(stdscr,y,x,y+h,x+w)
        editwin = curses.newwin(h-1,w-1,y+1,x+1)
        stdscr.refresh()
        #box=Textbox(editwin)
        box=inputBox(editwin)
        box.edit()
        text=box.gather()
        if text != "":
          #print("TEXT: "+text)
          #stdscr.getch()
          rx,res=nyx_search_writeups(None,text,None)
          buffer=[]
          for i in res["data"]:
            buffer.append(i["klub_jmeno"]+"|"+i["nick"]+"|"+cleanhtml(i["content"]))
          tuiBuffer("Vysledek hledani",buffer)
        else:
          stdscr.clear()     
      elif k == ord("v"): # V - vyhledat klicove slovo
        stdscr.addstr(0,1,"Hledej v diskuzi:")
        footer="-=[ klavesy: CTRL+G odeslat, CTRL+X zrusit ]=-" 
        if (len(footer)>=height-1):
          footer="-=[ ^G, ^X ]=-"
        stdscr.addstr(height-1,0,footer)
        x=1;y=1;h=height-3;w=width-3
        rectangle(stdscr,y,x,y+h,x+w)
        editwin = curses.newwin(h-1,w-1,y+1,x+1)
        stdscr.refresh()
        box=inputBox(editwin)
        box.edit()
        text=box.gather()
        if text is not None and text != "":
          ret=zobrazDiskuzi(str(tui_klub_id),stdscr,1,None,None,None,text)
        stdscr.clear()     
      elif k == ord("l"): # B - vyhledat prispevky uzivatele
        stdscr.addstr(0,1,"Hledej prispevky uzivatele:")
        footer="-=[ klavesy: CTRL+G odeslat, CTRL+X zrusit ]=-" 
        if (len(footer)>=height-1):
          footer="-=[ ^G, ^X ]=-"
        stdscr.addstr(height-1,0,footer)
        x=1;y=1;h=height-3;w=width-3
        rectangle(stdscr,y,x,y+h,x+w)
        editwin = curses.newwin(h-1,w-1,y+1,x+1)
        stdscr.refresh()
        #box=Textbox(editwin)
        box=inputBox(editwin)
        box.edit()
        text=box.gather()
        if text != "":
          ret=zobrazDiskuzi(str(tui_klub_id),stdscr,1,None,None,text)
        stdscr.clear()     
      elif k == ord("e"): # U - cti nasledujici od nejnovejsiho prispevku
        res=conyxDBQuery('select max(id_prispevek) prid from prispevek_cache')
        ret=zobrazDiskuzi(str(tui_klub_id),stdscr,1,res[1][0][0],"newer")
        if (klub_strana>1):
          klub_strana-=1      
        stdscr.clear() 
      elif k == ord("p"): # P - pis
        tuiWritePost(stdscr,width,height,tui_klub_id)
      elif k == ord("i"): # I - informace ze zahlavi klubu
        retVal=nyx_disc_header_desc(str(tui_klub_id))
        if (retVal):
          linelen=width-1
          stdscr.addstr(0,0,sutf8(cleanHtml(nactiNazevKlubu(tui_klub_id)))[:linelen],curses.color_pair(1))
          lineno=0
          for i in range(0,len(retVal[0]),linelen):
            stdscr.addstr(lineno+1,0,sutf8(cleanHtml(retVal[0]))[i:(i+linelen)])
            lineno+=1
            if lineno>height-2:
              break
            stdscr.addstr(height-1,0,"-=[ q - zpatky ]=-")
        else:
          stdscr.addstr(0,0,sutf8("Bez zahlavi"))
        stdscr.refresh()
        #stdscr.getch()    
        ugetch(stdscr)
        stdscr.clear()      
      elif k == ord("f"): # F - odesli soubor
        dir=str(getConfig('soubory')[0][0])
        strings = ls(dir,'') 
        sel=fBrowser(strings,0,0)
        if (not (sel is None) ):
          stdscr.refresh()
          curses.cbreak()
          header="Text k souboru:"
          height, width = stdscr.getmaxyx()
          footer="-=[ klavesy: CTRL+G odeslat, CTRL+X zrusit ]=-" 
          if len(footer)>=width-1:
            footer="-=[ ^G, ^X, ALT+1 ]=-" 
          stdscr.addstr(0,2,header)
          stdscr.addstr(height-1,0,footer)
          x=2;y=2;h=height-y;w=width-x;
          rectangle(stdscr,y-1,x-1,h,w)
          editwin = curses.newwin(h-1-1,w-2,y,x)
          stdscr.refresh()
          box=inputBox(editwin)
          text=box.edit()
          stdscr.clear()
          nazev_klubu = nactiNazevKlubu(tui_klub_id)[:width-1]
          if (nyx_send_message(tui_klub_id,text,sel)==0):
            stdscr.addstr(0, 0, " "*width)
            stdscr.addstr(0, 0, "*** Prispevek se souborem odeslan do klubu: " + sutf8(str(tui_klub_id)) + " " + nazev_klubu)
          else:
            stdscr.addstr(0, 0, " "*width)
            stdscr.addstr(0, 0, "!   Chyba pri odesilani prispevku se souborem do klubu " + nazev_klubu)
          stdscr.refresh()
          x = ugetch(stdscr)
      elif k == ord("d"): # D - dopisy
        tuiMail()
      elif k == ord("k"): # K - klub
        try:
          stdscr.refresh()
          curses.cbreak()
          stdscr.addstr(1,3,"Vyber klub (cislo):")
          stdscr.addstr(height-1,0,"-=[ klavesy: CTRL+G, CTRL+X ]=-")
          x=4;y=4;h=1;w=12
          rectangle(stdscr,x-1,y-1,h+x+1,w+y+1)
          editwin = curses.newwin(h,w,x,y)
          stdscr.refresh()
          #box=Textbox(editwin)
          box=inputBox(editwin)
          box.edit()
          text=box.gather()
          try:
            if (text!=""): 
              tui_klub_id=int(text)
              conyxDBLast(tui_klub_id)
              conyxDBSetForumLast(tui_klub_id)
          except Exception:
            stdscr.addstr(0, 0, "Neplatny vyber klubu")
            traceback.print_exc(file=sys.stdout)
            #stdscr.getch()    
            ugetch(stdscr)
          klub_strana=1
          stdscr.refresh()
          stdscr.clear()
        except Exception:
          traceback.print_exc(file=sys.stdout)
          input("Zmackni Enter ...")
          print("Problem pri ziskani cisla klubu.")

    rodzam=getParentalLockStatus()

    stdscr.refresh()
    stdscr.clear()
    cursor_x = max(0, cursor_x)
    cursor_x = min(width-1, cursor_x)

    cursor_y = max(0, cursor_y)
    cursor_y = min(height-1, cursor_y)

    # Declaration of strings

    start_y=int((height//2)-8)

    if (rodzam==1):
      title = "klávesa c - čti"
      start_x_title=int((width//2)-(len(title)//2)-len(title)%2)
      stdscr.addstr(start_y, start_x_title, sutf8(title))
      subtitle = "klávesa p - piš"
      stdscr.addstr(start_y+2, start_x_title, sutf8(subtitle))
    else:
      title = "C O N Y X"[:width-1]
      subtitle = "CONSOLE NYX CLIENT"[:width-1]
      #keystr = "Posledni klavesa: {}".format(k)[:width-1] + " KLUB: " + str(tui_klub_id) + " str.: " + str(klub_strana)
      keystr = " KLUB ["+str(klub_strana)+"] : " + str(tui_klub_id)
      nazev_klubu = nactiNazevKlubu(tui_klub_id)[:width-1]
      pre_sbar="(q)uit |"
      post_sbar="| (1) napoveda"
      fill_len=width-1-len(pre_sbar)-len(post_sbar)
      statusbarstr = pre_sbar+("_"*fill_len)+post_sbar
      sun = "Slunce: " + str(sunrise().strftime("%H.%M")) + "-" + str(sunset().strftime("%H.%M"))
      moon = "Měsíc: " + str(moon_phase())
      zodnow = datetime.datetime.now().strftime("%Y-%m-%d")
      name_zodiac = "Zvěrokruh: " + str(zodiac(zodnow))
      today = datetime.datetime.now().strftime("%d.%m.")
      day = hlp_day(datetime.datetime.now().strftime("%w"))
      name_date = datetime.datetime.now().strftime("%m-%d")
      name_day_name= hlp_nday_qry("select name from jmeniny where date = '%s'" % name_date)
      name_day = "Dnes je " + day + " " + today + " a svátek má " +name_day_name[0][0]
      credits = "MMXVIII-MMXX"
      if k == 0:
        credits = "MMXVIII-MMXX"
        keystr = " KLUB ["+str(klub_strana)+"] : " + str(tui_klub_id)
      # Centering calculations
      start_x_title=int((width//2)-(len(title)//2)-len(title)%2)
      start_x_subtitle=int((width//2)-(len(subtitle)//2)-len(subtitle)%2)
      start_x_keystr=int((width//2)-(len(keystr)//2)-len(keystr)%2)
      start_x_credits=int((width//2)-(len(credits)//2)-len(credits)%2)
      start_x_nazev_klubu=int((width//2)-(len(nazev_klubu)//2)-len(nazev_klubu)%2)
      start_x_sun=int((width//2)-(len(sun)//2)-len(sun)%2)
      start_x_moon=int((width//2)-(len(moon)//2)-len(moon)%2)
      start_x_zodiac=int((width//2)-(len(name_zodiac)//2)-len(name_zodiac)%2)
      start_x_name_day=int((width//2)-(len(name_day)//2)-len(name_day)%2)

      # Render status bar
      stdscr.attron(curses.color_pair(3))
      stdscr.addstr(height-1, 0, sutf8(statusbarstr))
      stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
      stdscr.attroff(curses.color_pair(3))

      # Turning on attributes for title
      stdscr.attron(curses.color_pair(2))
      stdscr.attron(curses.A_BOLD)

      # Rendering title
      #stdscr.addstr(start_y, start_x_title, sutf8(title))


      # Print rest of text
      stdscr.addstr(start_y,start_x_title, sutf8(title), )

      # Turning off attributes for the rest
      stdscr.attroff(curses.color_pair(2))
      stdscr.attroff(curses.A_BOLD)

      stdscr.addstr(start_y+2,start_x_keystr, sutf8(keystr))
      stdscr.addstr(start_y+4,start_x_nazev_klubu, sutf8(nazev_klubu))
      stdscr.addstr(start_y+6,start_x_sun, sutf8(sun))
      stdscr.addstr(start_y+8,start_x_moon, sutf8(moon))
      stdscr.addstr(start_y+10,start_x_name_day, sutf8(name_day))
      stdscr.addstr(start_y+12,start_x_zodiac, sutf8(name_zodiac))
      stdscr.move(cursor_y,cursor_x)

    # Refresh the screen
    stdscr.refresh()

    # Wait for next input
    #k = stdscr.getch()
    k = ugetch(stdscr)

def tuiMainScreen():
  global tui_klub_id
  tui_klub_id=-1
  locale.setlocale(locale.LC_ALL,"")
  encoding = "utf-8"
  tui_klub_id=getLastVisitedClub()
  curses.wrapper(draw_menu)

# DEBUG
#tuiMainScreen()
