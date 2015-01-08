import time
import signal
from xsys.xMsgNode import xMsgNode

__author__ = 'gurjyan'


class Dpe():

    def __init__(self):
        pass

    @staticmethod
    def start():
        """Clara DPE
        """
        xn = xMsgNode()

        print "================================"
        print "           CLARA Dpe "
        print "================================"
        print "lang = Python"
        print "date = " + time.strftime("%c")
        print "host = " + xn.host

        signal.signal(signal.SIGTERM, xn.exit_gracefully)
        signal.signal(signal.SIGINT, xn.exit_gracefully)


def main():
    dpe = Dpe()
    dpe.start()

if __name__ == '__main__':
    main()
