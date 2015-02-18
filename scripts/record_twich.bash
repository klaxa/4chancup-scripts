#!/bin/bash
date=$(date +%s | tr '\n' ' '; date)
date=$(date)
stream="http://www.twitch.tv/the4chancup"
#stream="http://www.twitch.tv/gamesdonequick"

livestreamer -Q -O $stream best | /root/tools/ffmpeg/ffmpeg -i - -map 0:a -map 0:v -c copy -absf aac_adtstoasc -metadata creation=$(date +%s) "$date".mkv
#livestreamer -Q -O $stream best | /root/tools/ffmpeg/ffmpeg -i - -map 0:a -map 0:v -c copy -absf aac_adtstoasc -metadata creation=$(date +%s) "agdq/$date".mkv
