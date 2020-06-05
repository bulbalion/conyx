# encoding=utf-8
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
# version 0.2.0
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
import sys, os, traceback
# reload(sys)
# sys.setdefaultencoding('utf8')
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import curses
import locale
import re
from conyxDBQuery import conyxDBQuery
from tuiWritePost import tuiWritePost
from conyxDBGetForumLast import conyxDBGetForumLast 

nocolors = {
  'r':"",
  0:"",
  1:"",
  2:"",
  3:"",
  4:"",
  5:"",
  6:"",
  7:"",
  8:"",
  9:"",
  10:"",
  11:"",
  12:"",
  13:"",
  14:"",
  15:"",
  16:""
}

colors = {
  'r':"\033[0m",
  0:"\033[0;30m",
  1:"\033[0;34m",
  2:"\033[0;32m",
  3:"\033[0;36m",
  4:"\033[0;31m",
  5:"\033[0;35m",
  6:"\033[0;33m",
  7:"\033[0;37m",
  8:"\033[1;30m",
  9:"\033[1;34m",
  10:"\033[1;32m",
  11:"\033[1;36m",
  12:"\033[1;31m",
  13:"\033[1;35m",
  14:"\033[1;33m",
  15:"\033[1;37m",
  16:"\033[40m"
}

def esc_length(s):
  #length_esc_exp = re.compile(r"""
  #  \x1b     # literal ESC
  #  \[       # literal [
  #  [;\d]*   # zero or more digits or semicolons
  #  [A-Za-z] # a letter
  #  """, re.VERBOSE).search
  esc_exp = "\x1b\[[;\d]*[A-Za-z]"
  esc_len=0
  for i in re.findall(esc_exp,s): esc_len+=(len(i))
  return(esc_len)

def strip_esc(s):
  strip_esc_exp = re.compile(r"""
    \x1b     # literal ESC
    \[       # literal [
    [;\d]*   # zero or more digits or semicolons
    [A-Za-z] # a letter
    """, re.VERBOSE).sub
  return(strip_esc_exp("", s))


def print_pallete():
 for i in colors.keys():
    print(str(colors[i]) + "| conyx | " + str(i).rjust(4,'0'))

def print_more(print_str,printed_lines,current_page):
  c = colors
  printed_chars=0
  ts = os.get_terminal_size()
  cols = ts.columns
  dlines=ts.lines-1
  printed_chars=0
  #print("|||"+print_str+"|||")
  #for i in (0,len(print_str),cols):
  while printed_chars < len(strip_esc(print_str)):
    #print(str(i)+"||"+str(len(print_str))+"||"+str(cols))
    if (printed_chars>len(strip_esc(print_str))):
      print(print_str[printed_chars:])
    else:
      print(print_str[printed_chars:printed_chars+cols])
    #vypoctu tisknuta pismena pro radkovani bez escape sekvenci
    printed_chars+=cols+esc_length(print_str[printed_chars:printed_chars+cols])
    printed_lines+=1
    if (printed_lines/dlines)>current_page:
      #delim_str="[ ENTER ] "+"-"*(cols-10)
      delim_str="-"*(cols-1)
      input(delim_str)
      current_page+=1
  return(printed_lines,current_page)

def br2nl(text):
  #brtext=text.replace('<br />','\n\r')
  brtext=text.replace('\n',' ')
  return(brtext)

def strip_empty_lines_from_end(text):
  lines = text.splitlines()
  #while lines and not lines[0].strip():
  #  lines.pop(0)
  while lines and not lines[-1].strip():
    lines.pop()
  return('\n'.join(lines))

def splitLine(line):
  spline=line.split('|') # SPLIT LINE
  return(spline)

def cleanHtml(text):
  #r_links = re.compile(r'href=[\'"]?([^\'" >]+)')
  #refs = re.findall(r_links,text)
  p_clean = re.compile('<.*?>')
  cleantext = re.sub(p_clean,'', text)
  #cleantext = text
  #if refs != []:
  #  cleantext=cleantext+'|R: '+', '.join(refs)
  #else:
  #  cleantext=text
  return(cleantext)

