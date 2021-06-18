
from subprocess import call

def speakText(input):
	cmdBegin = 'espeak '
	cmdEnd='" 2>/dev/null'
	cmdOut='"'
	cmdOut+=input
	cmdFinal=cmdBegin+cmdOut+cmdEnd
	call([cmdFinal], shell=True)
	return cmdFinal #to check command
