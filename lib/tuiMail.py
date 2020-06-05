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

import curses
from math import *

actual_char='>'
  
import sys, os, traceback
import locale
import sys
import re
import time

from curses.textpad import Textbox, rectangle

if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
from conyxDBQuery import conyxDBQuery
from nyxMail import nyx_list_mail, nyx_send_mail, nyx_filter_mail
from tuiBuffer import cleanHtml, br2nl
from sutf8 import sutf8 
from inputBox import inputBox
from ugetch import ugetch

def mailPrepareText(text,width,height):
  orig_text=text
  tmp=orig_text.strip().split('\n')
  text=""
  # b lib/tuiMai.py:50
  for i in tmp:
    text+=i
    if (len(i)!=width-4):
      text+='\n'
  return(text)

def getCurrentMsgId(strings,position):
  msg_id=strings[position-1].split('|')[0]
  return(msg_id)

def displayMail(screen,strings,position,width,height):
   screen.erase()
   msg_id=strings[position-1].split('|')[0]
   msg_content=getMailContent(msg_id)
   msg_date=time.strftime("%d.%m.%Y %H:%M",time.localtime(int(msg_content[0][2]))) 
   screen.addstr(0,0,"-|"+("-"*(width-5))+"|-")
   msg_str_dir="Od: "
   msg_str_act=  "Prijato:  "
   if (msg_content[0][3]=='to'):
     msg_str_dir="Komu: "
     msg_str_act="Odeslano: "
   screen.addstr(1,2,msg_str_dir+str(msg_content[0][0]) + "")
   screen.addstr(1,width-29,msg_str_act+str(msg_date)+ "")
   screen.addstr(2,0,"-|"+("-"*(width-5))+"|-")
   #screen.addstr(height-1,1,"-|"+("-"*(width-14))+" "+(str(position)+"/"+str(len(strings))).ljust(6)+" |-")
   footer_help="| o - odpovez h,l - pohyb |"
   footer="-"+footer_help+("-"*(width-len(footer_help)-15))+"| "+(str(position)+"/"+str(len(strings))).ljust(6)+" |-"
   screen.addstr(height-1,1,footer)
   try:
     screen.addstr(4,0,br2nl(msg_content[0][1])+ "")
   except Exception as e:
     screen.addstr(height-1,4,'Nedari se mi korektne zobrazit zpravu')

def getMailContent(msg_id):
  buffer=[]
  cols, rows = conyxDBQuery("select other_nick, content, time, direction from mail where id = %s" % (msg_id))
  for i in rows:
    buffer.append((str(i[0]),str(i[1]),str(i[2]),str(i[3])))
  return (buffer)

def getMail():
  buffer=[]
  cols, rows = conyxDBQuery("""select id, direction, other_nick, time from mail""")
  for i in rows:
    msg_date=time.strftime("%d.%m.%Y %H:%M", time.localtime(int(i[3]))) 
    msg_dir=  'komu'
    if (i[1]=='from'):
      msg_dir='od  '
    buffer.append(str(i[0])+'|'+msg_dir+'|'+str(i[2][:14]).ljust(14)+'|'+msg_date)
  return (buffer)

