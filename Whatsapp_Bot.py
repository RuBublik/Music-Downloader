from __future__ import unicode_literals

# Imports
import os
import re
import threading

import youtube_dl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Constants
WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'
BOT_CONTACT = '//span[@title="MusicBot"]'
MESSAGE_BOX = 'div._2S1VP.copyable-text.selectable-text'
OUT_CLASS = 'message-out'
TEXT_CLASS = 'ZhF0n'
TERMINATION_REP = 'shutting down...'
KILL_SWITCH = 'mischief managed'
URL_EXPRESSION = r'https://youtu.be/.+'
SHUTDOWN_VALUE = '-1'
IGNORE_VALUE = '-2'
LAST_TREATED_FILE = 'shit.txt'
DOWNLOAD_PATH = r'D:\\Desktop\\MUSIC'
DOWNLOAD_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '{}\\%(title)s.%(ext)s'.format(DOWNLOAD_PATH),
    'nocheckcertificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


class WhatsappBot:
    def __init__(self):
        """ hrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options) """
        self.driver = webdriver.Chrome()
        self.driver.get(WHATSAPP_WEB_URL)
        self.dl = youtube_dl.YoutubeDL(DOWNLOAD_OPTIONS)
        self.download_threads = []

    def prepare_browser(self):
        """Function finds html elements in whatsapp-web page and proceeds to chat."""
        self.driver.find_element_by_xpath(BOT_CONTACT).click()
        self.msg_box = self.driver.find_element_by_css_selector(MESSAGE_BOX)

    def quit_session(self):
        """Function acknowledges quiting by sending text message to the chat.
        Also closes driver gracefully and wait for downloading threads to close."""
        self.msg_box.send_keys(TERMINATION_REP)
        self.msg_box.send_keys(Keys.RETURN)
        self.driver.close()
        for i in self.download_threads:
            if i:
                i.join()

    def is_url(self, lm_text):
        """Function returns boolian value if given text is url."""
        if not lm_text:
            return False
        return re.match(URL_EXPRESSION, lm_text)

    def get_message_at(self, idx=-1):
        """Function returns the message at given idx, last by default"""
        last = self.driver.find_elements_by_class_name(TEXT_CLASS)[idx].text
        lm_text = str(last)

        # Retuens NONE if no new messages were sent.
        if lm_text == TERMINATION_REP:
            return None

        # Causes bot to SHUTDOWN if this is my will.
        elif lm_text == KILL_SWITCH:
            return SHUTDOWN_VALUE

        # Finnally, returns urls or junk (which is filtered later).
        return lm_text

    def catch_up(self):
        """Function restores relevant unread messages that were sent while the bot was
        down, if any. (until last - KILL_SWITCH / reply)
        """
        idx = -1
        pending = []
        lm_text = self.get_message_at(idx)

        # If there are unread messages (lm_text is not None):
        if lm_text:

            # Updates last treated url, file:
            with open(LAST_TREATED_FILE, 'w') as f:
                f.write(lm_text)

            # Loop starts downloading processes for all pending urls.
            while lm_text:
                if self.is_url(lm_text):
                    t = threading.Thread(
                            target=self._download_song, args=(lm_text,))
                    self.download_threads.append(t)
                    t.start()
                idx -= 1
                lm_text = self.get_message_at(idx)

    def assign_download(self, url):
        """Funciton starts downloading process and updates the LAST_TREATED_FILE."""
        t = threading.Thread(target=self._download_song, args=(url,))
        self.download_threads.append(t)
        t.start()
        with open(LAST_TREATED_FILE, 'w') as f:
            f.write(url)

    def _download_song(self, url):
        """Target of assign_download, downloads the sond with youtube_dl."""
        try:

            # might raise an exception if url is not a single video but a play-list.
            # or, if the song already exists.
            self.dl.download([url])
        except:
            print 'defective url -> ' + url


def main():
    bot = WhatsappBot()

    # Lets user scan the QR code:
    raw_input('press ENTER when ready')
    bot.prepare_browser()
    print 'BOT: I pledge myself to your teachings'

    # restores unread urls:
    bot.catch_up()

    # Restores last treated url from file:
    with open(LAST_TREATED_FILE, 'r') as f:
        lt_text = f.read()

    # Main loop
    lm_text = bot.get_message_at()
    while lm_text != SHUTDOWN_VALUE:

        # Not appropriate lm_text are returned None.
        if bot.is_url(lm_text) and lm_text != lt_text:
            lt_text = lm_text
            bot.assign_download(lm_text)
        lm_text = bot.get_message_at()

    # Quit acknowledge:
    bot.quit_session()
    print 'mischief managed'


if __name__ == '__main__':
    main()
