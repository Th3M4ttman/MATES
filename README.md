# Matt's Automatic Tracking Encounter Software

Videos:

<https://youtu.be/IkLZOhnaS2c>

<https://youtu.be/GtdwyRFSZAA>

Simple encounter tracker I slapped together in 3 days.
Entirely programmed for android phones on an android phone.

No I'm not joking.
![programming](https://i.imgur.com/BLCC92W.png)

## Requirements:


| rooted phone                                                    |
| --------------------------------------------------------------- |
| termux float - https\://github.com/termux/termux-float/releases |
| termux - https\://github.com/termux/termux-app/releases         |
| tsu - (in termux: pkg install tsu)                              |
| python (in termux: pkg install python)                          |
| tesseract (in termux: pkg install tesseract)                    |
| pytesseract (in termux: pip install pytesseract)                |
| opencv2 (in termux: pkg install opencv-python)                  |
| humanize (in termux: pip install humanize)                      |


don't get your hopes up too high. this is janky and sometimes doesnt work. if you have an issue please leave a report on the github issues page 
<https://github.com/Th3M4ttman/MATES/issues>

Installation:

clone this repo or download it as a zip and extract it where you want

git clone <https://github.com/Th3M4ttman/MATES/>


Installation is complete.

1 more step remains. launch MATES and enter the command init.

for this your onscreen buttons mhst be visible. possilbly 70% scale too.

The onscreen a/b buttons must be visible when you press enter. The only way to do this is use a floating keyboard like gboard.

Like this:
![init](https://i.imgur.com/SiIDeX3.png)
Usage:

To run the software "sudo python /whereever-you-put-it/MATES/main.py"

i would suggest adding: alias mates="sudo python /whereever-you-put-it/MATES/main.py"

to your bashrc file so that you can launch it with "mates"

![interface](https://i.imgur.com/d97zLJc.jpeg)

press enter to toggle capture on and off

Or type in commands


| Command                | Use                                            | Notes                                                                |
| ---------------------- | ---------------------------------------------- | -------------------------------------------------------------------- |
| init                   | Initialises the auto capture                   | Only needs to be performed once. A/B must be visible                 |
| Reset (Pokémon)        | Resets encounters for selected Pokémon.        | If given no Pokémon resets all                                       |
| add (number) (Pokémon) | Adds number \* Pokémon encounters              |                                                                      |
| sub (number) (Pokémon) | Subtracts number \* Pokémon encounters         |                                                                      |
| track (Pokémon)        | Sets the Pokémon as a tracked pokemon          | If given no Pokémon it tracks all Pokémon with registered encounters |
| untrack (Pokémon)      | Sets the Pokémon as an untracked pokemon       | If given no Pokémon it untracks all                                  |
| total                  | Toggles the visibility of the total encounters |                                                                      |
| charm                  | Toggles shiny charm                            |                           |
| donator                | Toggles donator                                |                           |
| link              | Toggles shiny charm link                       |                          |
| singles           | Toggles single tracking                        |                          |
