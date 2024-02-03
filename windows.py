import curses
import time
from curses import wrapper, newwin
from pokeutil import get_probability, colour_probability
import datetime

class Capture:
    def __init__(self, h, w, y, x, history):
        self.window = newwin(h, w, y, x)
        self.capturing = False
        self.window.refresh()
        self.h, self.w = self.window.getmaxyx()
        self.history = history
        

    def clear(self):
        self.window.clear()

    def addstr(self, string, color):
        self.window.addstr(0,0, "d", curses.color_pair(1) if self.history.donator else curses.color_pair(2))
        self.window.addstr(0,1, "c", curses.color_pair(1) if self.history.charm else curses.color_pair(2))
        self.window.addstr(0,2, "l", curses.color_pair(1) if self.history.linkcharm else curses.color_pair(2))
        
        bonus = str(int(float(self.history.getbonus())*100))
        
        newstr = bonus + "%"
        string = newstr + string[len(newstr) + 4:]
        self.window.addstr(0,4, str(string), color)

    def refresh(self):
        #self.clear()
        self.addstr("Capturing".center(self.w-1)  if self.capturing else "Not Capturing".center(self.w-1), curses.color_pair(1) if self.capturing else curses.color_pair(2))
        self.window.refresh()
        
    def set(self, capturing):
        self.capturing = capturing
        self.refresh()
        
    def toggle(self):
    	self.set(not self.capturing)
    	

class Counter:
	
    def __init__(self, title, h, w, y, x, history):
        self.window = newwin(h, w, y, x)
        #self.window.box()
        self.value = 0
        self.title = title
        self.visible = True
        self.window.refresh()
        self.history = history
    
    @property
    def prob(self):
    	return get_probability(self.value, self.history.donator, self.history.charm, self.history.linkcharm)
    
    

    def clear(self):
        self.window.clear()

    def addstr(self, *args, attr=0):
        self.window.addstr(*args, attr)

    def refresh(self):
        if self.visible is True:
        	end = self.window.getmaxyx()[1] - len("{self.prob}%")
        	self.window.addstr(self.title+f": {self.value}")
        	self.window.addstr(0, end, f"{self.prob}%", curses.color_pair(colour_probability(self.prob)))
        else:
        	self.clear()
        self.window.refresh()
        
    def set(self, n):
        self.clear()
        self.value = n
        self.refresh()
        
        