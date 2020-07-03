#this script requires a txt file with song urls as input, and a folder path to download to.
# ^ both are given as command line parameters.
#no need to change DOWNLOAD_OPTIONS.

from __future__ import unicode_literals
import youtube_dl
import sys
import os
import threading
import time


DOWNLOAD_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '{}\\%(title)s.%(ext)s',#.format(DOWNLOAD_PATH),
    'nocheckcertificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def main():

    # < BDIKOT PARAMETRIM >
    if (len(sys.argv) != 3):
        sys.exit( "usage: <whatever_you_call_the_file>.exe <queue_file_path> <download_folder_path>" )
    else:
        QUEUE_FILE = sys.argv[1]
        DOWNLOAD_PATH = sys.argv[2]
        if (not os.path.isfile(QUEUE_FILE) and QUEUE_FILE.endswith(".txt")):
            sys.exit( "queue file does not exist, or is of wrong format :/" )
        if (not os.path.isdir(DOWNLOAD_PATH)):
            sys.exit( "download folder does not exist :/" )
    # END: < BDIKOT PARAMETRIM >

    # < ACCTUAL SCRIPT >
    DOWNLOAD_OPTIONS['outtmpl'] = DOWNLOAD_OPTIONS['outtmpl'].format(DOWNLOAD_PATH)
    dl = youtube_dl.YoutubeDL(DOWNLOAD_OPTIONS)

    # reading urls from file
    with open(QUEUE_FILE, 'r') as f:
        lines = f.readlines()

    threads = []
    # Loop starts downloading processes for all pending urls.
    for line in lines:

        # wait here while max threads are occupied,
        Tidx = 0
        while (len(threads) == 10):
            #print ("Max threads...")
            if (not threads[Tidx].is_alive()):
                threads.pop(Tidx)
                break
            Tidx = (Tidx + 1) % len(threads)
            time.sleep(50 / 1000)   # milliseconds
            
        # process start new theard
        threads.append(threading.Thread(target=dl.download, args=([line.strip(),],)))
        threads[-1].start()

    for t in threads:
        t.join()
    # END: < ACCTUAL SCRIPT >
    
if __name__ == '__main__':
    main()
