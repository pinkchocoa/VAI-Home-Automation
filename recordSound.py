import subprocess 
import os 
import time
import signal


def recordSound(output, duration):
	record = 'arecord --format=S16_LE --rate=16000 --file-type=wav '
	record += output
	record += '.wav'

	p = subprocess.Popen(record, shell=True, preexec_fn=os.setsid)
	print("startRecordingArecord()> p pid= " + str(p.pid))
	print("startRecordingArecord()> recording started")
	time.sleep(duration)
	os.killpg(p.pid, signal.SIGTERM)
	p.terminate()
	p = None
	print("stopRecordingArecord()> Recording stopped")

def playSound(input):
	arg = 'aplay '
	arg += input
	arg += '.wav'
	print("playing: " + arg)
	subprocess.call(arg, shell=True)


recordSound('out', 5)
playSound('out')
