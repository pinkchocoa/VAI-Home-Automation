#!/usr/bin/env python3

#pip install num2words
#from num2words import num2words #idk why this is needed
from subprocess import call

cmdBegin = 'espeak '
cmdEnd='" 2>/dev/null'
cmdOut='"'
#cmdEnd = ' | aplay /home/pi/Destop/text.wav 2>/dev/null' # play text.wav and dump errors to /dev/null
#cmdOut = '--stdout > /home/pi/Desktop/text.wav ' #store the voice file

text = input("Enter text: ")
print("speaking... ", text)
#text = text.replace(' ', '_') #need to replace spaces with underscores to identify as a command
cmdOut += text

cmdFinal = cmdBegin+cmdOut+cmdEnd
print("running cmd: ", cmdFinal)


call([cmdFinal], shell=True)
