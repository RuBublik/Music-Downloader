# imports
from __future__ import unicode_literals
import youtube_dl
import os

# Contants
QUEUE_FILE = 'download_queue.txt'
DOWNLOAD_PATH = r'D:\\Elik\\MUSIC'
DEBUG_TEMPL = """
--------------------

songs dowloaded:\t{0}/{1}
dirs created:\t\t{2}
files arranged:\t\t{3}/{4}

--------------------

failed links:
\t{5}

files require attention:
\t{6}
"""


def main():

    # initiallizing counters and stuff...
    success_dl = 0
    failed_urls = []
    mkdir_cntr = 0
    failed_songs = []
    handled_cntr = 0


# =========
# DOWNLOAD:
# =========

    # setting download options:
    download_options = {
        'format': 'bestaudio/best',
        'outtmpl': '{}\\%(title)s.%(ext)s'.format(DOWNLOAD_PATH),
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # getting urls from file:
    with open(QUEUE_FILE, 'r') as f:
        song_urls = f.readlines()

    # downloading songs:
    with youtube_dl.YoutubeDL(download_options) as dl:
        for url in song_urls:
            try:

                # might raise an exception if url is not a single video but a play-list.
                dl.download([url])
                success_dl += 1
            except:
                failed_urls.append(url)

    # clearing the queue file:
    f = open(QUEUE_FILE, 'w')
    f.close()


# =========
# Arrange:
# =========

    # for easier acces to files:
    os.chdir(DOWNLOAD_PATH)

    # lists only (unsorted) files in ROOT:
    only_files = [song for song in os.listdir(
        DOWNLOAD_PATH) if not os.path.isdir(song)]

    # loop for arranging files in folders:
    for song_file in only_files:
        try:

            # might raise an exception if file's name is not like:
            # [band/singer] - [song name].mp3
            band_dir = song_file.split(' -')[0]

            # if band directory does not exist:
            if not os.path.isdir(band_dir):
                os.mkdir(band_dir)
                mkdir_cntr += 1

            #                                                    _        _
            # renaming file's full name acctually moves the file  \_(ツ)_/
            #
            os.rename(os.path.join(DOWNLOAD_PATH, song_file),
                      os.path.join(band_dir, song_file))
            handled_cntr += 1
        except:
            failed_songs.append(song_file)

    # Pretty prints:
    print DEBUG_TEMPL.format(success_dl,
                             len(song_urls),
                             mkdir_cntr,
                             handled_cntr,
                             len(only_files),
                             '\r\n\t'.join(
                                 failed_urls) if failed_urls else '*',
                             '\r\n\t'.join(failed_songs) if failed_songs else '*')

    # lets user see debug output:
    raw_input('--------------------')


if __name__ == '__main__':
    main()
