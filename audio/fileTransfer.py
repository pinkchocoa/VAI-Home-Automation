import subprocess

def fileTransfer(source, localFile, dest, remoteFile, path="~/"):
	def callCmd(cmd):
		try:
			subprocess.run([cmd], check=True)
		except subprocess.CalledProcessError:
			print("Failed tor run, command was: " + cmd)
	# scp pi@a.local:~/path pi@b.local:~/path
	cmd = "scp " + source + ":" +  path + localFile
	cmd += " pi@" + dest + ":" + path
	#print(cmd)
	callCmd(cmd)

fileTransfer("jas.local", "out.wav", "kkpi.local", "out.wav")
