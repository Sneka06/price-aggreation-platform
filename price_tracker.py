import getopt
import os
import sys
import time

from price_tracker.constants import SAVE_PATH
from price_tracker.helpers import build_invoker
from price_tracker.mailer import Mailer
from price_tracker.web.web_server import run as web_server_runner

help_text = '''usage: price_tracker [init] | [-h]

Available Arguments
init open configuration page on web browser

-h  help
'''

# create save directory
os.makedirs(SAVE_PATH, exist_ok=True)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:", ['init'])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)
    for arg in args:
        if arg in 'init':
            web_server_runner()
            exit()
    for opt, arg in opts:
        if opt in '-h':
            print(help_text)
            sys.exit(1)

    run()


def run():
    mailer = Mailer()
    mailer.log_in()

    invoker = build_invoker(mailer)
    try:
        while not invoker.is_empty():
            invoker.execute()
            if invoker.is_empty():
                mailer.log_out()
                break
            time.sleep(60 * 60)
    except KeyboardInterrupt:
        mailer.log_out()
        print('')
        sys.exit(0)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('')
        sys.exit(0)
