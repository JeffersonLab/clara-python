import time
import signal
from core.xMsgUtil import xMsgUtil
from xsys.xMsgNode import xMsgNode

__author__ = 'gurjyan'


class Dpe():

    def __init__(self):
        pass

    @staticmethod
    def start():
        """Clara DPE
        """
        print " ================================"
        print "           CLARA DPE "
        print " ================================"
        print " Binding = Python"
        print " Date = " + time.strftime("%c")
        print " Host = " + xMsgUtil.get_local_ip()
        print " ================================"

        xn = xMsgNode()
        signal.signal(signal.SIGTERM, xn.exit_gracefully)
        signal.signal(signal.SIGINT, xn.exit_gracefully)
        xn.join()

def main():
    dpe = Dpe()
    dpe.start()

if __name__ == '__main__':
    main()
