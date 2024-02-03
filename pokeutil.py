
import subprocess
from PIL import Image, ImageChops
import os
import cv2
import numpy as np
import time
from difflib import get_close_matches
from copy import deepcopy
import datetime
import os
import pathlib



pt = True

if pt:
	import pytesseract
	

#path of this file
PATH = "/".join(__file__.split("/")[:-1])

def get_device_proportions():
	#captures a frame using android screencap
	if pt:
		os.system(f"screencap -p {PATH}/base3.jpg")
	out = Image.open(f"{PATH}/base3.jpg").size
	os.remove(f"{PATH}/base3.jpg")
	return out

proportions = get_device_proportions()
device_y, device_x = min(proportions), max(proportions)
print(device_x, "x", device_y, sep="")

def get_grayscale(image):
	#converts image to black and white
	return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)


def thresholding(image):
	#applies thresholding to the image
	return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def capture():
	#captures a frame using android screencap
	if pt:
		os.system(f"screencap -p /{PATH}/frame.jpg")
	
	#opens the image and returns it
	try:
		return Image.open(f"{PATH}/frame.jpg")
	except FileNotFoundError:
		return None

def get_text(image):
	#post process the image for OCR
	gray = get_grayscale(image)
	thresh = thresholding(gray)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)
	
	#if pytesseract installed extract text from image
	if pt:
		#Image.fromarray(opening).save("/data/data/com.termux/files/home/Testo/wtf.jpg")
		return pytesseract.image_to_string(opening, lang = 'eng', config = '--psm 6')
	return
	
def init_out_of_combat():
	if pt:
		os.system(f"screencap -p {PATH}/base2.jpg")
	base = cv2.imread(f'{PATH}/base2.jpg')
	base = Image.fromarray(base)
	
	#postprocess
	gray = get_grayscale(base)
	thresh = thresholding(gray)
	image = Image.fromarray(thresh)
	
	#crop the image
	left = device_x // 1.3234
	top = device_y // 1.44
	right = device_x // 1.0857
	bottom = device_y // 1.2307
	
	image = image.crop((left, top, right, bottom))
	image = image.convert("RGB")
	image.save(f'{PATH}/base.jpg')



def out_of_combat(image):
	
	image = np.array(image)
	
	#the a + b button image
	base = cv2.imread(f'{PATH}/base.jpg')
	base = Image.fromarray(base)
	
	#postprocess
	gray = get_grayscale(image)
	thresh = thresholding(gray)
	image = Image.fromarray(thresh)
	
	#crop the image
	left = device_x // 1.3234
	top = device_y // 1.44
	right = device_x // 1.0857
	bottom = device_y // 1.2307
	
	image = image.crop((left, top, right, bottom))
	image = image.convert("RGB")
	
	#determine if we're out of combat'
	out = ImageChops.difference(base, image)
	out.crop(out.getbbox())
	out = np.average(np.array(out)) < 30
	return out
	
def get_probability(encounters, donator=False, charm=False, charmlink=False):
	# gets probability of success
	
	rate = 30_000 #base shiny rate
	
	if donator:
		rate -= rate*.1 #10% 
	if charm:
		rate -= rate*.1 #10% 
	elif charmlink:
		rate -= rate*0.05 #5% 
	
	rate = 1/rate
	return round((rate*100)*encounters, 1)
	

def colour_probability(prob):
	#return coloured percentage of probability
	if prob < 25:
		return 2
	elif prob < 50:
		return 3
	elif prob < 75:
		return 5
	return 1


#default history dictionary
DEFAULT = {
    "showtotal": True,
    "pcttotal": True,
    "pct": True,
    "Tracking": [
    ],
    "Last_Addition": None,
}

