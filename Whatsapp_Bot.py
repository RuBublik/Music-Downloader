# Imports
import re
import Queue
import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Constants
WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'
BOT_CONTACT = '//span[@title = "MusicBot"]'
MESSAGE_BOX = 'div._2S1VP.copyable-text.selectable-text'
OUT_CLASS = 'message-out'
SESSION_TERMINATOR_REP = 'shutting down...'
SESSION_TERMINATOR_MSG = 'mischief managed'
URL_EXPRESSION = r'https://youtu.be/.{4}-.{6}'
SHUTDOWN_VALUE = -1
IGNORE_VALUE = -2


def reply_text(msg):
    """Function sends a given text message to the chat."""
    global driver
    msg_box = driver.find_element_by_css_selector(MESSAGE_BOX)
    msg_box.send_keys(msg)
    msg_box.send_keys(Keys.RETURN)


def get_message_at(idx=-1):
    """Function returns the message at given idx, last by default"""
    global driver
    last = driver.find_elements_by_class_name(OUT_CLASS)[idx].text
    lm_text, lm_time = last.split("\n")

    # Retuens NONE if no new messages were sent.
    if lm_text == SESSION_TERMINATOR_REP:
        return None, lm_time

    # --V  Might server for later refinements  V--
    # Returns TERMINATION VALUE if this is my will.
    elif lm_text == SESSION_TERMINATOR_MSG:
        return SHUTDOWN_VALUE, lm_time

    # Finnally, returns urls or junk (which is filtered later).
    return lm_text, lm_time


def is_url(lm_text):
    """Function returns boolian value if given text is url. (to simplify the view)"""
    return re.match(URL_EXPRESSION, lm_text)


def catch_up():
    """Function returs list of all the messages that were sent while the bot was down."""
    idx = -1
    pending = []
    lm_text, lm_time = get_message_at(idx)

    # Loop appends pending urls (if any) until reaches last SESSION_TERMINATOR_REP.
    while lm_text:
        if is_url(lm_text):
            print lm_text
            pending.append(lm_text)
        idx -= 1
    return pending


def main():
    global driver
    driver = webdriver.Chrome()
    driver.get(WHATSAPP_WEB_URL)

    # Lets user scan the QR code:
    raw_input('press ENTER when ready')

    # Clicks on BOT contact:
    driver.find_element_by_xpath(BOT_CONTACT).click()
    print 'BOT: I pledge myself to your teachings'

    # Restores relevant unread messages:
    pending = catch_up()
    for i in pending:
        print i

    # Main loop
    while lm_text != SESSION_TERMINATOR_MSG:

        # Not appropriate lm_text are returned None.
        if is_url(lm_text):
            print lm_text
        last_message = get_message_at()

    # Quit acknowledge:
    reply_text(SESSION_TERMINATOR_REP)
    print 'mischief managed'

    # Closes driver gracefully.
    driver.close()


if __name__ == '__main__':
    main()

# TODO:
# consider quit during catch_up
