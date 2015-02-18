#!/usr/bin/python3

import os
os.system("mkdir -p split")
os.chdir("split")
cmd = 'while read line; do echo -n "$(echo $line | awk \'{print $NF}\'),"; done < ../splits.txt | sed s/\,[^\,]*\,$//g > marks.txt'
os.system(cmd)
os.system("mkvmerge --split timecodes:$(cat marks.txt) ../matchday_fixed_aac.mkv -o matchday_split.mkv")
cmd = 'while read line; do echo "$(echo $line | awk \'{first = $NF; $NF = ""; print $0}\' | sed s/\ *$/.mkv/)"; done < ../splits.txt > names.txt'
os.system(cmd)
os.system("ls matchday_split-0* > files.txt")
names = open("names.txt", "r")
files = open("files.txt", "r")

name = names.readline()
cur = files.readline()

while name != "":
	print("os.rename(" + cur.rstrip() + " ," +  name.rstrip() + ")")
	os.rename(cur.rstrip(), name.rstrip())
	name = names.readline()
	cur = files.readline()