def tuiScrollContent(filename,lines):
  try:
    screen=curses.initscr()
    rows,columns=screen.getmaxyx()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    screen.keypad(1)
    screen.clear()
    screen.refresh()
    curses.start_color()
    #curses.init_pair(10,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(10,curses.COLOR_WHITE,curses.COLOR_BLACK)
    height,width=screen.getmaxyx()
    hiTe=curses.color_pair(10)|curses.A_BOLD
    miTe=curses.color_pair(10)
    loTe=curses.color_pair(10)|curses.A_DIM
    clean=[]
    for i in lines:
      #clean.append(cleanHtml(br2nl(i)))
      clean.append(br2nl(cleanHtml(i)))
    #clean=lines
    buffer=[]
    #print(clean)
    #buffer=clean
    for j in clean:
      #if len(j)>columns:
      #  for i in range(0,len(j),columns):
      #buffer.append(j[i:i+columns])
      #else:
      #  buffer.append(j)
      buffer.append(j)
    buffer=buffer[::-1] # REVERSE BUFFER
    c=""
    shift=0 # len(buffer)-rows+1
    klub_strana=1
    while c!=ord("q"):
      if c == curses.KEY_DOWN or c==ord("j"):
        if y+shift<len(buffer)-1: shift+=1 
        screen.clear()
      elif c == ord("p"):
        screen.clear()
        tui_klub_id=conyxDBGetForumLast()
        tuiWritePost(screen,width,height,tui_klub_id)
        return(0)
        #zobrazDiskuzi(str(tui_klub_id),screen,1)
      elif c==ord("h"):
        shift=0
      elif c == curses.KEY_UP or c==ord("k"):
        if shift>0: shift-=1
      elif c == curses.KEY_PPAGE or c==ord("u"):
        if shift-rows>0: 
          shift-=rows 
        else: 
          shift=0
      elif c == curses.KEY_NPAGE or c==ord("n"):
        if y+shift+rows<len(buffer)-1:
          shift+=rows 
      elif c == ord("o"): # O - cti od prispevku
        curses.endwin()
        screen.refresh()
        c = screen.getch()
        return(-1)
        #stdscr.clear()      

      screen.clear()
      try:
        scr_row=0
        add_lines=0
        for y in range(len(buffer)):
          buff_row=y+shift
          if (scr_row<rows-1):
            split_line=splitLine(buffer[buff_row])
            slno=0
            slprn=0
            slcnt=len(split_line)
            slend=0
            eol=0
            for sl in split_line:
              slend=slprn+len(sl)
              if slno==0: 
                sl=sl+'> '
                screen.addstr(scr_row,0,sl,loTe)
              elif slno==slcnt-1:
                screen.addstr(scr_row,columns-len(sl),sl,loTe)
              elif(slno==1):
                sl=sl.replace('\n',' ').replace('\r',' ')
                if (slend>=columns): # LINE LONGER THAN WIDTH
                  screen.addstr(scr_row,slprn,sl[:columns-slprn],miTe)
                  for x in range(columns-slprn,len(sl),columns-1):
                    if (scr_row==rows-2): break
                    scr_row+=1; add_lines+=1
                    screen.addstr(scr_row,0,sl[x:x+columns],miTe)
                else:
                  screen.addstr(scr_row,slprn,sl,miTe)
              slprn+=len(sl)
              slno+=1
            scr_row+=1; add_lines+=1
          else:
            break
        help_text_read="%s -=[ Klavesy: j,k,l,h,u,n,q ]=-" % str(shift)
        screen.addstr(rows-1,columns-len(help_text_read)-1,help_text_read,loTe)
      except Exception as e:
        try:
          screen.addstr(rows-1,0,"ERR: " + "BR: " + str(y) + " SCR_ROW: " + str(scr_row) + " e: " + str(e) + " slno " + str(slno) + " slprn " + str(slprn) + " cp " + str(scr_row))
        except:
          screen.addstr(rows-1,0,"ERROR PRINTING ERROR")
          
        #traceback.print_exc(file=sys.stdout)
        #screen.getch()

      screen.refresh()
      c = screen.getch()
  finally:
    curses.endwin()

def tuiBuffer(name,buffer):
  locale.setlocale(locale.LC_ALL, '')
  tuiScrollContent(name,buffer)
