import curses
from curses import newwin
from pokeutil import get_probability, colour_probability

class Capture:
    def __init__(self, h, w, y, x):
        self.window = newwin(h, w, y, x)
        self.capturing = False
        self.window.refresh()
        self.h, self.w = self.window.getmaxyx()
        
    def clear(self):
        self.window.clear()

    def addstr(self, string, color):
        self.window.addstr(0,0, str(string), color)

    def refresh(self):
        self.addstr("Capturing".center(self.w-1)  if self.capturing else "Not Capturing".center(self.w-1), curses.color_pair(1) if self.capturing else curses.color_pair(2))
        self.window.refresh()
        
    def set(self, capturing):
        self.capturing = capturing
        self.refresh()
        
    def toggle(self):
    	self.set(not self.capturing)
    	

class Counter:
	
    def __init__(self, title, h, w, y, x):
        self.window = newwin(h, w, y, x)
        self.value = 0
        self.title = title
        self.visible = True
        self.window.refresh()
    
    @property
    def prob(self):
    	return get_probability(self.value)

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
        
        