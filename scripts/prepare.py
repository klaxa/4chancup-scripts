#!/usr/bin/python

import time
import subprocess
import os
import sys


DRYRUN = False
NO_SUB = False

if len(sys.argv) > 1:
	if "--dry" in sys.argv:
		DRYRUN = True
	if "--no-chat" in sys.argv:
		NO_SUB = True
def call(cmd):
	if not DRYRUN:
		os.system(cmd)

FFPROBE="/root/tools/ffmpeg/ffprobe"
FILE="matchday_fixed_aac.mkv"

cmd = 'mkvinfo -s matchday_fixed_aac.mkv | grep track\ 1 | grep I\ frame | grep -o -E "[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}\.[0-9]{3}" > I-frames_stripped.txt'
print(cmd)
call(cmd)

probe = subprocess.Popen([FFPROBE, FILE], stderr=subprocess.PIPE)
line = str(probe.stderr.readline())[2:-1].rstrip()

def str2ts(string):
	#print("str2ts: " + string)
	string = string.split(":")
	hours = int(string[0])
	minutes = int(string[1])
	seconds = float(string[2])
	return 3600 * hours + 60 * minutes + seconds

duration = 0
start = 0

while line != "":
	#print(line)
	if "Duration" in line:
		#print(line.split(" "))
		#print("line: " + line.split(" ")[3][:-1])
		duration = str2ts(line.split(" ")[3][:-1])
		print(duration)
	elif "CREATION" in line:
		start = line.split(" ")[-1][:-2]
		print(start)
	line = str(probe.stderr.readline())[2:-1].rstrip()
if not NO_SUB:
	cmd = "python3 ../../../chat_render/render.py ../../../logger/latest.log " + str(start) + " " + str(duration)
	print(cmd)
	call(cmd)
	cmd = "mkvmerge -o matchday_fixed_aac_w_chat.mkv -S matchday_fixed_aac.mkv chat.ass --attach-file /home/4chancup/chat_render/Consolas.ttf"
	print(cmd)
	call(cmd)
	cmd = "mv matchday_fixed_aac.mkv matchday_fixed_aac_wo_chat.mkv; mv matchday_fixed_aac_w_chat.mkv matchday_fixed_aac.mkv"
	print(cmd)
	call(cmd)

