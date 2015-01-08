import time
import signal
from xsys.xMsgFE import xMsgFE

__author__ = 'gurjyan'


class Platform():

    def __init__(self):
        pass

    @staticmethod
    def start():
        """Clara DPE
        """
        xn = xMsgFE()

        print "================================"
        print "      CLARA Cloud Manager       "
        print "================================"
        print "lang = Python"
        print "date = " + time.strftime("%c")

        signal.signal(signal.SIGTERM, xn.exit_gracefully)
        signal.signal(signal.SIGINT, xn.exit_gracefully)


def main():
    dpe = Platform()
    dpe.start()

if __name__ == '__main__':
    main()
