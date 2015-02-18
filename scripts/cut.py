#!/usr/bin/python

from Player import Mpv
import os
import subprocess

class Cutter():
	
	def done_cb(self):
		pass
	def update_cb(self):
		
		tc = str(self.mpv.stderr).split(" ")[1]
		if tc != self.old_tc:
			grep = subprocess.Popen(["grep", tc, "I-frames_stripped.txt"], stdout=subprocess.PIPE)
			self.old_tc = tc
			tc = str(grep.stdout.readline())[2:-3]
			#print(tc)
			if tc != "":
				print(tc)
				os.system("echo " + tc + " | xclip -selection clipboard")
				os.system("echo " + tc + " | xclip")

	def __init__(self):
		self.mpv = Mpv(self.done_cb, self.update_cb)
		self.old_tc = ""
	def start(self):
		self.mpv.play("matchday_fixed_aac.mkv")
if __name__ == "__main__":
	cutter = Cutter()
	cutter.start()
