import subprocess

def fileTransfer(localFile, dest, remoteFile, path="~/"):
	def callCmd(cmd):
		try:
			subprocess.run([cmd], check=True)
		except subprocess.CalledProcessError:
			print("Failed tor run, command was: " + cmd)
	# scp pi@a.local:~/path pi@b.local:~/path
	cmd = "scp " + path + localFile
	cmd += " pi@" + dest + ":" + path
	#print(cmd)
	callCmd(cmd)

fileTransfer("out.wav", "kkpi.local", "out.wav")
