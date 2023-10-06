#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import feedparser
import random, string
import os, sys
import signal



def exit():
    print("exiting")
    os._exit(os.EX_OK)


def randfilename():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(5))


def getMP3(links):
    for link in links:
        url = link.href
        if link.rel == 'enclosure':
            return url
    return None

def youtubeExits(post):
    return False

def downloadMP3(url):
    suffix = "." + url.rsplit(".", 1)[1]
    tmp = randfilename() + suffix
    os.system("wget {} -O {}".format(url,tmp))
    return tmp

def MP3toMP4(mp3):
    mp4 = mp3.rsplit(".", 1)[0] + ".mp4"
    os.system("ffmpeg -loop 1 -i .github/youtube.png -i {} -vf 'scale=-1:360 :force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1:color=black,setsar=1,format=yuv420p' -framerate 2 -preset  ultrafast -shortest -fflags +shortest {}".format(mp3,mp4))
    return  mp4

def publishMP4toYoutube(mp4,title):
    print("【{}】 upload {} to youtube".format(title,mp4))
    os.system("youtubeuploader --filename {} -title='{}' -secrets=youtube-token.json -privacy=public".format(mp4,title))
    return 



def main():
    signal.signal(signal.SIGINT,exit)

    NewsFeed = feedparser.parse('https://feeds.osf2f.net/osf2f.xml')
    try:
        for entry in NewsFeed.entries:
        
            # Print rss feed keys
            # print(entry.keys())
        
            # Check Post ready publish on youtube
            if youtubeExits(entry.title):
                print("【{}】 eady published, skipped".format(entry.title))
                continue
            mp3Url = getMP3(entry.links)
            if not  mp3Url:
                print("【{}】 mp3 link not found, skipped".format(entry.title))
                continue
        
            print("【{}】 downloading {} ".format(entry.title,mp3Url))
            mp3 = downloadMP3(mp3Url)
        
            if not mp3:
                continue
            print("{} {} successed".format(mp3Url,mp3))
        
            mp4 = MP3toMP4(mp3)
            if mp4:
                publishMP4toYoutube(mp4,entry.title)
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE


main()
