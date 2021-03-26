import subprocess 
import os 
import time
import signal


def recordSound(output, duration):

	def stopRec(p, duration):
		time.sleep(duration)
		print("stop recording pid: " + str(p.pid))
		os.killpg(p.pid, signal.SIGTERM)
		p.terminate()
		p = None

	record = 'arecord --format=S16_LE --rate=16000 --file-type=wav '
	record += output
	record += '.wav'

	p = subprocess.Popen(record, shell=True, preexec_fn=os.setsid)
	print("startRecordingArecord()> p pid= " + str(p.pid))
	print("startRecordingArecord()> recording started")
	stopRec(p, duration)

def playSound(input):
	arg = 'aplay '
	arg += input
	arg += '.wav'
	print("playing: " + arg)
	subprocess.call(arg, shell=True)


recordSound('out', 5)
playSound('out')
