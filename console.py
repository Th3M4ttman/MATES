from pokeutil import pokes, init_out_of_combat


def console(cmd, history):
	parts = cmd.split(" ")
	if parts[0] == "init":
		init_out_of_combat()
		return "Initialised"
	if parts[0] in ("+", "add"):
		if parts[1].isnumeric():
			if parts[2].title() in pokes:
				history.add(f"{parts[1]}x {parts[2].title()}")
				return f"Added {parts[1]}x {parts[2].title()}"
			else:
				return f"{parts[2].title()} not found"
		else:
			return f"{parts[1]} is not a number"
	if parts[0][0] == "+" and parts[0].replace("+", "").isnumeric():
		if parts[1].title() in pokes:
			history.add(f"{parts[0][1:]}x {parts[1].title()}")
			return f"Added {parts[0][1:]}x {parts[1].title()}"
		else:
			return f"{parts[1].title()} not found"
			
	if parts[0]  in ("-", "sub"):
		if parts[1].isnumeric():
			if parts[2].title() in pokes:
				history.sub(f"{parts[1]}x {parts[2].title()}")
				return f"Subtracted {parts[1]}x {parts[2].title()}"
			else:
				return f"{parts[2].title()} not found"
		else:
			return f"{parts[1]} is not a number"
	if parts[0][0] == "-" and parts[0][1:].isnumeric():
		if parts[1].title() in pokes:
			history.sub(f"{parts[0][1:]}x {parts[1].title()}")
			return f"Subtracted {parts[0][1:]}x {parts[1].title()}"
		else:
			return f"{parts[1].title()} not found"
			
	if parts[0] == "reset":
		if len(parts) > 1:
			if parts[1].title() in pokes:
				del history.data[parts[1].title()]
				return  "Reset " + parts[1].title()
			else:
				return f"No such pokemon: {parts[1].title()}"
		history.regen_dict()
		return "Reset Progress"
	
	if parts[0] == "total":
		history.toggle_total()
		return "Toggled Total"
		
	if parts[0] == "track":
		if len(parts) == 1:
			history.data["Tracking"] = [p for p in history.data.keys() if p not in ["Last_Addition", "Tracking", "showtotal", "pct", "pcttotal"]]
			history.save()
			return "Tracking all encountered"
		if parts[1].title() in pokes:
			if parts[1].title() in history.data["Tracking"]:
				return "Already tracking "+ parts[1].title() 
			else:
				history.data["Tracking"].append(parts[1].title())
				history.save()
			return f"Tracking {parts[1].title()}"
		else:
			return f"No such pokemon: {parts[1].title()}"
			
	if parts[0] == "untrack":
		if len(parts) == 1:
			history.data["Tracking"] = []
			history.save()
			return "Untracked all"
			
		if parts[1] == "0":
			history.data["Tracking"] = [poke for poke in history.data["Tracking"] if poke in history.data.keys() ]
			history.save()
			return "Untracked all 0s"
			
		if parts[1].title() in pokes:
			if parts[1].title() not in history.data["Tracking"]:
				return "Not tracking "+ parts[1].title() 
			else:
				history.data["Tracking"].pop(history.data["Tracking"].index(parts[1].title()))
				history.save()
			return f"Untracking {parts[1].title()}"
		else:
			return f"No such pokemon: {parts[1].title()}"
			
	return f"Unknown Command"
