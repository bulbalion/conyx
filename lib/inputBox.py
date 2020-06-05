#-*- coding: utf-8 -*-
#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Operations Library
#
# version 0.2.3
#
# You can do whatever You want with Conyx.
# But I don't take reponsbility nor even
# implied responsibility for the harm,
# damage, loss or anything negative
# You cause using Conyx.
#
#"""Simple textbox editing widget with Emacs-like keybindings."""

import sys, os, traceback
import curses
import curses.ascii
from ugetch import ugetch
from hlp_ytb_search import hlp_ytb_dialog
import re

def strip_empty_lines_from_end(text):
  lines = text.splitlines()
  #while lines and not lines[0].strip():
  #  lines.pop(0)
  while lines and not lines[-1].strip():
    lines.pop()
  return('\n'.join(lines))

  

def rectangle(win, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    win.vline(uly+1, ulx, curses.ACS_VLINE, lry - uly - 1)
    win.hline(uly, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.hline(lry, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.vline(uly+1, lrx, curses.ACS_VLINE, lry - uly - 1)
    win.addch(uly, ulx, curses.ACS_ULCORNER)
    win.addch(uly, lrx, curses.ACS_URCORNER)
    win.addch(lry, lrx, curses.ACS_LRCORNER)
    win.addch(lry, ulx, curses.ACS_LLCORNER)


class inputBox:
    """Editing widget using the interior of a window object.
     Supports the following Emacs-like key bindings:

    Ctrl-A      Go to left edge of window.
    Ctrl-B      Cursor left, wrapping to previous line if appropriate.
    Ctrl-D      Delete character under cursor.
    Ctrl-E      Go to right edge (stripspaces off) or end of line (stripspaces on).
    Ctrl-F      Cursor right, wrapping to next line when appropriate.
    Ctrl-G      Terminate, returning the window contents.
    Ctrl-H      Delete character backward.
    Ctrl-J      Terminate if the window is 1 line, otherwise insert newline.
    Ctrl-K      If line is blank, delete it, otherwise clear to end of line.
    Ctrl-L      Refresh screen.
    Ctrl-N      Cursor down; move down one line.
    Ctrl-O      Insert a blank line at cursor location.
    Ctrl-P      Cursor up; move up one line.

    Move operations do nothing if the cursor is at an edge where the movement
    is not possible.  The following synonyms are supported where possible:

    KEY_LEFT = Ctrl-B, KEY_RIGHT = Ctrl-F, KEY_UP = Ctrl-P, KEY_DOWN = Ctrl-N
    KEY_BACKSPACE = Ctrl-h
    """
    def __init__(self, win, insert_mode=False):
        self.win = win
        self.insert_mode = insert_mode
        self._update_max_yx()
        self.stripspaces = 1
        self.lastcmd = None
        self.content = u''
        self.altModif = 0
        win.keypad(1)
        self.helpTextSmall="""Klavesy:
^A  | ^B | ^G  | ^H 
^L  | ^N | ^O  | ^P
^F  | ^E | ^D  | ^J
^K  | ^X | ALT-Y

left  ^B | right ^F
up    ^P | down  ^N
bkc   ^h |
"""
        self.helpText="""
Ctrl-A  do vlevo nahoru     | Ctrl-B  posun kurzor vlevo
Ctrl-G  odesli              | Ctrl-H  smaz predchozi pismeno
Ctrl-L  obnov obrazovku     | Ctrl-N  kurzor o radku dolu
Ctrl-O  vloz prazdnou radku | Ctrl-P  kurzor o radku nahoru
Ctrl-F  kurzor doprava
Ctrl-E  posun na pravy okraji nebo na konec radku
Ctrl-D  smaz pismeno pod kurzorem  
Ctrl-J  odesli, pokud je jeden radek nebo vloz novy
Ctrl-K  smaz prazdnou radku, jinak smaz do konce radku
Ctrl-X  zrusit psani
ALT-Y   YTB Helper

KEY_LEFT = Ctrl-B KEY_RIGHT = Ctrl-F
KEY_UP = Ctrl-P KEY_DOWN = Ctrl-N
KEY_BACKSPACE = Ctrl-h

"""
    def _update_max_yx(self):
        maxy, maxx = self.win.getmaxyx()
        self.maxy = maxy - 1
        self.maxx = maxx - 1

    def _end_of_line(self, y):
        """Go to the location of the first blank on the given line,
        returning the index of the last non-blank character."""
        self._update_max_yx()
        last = self.maxx
        while True:
            if curses.ascii.ascii(self.win.inch(y, last)) != curses.ascii.SP:
                last = min(self.maxx, last+1)
                break
            elif last == 0:
                break
            last = last - 1
        return last

    def _insert_printable_char(self, ch):
        self._update_max_yx()
        (y, x) = self.win.getyx()
        backyx = None
        while y < self.maxy or x < self.maxx:
            if self.insert_mode:
                oldch = self.win.inch()
            # The try-catch ignores the error we trigger from some curses
            # versions by trying to write into the lowest-rightmost spot
            # in the window.
            try:
                #self.win.addstr(0,0,u'(ch)))
                self.win.addstr(str(chr(ch)))
            except curses.error:
                pass
            if not self.insert_mode or not curses.ascii.isprint(oldch):
                break
            ch = oldch
            (y, x) = self.win.getyx()
            # Remember where to put the cursor back since we are in insert_mode
            if backyx is None:
                backyx = y, x

        if backyx is not None:
            self.win.move(*backyx)

    def help(self):
      tmp=self.gather()
      self.win.move(0, 0)
      if self.maxx<=50:
        self.win.addstr(0,0,self.helpTextSmall)
      else:
        self.win.addstr(0,0,self.helpText)
      self._update_max_yx()
      rows=self.maxy
      ch = ugetch(self.win)
      self.win.move(0, 0)
      self.win.clear()
      self.win.addstr(0,0,tmp)
      self._update_max_yx()
      self.win.refresh()
    
    def helpers(self):
      tmp=self.gather()
      self.win.clear()
      self.win.addstr(0,0,tmp)
      self._update_max_yx()
      self.win.refresh()
    
    def do_command(self, ch):
        "Process a single editing command."
        self._update_max_yx()
        (y, x) = self.win.getyx()
        self.lastcmd = ch
        #if curses.ascii.isprint(ch)):
        isChar = re.search("[0-9a-zA-ZÁ-Ž]",str(chr(ch)))
        #self.win.addstr(0,0,"Key: "+ str(ord(chr(ch))) + " |||")
        if ((isChar or ch >= 32 <= 126) and ch != 127 and ch != 263 and str(chr(ch)) not in ("ă","Ă","ă","ő","Ą","Ć","Ũ","ą")):
          if (y < self.maxy or x < self.maxx) and (ch != curses.ascii.BEL):
            self._insert_printable_char(ch)
        elif ch == 24:
            return (0)
        elif ch == curses.ascii.SOH:                           # ^a
            self.win.move(y, 0)
        elif ch in (curses.ascii.STX,curses.KEY_LEFT, curses.ascii.BS,curses.KEY_BACKSPACE,263,127): # 263 backspace
            if x > 0:
                self.win.move(y, x-1)
            elif y == 0:
                pass
            elif self.stripspaces:
                self.win.move(y-1, self._end_of_line(y-1))
            else:
                self.win.move(y-1, self.maxx)
            if ch in (curses.ascii.BS,curses.KEY_BACKSPACE,127):
                self.win.delch()
        elif ch == curses.ascii.EOT:                           # ^d
            self.win.delch()
        elif ch == curses.ascii.ENQ:                           # ^e
            if self.stripspaces:
                self.win.move(y, self._end_of_line(y))
            else:
                self.win.move(y, self.maxx)
        elif ch in (curses.ascii.ACK, curses.KEY_RIGHT):       # ^f
            if x < self.maxx:
                self.win.move(y, x+1)
            elif y == self.maxy:
                pass
            else:
                self.win.move(y+1, 0)
        elif ch == curses.ascii.BEL:                           # ^g
            return 0
        elif ch == curses.ascii.NL:                            # ^j
            if self.maxy == 0:
                #return 0
                return 1 # HERE
            elif y < self.maxy:
                self.win.move(y+1, 0)
            #return 0 # HERE
        elif ch == curses.ascii.VT:                            # ^k
            if x == 0 and self._end_of_line(y) == 0:
                self.win.deleteln()
            else:
                # first undo the effect of self._end_of_line
                self.win.move(y, x)
                self.win.clrtoeol()
        elif ch == curses.ascii.FF:                            # ^l
            self.win.refresh()
        elif ch in (curses.ascii.SO, curses.KEY_DOWN):         # ^n
            if y < self.maxy:
                self.win.move(y+1, x)
                if x > self._end_of_line(y+1):
                    self.win.move(y+1, self._end_of_line(y+1))
        elif ch == curses.ascii.SI:                            # ^o
            self.win.insertln()
        elif ch in (curses.ascii.DLE, curses.KEY_UP):          # ^p
            if y > 0:
                self.win.move(y-1, x)
                if x > self._end_of_line(y-1):
                    self.win.move(y-1, self._end_of_line(y-1))
        return 1

    def gather(self):
        "Collect and return the contents of the window."
        #result = bytearray()
        result = ""
        self._update_max_yx()
        for y in range(self.maxy+1):
            self.win.move(y, 0)
            stop = self._end_of_line(y)
            if stop == 0: # and self.stripspaces:
                result = result + "\n"
                continue
            for x in range(self.maxx+1):
                if x > stop: # self.stripspaces and x > stop:
                  #result = result + "\n"
                  break
                #result = result + chr(curses.ascii.ascii(self.win.inch(y, x)))
                #result = result + chr(self.win.inch(y, x)) # won't work
                #result.append(self.win.inch(y, x))
                #        result=result+self.win.instr(y,x)
                result=result+str(chr(self.win.inch(y,x)))
            if self.maxy > 0:
                result = result + "\n"
        #print(self.content)
        #result=self.content
        #result=result.decode("utf-8")
        #result=str(result,"utf-8")
        # CLEAN THE TAIL
        result=strip_empty_lines_from_end(result)
        return result

    def edit(self, validate=None, ytb="NO"):
        "Edit in the widget window and collect the results."
        while 1:
            #self.altModif=1 # FORCE DEBUG 
            ch = ugetch(self.win)
            if (self.altModif == 1 and ch == ord("1")) or ch == 408:
              self.help()
              self.altModif=0
            elif (self.altModif == 1 and ch == ord("y") and ytb=="YES") or ch == 441:
              self.win.clear()
              ytb_link=hlp_ytb_dialog()
              if not (ytb_link is None):
                self.win.addstr(0,0,ytb_link)
              self._update_max_yx()
              self.win.refresh()
            elif (self.altModif == 1 and ch == ord("d")) or ch == 420:
              # DEBUG
              while ch != ord("q"):
                ch = ugetch(self.win)
                self.win.addstr(0,0,"DEBUG Key: "+ str(ord(chr(ch))) + "")
              self.altModif=0
            else: 
              if ch==27:
                 self.altModif=1
              else:
                 self.altModif=0
              if validate:
                  ch = validate(ch)
              if not ch:
                   continue
              res=self.do_command(ch)
              if res==0:
                  break
            self.win.refresh()
        if ch==24 or ch==278:
          return("")
        else:
          return(self.gather())

#if __name__ == '__main__':
#    def test_editbox(stdscr):
#        ncols, nlines = 9, 4
#        uly, ulx = 15, 20
#        stdscr.addstr(uly-2, ulx, "Use Ctrl-G to end editing.")
#        win = curses.newwin(nlines, ncols, uly, ulx)
#        rectangle(stdscr, uly-1, ulx-1, uly + nlines, ulx + ncols)
#        stdscr.refresh()
#        return inputBox(win).edit()
#
#    str = curses.wrapper(test_editbox)
#    print 'Contents of text box:', repr(str)