#list of pokemon
pokes = ['Bulbasaur', 'Caterpie', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Metapod', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Butterfree', 'Staryu', 'Starmie', 'Mr. Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Weedle', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kakuna', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Beedrill', 'Mewtwo', 'Mew', 'Chikorita', 'Bayleef', 'Meganium', 'Cyndaquil', 'Quilava', 'Typhlosion', 'Totodile', 'Croconaw', 'Pidgey', 'Feraligatr', 'Sentret', 'Furret', 'Hoothoot', 'Noctowl', 'Ledyba', 'Ledian', 'Spinarak', 'Ariados', 'Crobat', 'Pidgeotto', 'Chinchou', 'Lanturn', 'Pichu', 'Cleffa', 'Igglybuff', 'Togepi', 'Togetic', 'Natu', 'Xatu', 'Mareep', 'Pidgeot', 'Flaaffy', 'Ampharos', 'Bellossom', 'Marill', 'Azumarill', 'Sudowoodo', 'Politoed', 'Hoppip', 'Skiploom', 'Jumpluff', 'Rattata', 'Aipom', 'Sunkern', 'Sunflora', 'Yanma', 'Wooper', 'Quagsire', 'Espeon', 'Umbreon', 'Murkrow', 'Slowking', 'Ivysaur', 'Raticate', 'Misdreavus', 'Unown', 'Wobbuffet', 'Girafarig', 'Pineco', 'Forretress', 'Dunsparce', 'Gligar', 'Steelix', 'Snubbull', 'Spearow', 'Granbull', 'Qwilfish', 'Scizor', 'Shuckle', 'Heracross', 'Sneasel', 'Teddiursa', 'Ursaring', 'Slugma', 'Magcargo', 'Fearow', 'Swinub', 'Piloswine', 'Corsola', 'Remoraid', 'Octillery', 'Delibird', 'Mantine', 'Skarmory', 'Houndour', 'Houndoom', 'Ekans', 'Kingdra', 'Phanpy', 'Donphan', 'Porygon2', 'Stantler', 'Smeargle', 'Tyrogue', 'Hitmontop', 'Smoochum', 'Elekid', 'Arbok', 'Magby', 'Miltank', 'Blissey', 'Raikou', 'Entei', 'Suicune', 'Larvitar', 'Pupitar', 'Tyranitar', 'Lugia', 'Pikachu', 'Ho-Oh', 'Celebi', 'Treecko', 'Grovyle', 'Sceptile', 'Torchic', 'Combusken', 'Blaziken', 'Mudkip', 'Marshtomp', 'Raichu', 'Swampert', 'Poochyena', 'Mightyena', 'Zigzagoon', 'Linoone', 'Wurmple', 'Silcoon', 'Beautifly', 'Cascoon', 'Dustox', 'Sandshrew', 'Lotad', 'Lombre', 'Ludicolo', 'Seedot', 'Nuzleaf', 'Shiftry', 'Taillow', 'Swellow', 'Wingull', 'Pelipper', 'Sandslash', 'Ralts', 'Kirlia', 'Gardevoir', 'Surskit', 'Masquerain', 'Shroomish', 'Breloom', 'Slakoth', 'Vigoroth', 'Slaking', 'Nidoran♀', 'Nincada', 'Ninjask', 'Shedinja', 'Whismur', 'Loudred', 'Exploud', 'Makuhita', 'Hariyama', 'Azurill', 'Nosepass', 'Venusaur', 'Nidorina', 'Skitty', 'Delcatty', 'Sableye', 'Mawile', 'Aron', 'Lairon', 'Aggron', 'Meditite', 'Medicham', 'Electrike', 'Nidoqueen', 'Manectric', 'Plusle', 'Minun', 'Volbeat', 'Illumise', 'Roselia', 'Gulpin', 'Swalot', 'Carvanha', 'Sharpedo', 'Nidoran♂', 'Wailmer', 'Wailord', 'Numel', 'Camerupt', 'Torkoal', 'Spoink', 'Grumpig', 'Spinda', 'Trapinch', 'Vibrava', 'Nidorino', 'Flygon', 'Cacnea', 'Cacturne', 'Swablu', 'Altaria', 'Zangoose', 'Seviper', 'Lunatone', 'Solrock', 'Barboach', 'Nidoking', 'Whiscash', 'Corphish', 'Crawdaunt', 'Baltoy', 'Claydol', 'Lileep', 'Cradily', 'Anorith', 'Armaldo', 'Feebas', 'Clefairy', 'Milotic', 'Castform', 'Kecleon', 'Shuppet', 'Banette', 'Duskull', 'Dusclops', 'Tropius', 'Chimecho', 'Absol', 'Clefable', 'Wynaut', 'Snorunt', 'Glalie', 'Spheal', 'Sealeo', 'Walrein', 'Clamperl', 'Huntail', 'Gorebyss', 'Relicanth', 'Vulpix', 'Luvdisc', 'Bagon', 'Shelgon', 'Salamence', 'Beldum', 'Metang', 'Metagross', 'Regirock', 'Regice', 'Registeel', 'Ninetales', 'Latias', 'Latios', 'Kyogre', 'Groudon', 'Rayquaza', 'Jirachi', 'Deoxys', 'Turtwig', 'Grotle', 'Torterra', 'Jigglypuff', 'Chimchar', 'Monferno', 'Infernape', 'Piplup', 'Prinplup', 'Empoleon', 'Starly', 'Staravia', 'Staraptor', 'Bidoof', 'Charmander', 'Wigglytuff', 'Bibarel', 'Kricketot', 'Kricketune', 'Shinx', 'Luxio', 'Luxray', 'Budew', 'Roserade', 'Cranidos', 'Rampardos', 'Zubat', 'Shieldon', 'Bastiodon', 'Burmy', 'Wormadam', 'Mothim', 'Combee', 'Vespiquen', 'Pachirisu', 'Buizel', 'Floatzel', 'Golbat', 'Cherubi', 'Cherrim', 'Shellos', 'Gastrodon', 'Ambipom', 'Drifloon', 'Drifblim', 'Buneary', 'Lopunny', 'Mismagius', 'Oddish', 'Honchkrow', 'Glameow', 'Purugly', 'Chingling', 'Stunky', 'Skuntank', 'Bronzor', 'Bronzong', 'Bonsly', 'Mime Jr.', 'Gloom', 'Happiny', 'Chatot', 'Spiritomb', 'Gible', 'Gabite', 'Garchomp', 'Munchlax', 'Riolu', 'Lucario', 'Hippopotas', 'Vileplume', 'Hippowdon', 'Skorupi', 'Drapion', 'Croagunk', 'Toxicroak', 'Carnivine', 'Finneon', 'Lumineon', 'Mantyke', 'Snover', 'Paras', 'Abomasnow', 'Weavile', 'Magnezone', 'Lickilicky', 'Rhyperior', 'Tangrowth', 'Electivire', 'Magmortar', 'Togekiss', 'Yanmega', 'Parasect', 'Leafeon', 'Glaceon', 'Gliscor', 'Mamoswine', 'Porygon-Z', 'Gallade', 'Probopass', 'Dusknoir', 'Froslass', 'Rotom', 'Venonat', 'Uxie', 'Mesprit', 'Azelf', 'Dialga', 'Palkia', 'Heatran', 'Regigigas', 'Giratina', 'Cresselia', 'Phione', 'Venomoth', 'Manaphy', 'Darkrai', 'Shaymin', 'Arceus', 'Victini', 'Snivy', 'Servine', 'Serperior', 'Tepig', 'Pignite', 'Charmeleon', 'Diglett', 'Emboar', 'Oshawott', 'Dewott', 'Samurott', 'Patrat', 'Watchog', 'Lillipup', 'Herdier', 'Stoutland', 'Purrloin', 'Dugtrio', 'Liepard', 'Pansage', 'Simisage', 'Pansear', 'Simisear', 'Panpour', 'Simipour', 'Munna', 'Musharna', 'Pidove', 'Meowth', 'Tranquill', 'Unfezant', 'Blitzle', 'Zebstrika', 'Roggenrola', 'Boldore', 'Gigalith', 'Woobat', 'Swoobat', 'Drilbur', 'Persian', 'Excadrill', 'Audino', 'Timburr', 'Gurdurr', 'Conkeldurr', 'Tympole', 'Palpitoad', 'Seismitoad', 'Throh', 'Sawk', 'Psyduck', 'Sewaddle', 'Swadloon', 'Leavanny', 'Venipede', 'Whirlipede', 'Scolipede', 'Cottonee', 'Whimsicott', 'Petilil', 'Lilligant', 'Golduck', 'Basculin', 'Sandile', 'Krokorok', 'Krookodile', 'Darumaka', 'Darmanitan', 'Maractus', 'Dwebble', 'Crustle', 'Scraggy', 'Mankey', 'Scrafty', 'Sigilyph', 'Yamask', 'Cofagrigus', 'Tirtouga', 'Carracosta', 'Archen', 'Archeops', 'Trubbish', 'Garbodor', 'Primeape', 'Zorua', 'Zoroark', 'Minccino', 'Cinccino', 'Gothita', 'Gothorita', 'Gothitelle', 'Solosis', 'Duosion', 'Reuniclus', 'Growlithe', 'Ducklett', 'Swanna', 'Vanillite', 'Vanillish', 'Vanilluxe', 'Deerling', 'Sawsbuck', 'Emolga', 'Karrablast', 'Escavalier', 'Arcanine', 'Foongus', 'Amoonguss', 'Frillish', 'Jellicent', 'Alomomola', 'Joltik', 'Galvantula', 'Ferroseed', 'Ferrothorn', 'Klink', 'Charizard', 'Poliwag', 'Klang', 'Klinklang', 'Tynamo', 'Eelektrik', 'Eelektross', 'Elgyem', 'Beheeyem', 'Litwick', 'Lampent', 'Chandelure', 'Poliwhirl', 'Axew', 'Fraxure', 'Haxorus', 'Cubchoo', 'Beartic', 'Cryogonal', 'Shelmet', 'Accelgor', 'Stunfisk', 'Mienfoo', 'Poliwrath', 'Mienshao', 'Druddigon', 'Golett', 'Golurk', 'Pawniard', 'Bisharp', 'Bouffalant', 'Rufflet', 'Braviary', 'Vullaby', 'Abra', 'Mandibuzz', 'Heatmor', 'Durant', 'Deino', 'Zweilous', 'Hydreigon', 'Larvesta', 'Volcarona', 'Cobalion', 'Terrakion', 'Kadabra', 'Virizion', 'Tornadus', 'Thundurus', 'Reshiram', 'Zekrom', 'Landorus', 'Kyurem', 'Keldeo', 'Meloetta', 'Genesect', 'Alakazam', 'Deoxys', 'Wormadam', 'Wormadam', 'Shaymin', 'Giratina', 'Rotom', 'Rotom', 'Rotom', 'Machop', 'Rotom', 'Rotom', 'Castform', 'Castform', 'Castform', 'Basculin', 'Machoke', 'Machamp', 'Bellsprout', 'Squirtle', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Wartortle', 'Slowbro', 'Magnemite', 'Magneton', "Farfetch'd", 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Blastoise', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler']

abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-+ " #acceptable characters

def count_mons(image:np.ndarray, threshold:float =0.8) -> int:
	template = cv2.imread(f"{PATH}/hp.png", 0)
	
	gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
	
	
	#counts the number of hp icons in the upper half of the screen
	matches = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where(matches >= threshold)
	
	i = 0
	for _ in zip(*loc[::-1]):
		i += 1
		#cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
	return int(i/3)
	
	
def get_mons(cap):
	cap = Image.fromarray(cap)
	h, w = cap.size

	left = 0
	top = 0
	right = device_x
	bottom = device_y//3.6

	cap = cap.crop((left, top, right, bottom)).convert("RGB")
	x = get_text(cap).split(" ")
	out = []
	for i in x:
		if len(i) > 2 and i.isalpha():
			if get_close_matches(i, pokes):
				out.append(get_close_matches(i, pokes)[0])
	#print(out)
	num = count_mons(cap)
	if len(out) == 0:
		return []
	while len(out) < num:
		out.append(out[0])
	return out
	
def log(*text, sep=" ", end="\n"):
	with open("./log.txt", "a") as f:
		f.write(sep.join([str(t) for t in text])+end)
		print(*text, sep=sep, end=end)



def list_to_words(listo):
	out = ""
	mons = set(listo)
	for mon in mons:
		if out != "":
			out += ", "
		out += str(listo.count(mon)) +"x " + mon
	return out