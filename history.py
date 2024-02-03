import os, json
from collections import defaultdict
from copy import deepcopy
from pokeutil import DEFAULT

PATH = "/".join(__file__.split("/")[:-1])
print(os.path.exists(f"{PATH}/history.json"))
class History():
	def __init__(self, fn=f"{PATH}/history.json"):
		self.fn = fn
		if os.path.isfile(fn):
			self.load()
		else:
			self.data = {}
			self.regen_dict()
	
	def regen_dict(self):
		self.data = defaultdict(int)
		for k, i in DEFAULT.items():
			self.data[k] = deepcopy(i)
		self.save()
				
	@property
	def showtotal(self):
		return self.data["showtotal"]
		
	def toggle_total(self):
		self.data["showtotal"] = not self.data["showtotal"]
		self.save()
	
	def load(self):
		#print("Loading")
		with open(self.fn) as f:
			s = json.loads(f.read())
			self.data = s
		return s
	
	def save(self):
		#print("Saving")
		with open(self.fn, "w") as f:
			s = json.dumps(self.data, indent=4)
			f.write(s)
			
	def sub(self, mons):
			self.data["Last_Addition"] = None
			mons = mons.split(", ")
			if type(mons) is str:
				mons=[mons]
			for mon in mons:
				qty, mon = mon.split("x")
				qty = int(qty)
				mon = mon.replace(" ", "")
				if mon in self.data.keys():
					self.data[mon] -= qty
				
				if self.data[mon] < 1:
					del self.data[mon]

			self.save()
	
	
	def add(self, mons):
			self.data["Last_Addition"] = mons
			mons = mons.split(", ")
			if type(mons) is str:
				mons=[mons]
			for mon in mons:
				qty, mon = mon.split("x")
				qty = int(qty)
				mon = mon.replace(" ", "")
				if mon in self.data.keys():
					self.data[mon] += qty
				else:
					self.data[mon] = qty
					
				
			self.save()
	
	@property
	def total(self):
		out = 0
		for k, i in self.data.items():
			if k in ("Last_Addition", "Tracking", "showtotal", "pcttotal", "pct"):
				continue
			out += int(i)
		return out
	
	def undo(self):
		if self.data["Last_Addition"] == None:
			return
		self.sub(self.data["Last_Addition"])
	
	def reset(self, mon=""):
		if mon == "":
			self.data = defaultdict(int)
		if mon in self.data.keys():
			self.data["Total"] -= self.data[mon]
			self.data[mon] = 0
		self.save()
		