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

import curses
import locale
import sys

def stripDia(in_str):
  return(in_str.encode('ascii','ignore'))

def tuiScrollContent(filename,filecontent,encoding="utf-8",cursor=0,fromBottom=0):
  try:
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)
    rows, columns = stdscr.getmaxyx()
    stdscr.border()
    bottom_menu = "CONYX " + filename # u"(n) Next line | (p) Previous line | (n) Next page | (p) Previous page | (q) Quit".encode(encoding).center(columns - 4)
    stdscr.addstr(rows - 1, 2, bottom_menu, curses.A_REVERSE)
    out = stdscr.subwin(rows - 2, columns - 2, 1, 1)
    out_rows, out_columns = out.getmaxyx()
    out_rows -= 1
    lines = map(lambda x: x + " " * (out_columns - len(x)), reduce(lambda x, y: x + y, [[x[i:i+out_columns] for i in xrange(0, len(x), out_columns)] for x in stripDia(filecontent).expandtabs(4).splitlines()]))
    stdscr.refresh()
    if fromBottom==1:
      line = len(lines) - out_rows
    else:
      line = 0
    while 1:
      top_menu = (u"Radek %d az %d z %d z %s" % (line + 1, min(len(lines), line + out_rows), len(lines), filename)).encode(encoding).center(columns - 4) 
      stdscr.addstr(0, 2, top_menu, curses.A_REVERSE)
      
      out.addstr(0, 0, "".join(lines[line:line+out_rows]))
      stdscr.refresh()
      out.refresh()
      c = stdscr.getch()
      if c == ord("q"):
        stdscr.clear()
        stdscr.refresh()
        break
      elif c == curses.KEY_DOWN:
        if len(lines) - line > out_rows:
          line += 1
      elif c == curses.KEY_UP:
        if line > 0:
          line -= 1
      elif c == curses.KEY_RIGHT:
        if len(lines) - line >= 2 * out_rows:
          line += out_rows
      elif c == curses.KEY_LEFT:
        if line >= out_rows:
          line -= out_rows
  finally:
    #curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.curs_set(1)
    curses.endwin()

def tuiBuffer(name,buffer,fromBottom=0):
  encoding = locale.getpreferredencoding()
  #print(encoding)
  #encoding = "UTF-8"
  locale.setlocale(locale.LC_ALL, '')
  tuiScrollContent(name,buffer, encoding,0,fromBottom)