def tuiMail():
  screen = curses.initscr()
  height,width=screen.getmaxyx()

  msgDisplayed=0

  tmp=[] 
  strings=[] 
  nyx_list_mail()
  tmp=getMail()
  row_num = len(strings)
  strings=tmp
  curses.noecho()
  curses.cbreak()
  curses.start_color()
  screen.keypad(1)
  curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_MAGENTA)
  highlightText=curses.color_pair(1)
  normalText=curses.A_NORMAL
  max_row=height-2
  box=curses.newwin(max_row+2,width,0,0)
 
  pages=int(ceil(row_num/max_row))
  last_pos=1
  last_page=1
  position=last_pos 
  page=last_page
  for i in range(1,len(strings)):
    if (i+(max_row*(page-1))==position+(max_row*(page-1))):
      box.addstr(i-(max_row*(page-1)),0,actual_char+" "+cleanHtml(sutf8(strings[i-1])), highlightText)
    else:
      box.addstr(i-(max_row*(page-1)),0,"  "+cleanHtml(sutf8(strings[i-1])),normalText)
    if i == max_row:
      break
  mm_footer_help="-=[ pohyb: j,k,ENTER ]=-" 
  box.addstr(height-1,0,mm_footer_help)
  screen.refresh()
  box.refresh()
  tuiMailDisplayed=0
  x = screen.getch()
  while x != 113: # dokud neni stisknuta klavesa 'q'
    if (tuiMailDisplayed==0):
      if x==curses.KEY_DOWN or x==ord('j'):
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
      elif x == ord("f"):
        screen.clear() 
        screen.refresh()
        curses.cbreak()
        screen.addstr(1,3,"Vyhledat dopisy od: [ ctrl+g pro odeslani ]")
        x=4;y=4;h=1;w=25
        rectangle(screen,x-1,y-1,h+x+1,w+y+1)
        editwin = curses.newwin(h,w,x,y)
        screen.refresh()
        searchBox=inputBox(editwin)
        searchBox.edit()
        text=searchBox.gather()
        if (text!=""): 
          nyx_filter_mail(text,"")
          tmp=getMail()
          row_num = len(strings)
          strings=tmp
      elif x == curses.KEY_UP or x == ord('k'):
        if page == 1:
            if position > 1:
              position = position - 1
        else:
            if position > ( 1 + ( max_row * ( page - 1 ) ) ):
              position = position - 1
            else:
              page = page - 1
              position = max_row + ( max_row * ( page - 1 ) )
      elif x == curses.KEY_LEFT or x == ord('h'):
        if page > 1:
           page=page-1
           position=1+(max_row*(page-1))
      elif x == curses.KEY_RIGHT or x == ord('l'):
        if page < pages:
           page = page + 1
           position = ( 1 + ( max_row * ( page - 1 ) ) )
      elif x == ord( "\n" ) and position != 0:
        displayMail(screen,strings,position,width,height)
        tuiMailDisplayed=1
 
    elif tuiMailDisplayed==1:
      if x==ord("q"):
        tuiMailDisplayed=0
      elif x in (curses.KEY_LEFT,ord('h')):
        if position<len(strings): position+=1
        displayMail(screen,strings,position,width,height)
      elif x in (curses.KEY_RIGHT,ord('l')):
        if position>1: position-=1
        displayMail(screen,strings,position,width,height)
      elif x == ord("o"): # O - odpovez
        screen.clear()
        screen.refresh()
        curses.cbreak()
        msg_id=getCurrentMsgId(strings,position)
        msg_content=getMailContent(msg_id)
        msg_recepient=msg_content[0][0]
        screen.addstr(0,2,"Zadej zpravu pro " + msg_recepient + ":")
        #footer="pos " + str(position) + " page " + str(page) + " mr " + str(max_row) + " row_num " + str(row_num) + " | -=[ ctlr+G - posli, ctrl+X - zrus ]=-"
        footer="-=[ ctlr+G - posli, ctrl+X - zrus ]=-"
        screen.addstr(height-1,0,footer)
        height, width = screen.getmaxyx()
        x=2;y=2;h=height-y;w=width-x;
        rectangle(screen,y-1,x-1,h,w)
        editwin = curses.newwin(h-2,w-2,y,x)
        screen.refresh()
        mailBox=inputBox(editwin)
        text=mailBox.edit()
        curses.nocbreak()
        if (text!=""): 
          #text=cleanHtml(text)
          text=mailPrepareText(text,width,height)
          if (nyx_send_mail(msg_recepient,text)==0):
            screen.addstr(0, 0, " "*width)
            screen.addstr(0, 0, "*** Dopis pro "+msg_recepient+" odeslan.")
          else:
            screen.addstr(0, 0, " "*width)
            screen.addstr(0, 0, "!   Chyba pri odesilani dopisu")
          x = ugetch(screen)
        else:
          screen.addstr(0, 0, " "*width)
          screen.addstr(0, 2, "Zprava zrusena, stiskni ENTER ...")
          x = ugetch(screen)
        curses.cbreak()
        tuiMailDisplayed=0
        nyx_list_mail()
        tmp=getMail()
        row_num = len(strings)
        strings=tmp
 
    if tuiMailDisplayed==0:
      box.erase()
      for i in range(1,len(strings)):
        if (i+(max_row*(page-1))==position+(max_row*(page-1))):
          box.addstr(i-(max_row*(page-1)),0,actual_char+" "+cleanHtml(sutf8(strings[i-1])), highlightText)
        else:
          box.addstr(i-(max_row*(page-1)),0,"  "+cleanHtml(sutf8(strings[i-1])),normalText)
        if i == max_row:
          break
      box.addstr(height-1,0,mm_footer_help)

    screen.refresh()
    box.refresh()
    x = screen.getch()
  
  curses.endwin()

