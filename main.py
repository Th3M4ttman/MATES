from history import History
from pokeutil import *
from windows import *
import numpy as np
from console import console
import curses

history = History()

#curses window
def main(scr):
	
	global history
	
	#Initialising ths colours
	curses.start_color()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	
	#hides cursor
	curses. curs_set(0)
	
	#height and width of the terminal
	h, w = scr.getmaxyx()
	
	#Auto capture off by default
	capturing = False
	
	#stops waiting on input
	scr.nodelay(True)
	
	#initialising the windows
	capwin = Capture(1, w, 0, 1, history)
	total_window = Counter("Total", 1,w, 1, 0, history)
	
	#time until next clear of the output field
	clear_timer = None
	
	text =">: " #cmd input
	out = "" #cmd output
	
	mons = history.data["Tracking"] #which mons to track
	
	def regen(scr, mons):
		#regenerates a tracking window for each mon in mons
		windows = []
		
		for i, mon in enumerate(mons):
			windows.append(Counter(mon, i+2, w, i+2, 0, history))
		scr.clear()
		return windows, len(windows)+2, len(windows)+3
	
	#generating windows
	windows, input_line, output_line = regen(scr, mons)
	
	#whether the pokemon on screen has been reported yet
	reported = True 
	
	#timer to next auto capture
	cap_timer = datetime.datetime.now()
	
	#main program loop
	while True:
		mons = []
		
		#clears output every 4 seconds
		if clear_timer:
			if datetime.datetime.now() > clear_timer:
				out = ""
				clear_timer = None
				scr.clear()
				scr.addstr(5,0, text)
		
		#Auto capture
		if capturing and datetime.datetime.now() > cap_timer:
			cap = capture() 
			if cap:
				cropped = np.array(deepcopy(cap).crop((0,0,3040,400)))
			
				#determine if in combat
				if cap and not out_of_combat(cap) and count_mons(cropped) > 0:
					if reported: #ignore mon on screen
						mons = []
					else: #detect mons on screen
						mons = get_mons(cropped)
						
					if len(mons) > 0:
						#reports the mon to the lpg
						ti = str(datetime.datetime.now()).split(".")[0]
						log(f"[{ti}]:", list_to_words(mons))
						reported = True
						
						#adds it to the history and times out capture for 4 seconds
						history.add(list_to_words(mons))
						cap_timer = datetime.datetime.now() + datetime.timedelta(seconds=4)
						scr.addstr(output_line+1, 0, list_to_words(mons))
						
					else:
						#if no pokemon are found try again in 1 second
						cap_timer = datetime.datetime.now() + datetime.timedelta(seconds=1)
						
					#deletes the frame
					os.remove(f"{PATH}/frame.jpg")
					
				elif out_of_combat(cap):
					reported = False
					scr.clear()
					cap_timer = datetime.datetime.now() + datetime.timedelta(seconds=1)
					
			scr.refresh()
		
		#sets the visibility of the total encounters
		total_window.visible = history.showtotal
		
		#updates the total encounters
		total_window.set(history.total)
		
		#update each of the counters
		for window in windows:
			if window.title in history.data.keys():
				n = history.data[window.title]
			else:
				n = 0
			window.set(n)
		
		#updates the capture indicator
		capwin.set(capturing)
		
		#getting keyboard input
		try:
			key = scr.getkey()
		except:
			key = ""
		
		if key == "\n": #run command
			if text.replace(">: ", "") in ("quit", "exit", "qq"):
				return #exit the program
			try:
				if text.replace(">: ", "") == "": #press enter to toggle capture
					capturing = not capturing
				else: #execute command
					out = console(text.replace(">: ", ""), history)
					history.save()
				
				#reset the terminal area
				text =">: "
				scr.clear()
				clear_timer = datetime.datetime.now() + datetime.timedelta(seconds=3)
				
				#regenerate the tracking windows
				if "Tracking" in out or "Untracking" in out or "Untracked" in out:
					windows, input_line, output_line = regen(scr, history.data["Tracking"])
					
			except Exception as e:
				out = ""
				text =">: "
				scr.clear() 
				
		elif key in abc: #add letter to the input
			text += key
			
		elif key == "\x7f": #backspace
			if len(text) > 3:
				text = text[:-1]
			scr.clear() 
		
		try: #command output
			scr.addstr(input_line,0, text)
			scr.addstr(output_line,0, out)
		except TypeError:
			scr.addstr(6,0, "Unkown Error.")
			clear_timer = datetime.datetime.now() + datetime.timedelta(seconds=3)
			out = ""
	
		scr.refresh()
		
		time.sleep(.2)
	return 

#run program
x = curses.wrapper(main)
