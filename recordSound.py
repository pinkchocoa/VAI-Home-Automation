import subprocess 
import os 
import time
import signal

outputFile = 'out'
record = 'arecord --format=S16_LE --rate=16000 --file-type=wav '
record += outputFile
record += '.wav'

p = subprocess.Popen(record, shell=True, preexec_fn=os.setsid)
print("startRecordingArecord()> p pid= " + str(p.pid))
print("startRecordingArecord()> recording started")
time.sleep(20)
os.killpg(p.pid, signal.SIGTERM)
p.terminate()
p = None
print("stopRecordingArecord()> Recording stopped")
