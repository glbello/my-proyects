import jsonReader
import random
#import msvcrt
#from gtts import gTTS
#tts = gTTS(text='strike', lang='en')
#tts.save("ejemplo.mp3")

import pyglet
#pyglet.resource.media("ejemplo.mp3").play()

d1 = {"by":1, "by that": 2}
d2 = {"by_3": 1, "by_1":2,"by that":4}


#d_list = list(d2.keys())
word = "by"
#n = max([int(w[-1]) for w in list(d2.keys()) if w+"_" in w])


d = [int(w[-1]) for w in list(d2.keys()) if "by_" in w]










