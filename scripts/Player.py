#!/usr/bin/python

import logging
import threading
import select
import subprocess
import sys
import time
import queue

PLAYER="mpv"
BUFSIZE=64
logging.basicConfig(level=logging.INFO)

class Mpv():
	def __init__(self, callback, ui_callback):
		self.playing = False
		self.proc = None
		self.callback = callback
		self.ui_callback = ui_callback
		self.stderr = "" # queue.Queue()
	def _play(self):
		while self.proc.poll() == None:
			#stdout = self.proc.stdout.read(1)
			(read, foo, bar) = select.select([self.proc.stderr], [], [])
			if self.proc.stderr in read:
				#self.stderr.put(self.proc.stderr.readline())
				self.stderr = str(self.proc.stderr.readline())
				self.ui_callback()
			
			#logging.info("stdout: %s" % (stdout))
			logging.info("stderr: %s" % (self.stderr))
			#logging.info("still reading")
		logging.info("dropped out of loop, calling callback")
		self.playing = False
		self.proc = None
		self.callback()
		
	def is_playing(self):
		return self.playing

	def is_running(self):
		return self.proc != None

	def wait(self):
		while self.proc == None:
			time.sleep(1) # XXX: bad hack
		logging.info("Waiting for proc.")
		self.proc.wait()
		logging.info("wait() returned.")
	
	def play(self, filename):
		self.playing = True
		player_command = [PLAYER, filename]
		if self.proc != None:
			self.proc.terminate()
		self.proc = subprocess.Popen(player_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		logging.info("Playing track: %s" % (filename))
		threading.Thread(target=self._play).start()
		#self._play()
		
	def comm(self, command):
		if command != "" and self.proc != None:
			logging.info("Sent command: %s" % (command))
			self.proc.stdin.write(bytes(command, 'UTF-8'))
			self.proc.stdin.flush()
