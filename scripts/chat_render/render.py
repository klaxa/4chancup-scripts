#!/usr/bin/python

from decimal import *
import ast
import sys
import time
import os

X_POS = 3.0
Y_POS = 314.5
Y_DIFF = 12
SLOTS = 10
CHARS = 80
OUT = "temp.ass"
BASE = "/home/4chancup/chat_render/base.ass"

class Element():
	def __init__(self, item):
		self.content = item
		self.next = None
		self.prev = None
	
	def __repr__(self):
		return str(item)
	
	def __str__(self):
		return str(item)

class MyQueue():
	def __init__(self):
		self.placeholder = dict()
		self.placeholder["type"] = "message"
		self.placeholder["message"] = ""
		self.placeholder["nick"] = ""
		self.placeholder["time"] = 0.0
		self.MAX_ELEMS = SLOTS + 1
		self.elements = 0
		self.head = None
		self.tail = None
		while self.elements != self.MAX_ELEMS - 1:
			self.add(self.placeholder)
	
	def add(self, item):
		if self.tail != None:
			new_tail = Element(item)
			new_tail.prev = self.tail
			self.tail.next = new_tail
			self.tail = new_tail
		else:
			self.tail = Element(item)
			self.head = self.tail
		self.elements += 1
		if self.elements > self.MAX_ELEMS:
			new_head = self.head.next
			self.head = new_head
			self.head.prev = None
			self.elements -= 1
	
	def __repr__(self):
		item = self.head
		result = "%d Elements: [\n" % (self.elements)
		while item != None:
			result += str(item.content) + ", \n"
			item = item.next
		result += "]\n\n"
		return result

class Renderer():

	def gen_line(self, line, ts_start, ts_end, off):
		# "Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,{\\an4\\alpha90\\fscx100\\fscy100\pos(347.556,338.556)}<klaxa> hello world does this line up? I mean it's mono"
		start = self.ts2str(ts_start)
		end = self.ts2str(ts_end)
		#print(start + " -> " + end + "  : " +str(ts_end + self.start_time))
		if ts_end < ts_start:
			print("WTF")
			print(line)
		return "Dialogue: 0,%s,%s,Default,,0,0,0,,{\\an4\\alpha50\\fscx100\\fscy100\pos(%.3f,%.3f)}%s\n" % (start, end, X_POS, Y_POS + off * Y_DIFF, line)

	def generate_ass(self, queue):
		result = ""
		cur = queue.head
		next = cur.next
		off = 0
		while next != None:
			nick = cur.content["nick"]
			msg = cur.content["message"]
			line = ""
			if nick != "":
				line = "<%s> %s" % (nick, msg)
			line = line[0:79]
			ts_start = queue.tail.prev.content["time"]
			ts_end = queue.tail.content["time"]
			#print(str(ts_start) + " -> " + str(ts_end) + " " + line)
			result += self.gen_line(line, ts_start, ts_end, off)
			cur = next
			next = next.next
			off += 1
		return result
	def __init__(self):
		self.log_file = sys.argv[1]
		self.start_time = float(sys.argv[2])
		self.duration = float(sys.argv[3])
		self.queue = MyQueue()
		self.chat_log = open(self.log_file, "r")
		self.out = open(OUT, "w")

	def box_line(self, duration):
		return "Dialogue: 0,0:00:00.00,%s,Default,,0,0,0,,{\\alphaB0\\an1\\fscx426\\fscy125\pos(0,432.776)} {\p1}m 0 0 l 100 0 100 100 0 100{\p0}\n" % (duration)

	def ts2str(self, ts):
		
		new_ts = time.strftime("%H:%M:%S", time.gmtime(int(ts)))[1:]
		ms = ts % 1
		ms = Decimal(str(ms)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
		new_ts += str(ms)[1:]
		return new_ts
	
	def start(self):
		duration = self.ts2str(self.duration)
		
		#self.out.write(self.box_line(duration))
		line = self.chat_log.readline()
		run = True
		while line != "" and run:
			item = ast.literal_eval(line)
			if item["type"] == "message":
				item["time"] = item["time"] - self.start_time
				if item["time"] >= 0:
					self.queue.add(item)
					self.out.write(self.generate_ass(self.queue))
				if item["time"] > self.duration:
					#print("end of file")
					#print(item["time"])
					run = False
			line = self.chat_log.readline()
			
			
		self.out.close()
		self.chat_log.close()
		os.system("cat " + BASE + " " + OUT + " > chat.ass")
if __name__ == "__main__":
	renderer = Renderer()
	renderer.start()
