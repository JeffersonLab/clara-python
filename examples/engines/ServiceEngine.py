from core.xMsgConstants import xMsgConstants
from src.util.ACEngine import ACEngine

__author__ = 'gurjyan'


class Engine1(ACEngine):
    def __init__(self):
        pass

    def execute(self, x):
        print "INPUT SERVICE .....> " + x.sender
        print "INPUT DATA    .....> " + x.BYTES
        x.BYTES = 'a' * 10
        return x

    def execute_group(self, x):
        print "MULTI-INPUT DATA .....> "
        for k in x:
            print "INPUT SERVICE    .....> " + k.sender
            print k.BYTES
        x[0].BYTES = 'm' * 10
        return x[0]

    def get_description(self):
        return "service engine1 description"

    def get_author(self):
        return "gurjyan"

    def get_version(self):
        pass

    def get_returned_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_states(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def configure(self, x):
        pass

    def dispose(self):
        pass


class Engine2(ACEngine):
    def execute(self, x):
        print "INPUT SERVICE .....> " + x.sender
        print "INPUT DATA    .....> " + x.BYTES
        x.STRING = 'b' * 10
        return x

    def execute_group(self, x):
        print "MULTI-INPUT DATA .....> "
        for k in x:
            print "INPUT SERVICE    .....> " + k.sender
            print k.BYTES
        x[0].BYTES = 'm' * 10
        return x[0]

    def get_description(self):
        return "service engine2 description"

    def get_author(self):
        pass

    def configure(self, x):
        pass

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def __init__(self):
        pass

    def dispose(self):
        pass


class Engine3(ACEngine):
    def execute(self, x):
        print "INPUT SERVICE .....> " + x.sender
        print "INPUT DATA    .....> " + x.BYTES
        x.BYTES = 'c' * 10
        return x

    def execute_group(self, x):
        print "MULTI-INPUT DATA .....> "
        for k in x:
            print "INPUT SERVICE    .....> " + k.sender
            print k.BYTES
        x[0].BYTES = 'm' * 10
        return x[0]

    def get_description(self):
        return "service engine3 description"

    def get_author(self):
        pass

    def configure(self, x):
        pass

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def __init__(self):
        pass

    def dispose(self):
        pass


class F1(ACEngine):

    f_content = ""
    c_count = 0

    def __init__(self):
        self.f_content = ""
        self.c_count = 0

    def execute(self, x):

        print "INPUT SERVICE .....> " + x.sender + " " + self.f_content
        if self.c_count < len(self.f_content):
            x.STRING = self.f_content[self.c_count]
            self.c_count += 1
        else:
            self.c_count = 0
            x.STRING = " "
        print "SENDING DATA = " + x.STRING
        return x

    def execute_group(self, x):
        pass

    def get_description(self):
        return "F1 description"

    def get_author(self):
        pass

    def configure(self, x):
        print "GOT CONFIGURE REQUEST"
        f = open(str(x.STRING), "r+b")
        self.f_content = f.readline()
        self.c_count = 0
        f.close()
        print "FILE CONTENT = "+self.f_content

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def dispose(self):
        pass


class F2(ACEngine):

    f_content = ""
    c_count = 0

    def __init__(self):
        self.f_content = ""
        self.c_count = 0

    def execute(self, x):

        print "INPUT SERVICE .....> " + x.sender + " " + self.f_content
        if self.c_count < len(self.f_content):
            x.STRING = self.f_content[self.c_count]
            self.c_count += 1
        else:
            self.c_count = 0
            x.STRING = " "
        print "SENDING DATA = "+x.STRING
        return x

    def execute_group(self, x):
        pass

    def get_description(self):
        return "F2 description"

    def get_author(self):
        pass

    def configure(self, x):
        print "GOT CONFIGURE REQUEST"
        f = open(str(x.STRING), "r+b")
        self.f_content = f.readline()
        self.c_count = 0
        f.close()
        print "FILE CONTENT = "+self.f_content

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def dispose(self):
        pass


class F3(ACEngine):

    f_content = ""
    c_count = 0

    def __init__(self):
        self.f_content = ""
        self.c_count = 0

    def execute(self, x):

        print "INPUT SERVICE .....> " + x.sender + " " + self.f_content
        if self.c_count < len(self.f_content):
            x.STRING = self.f_content[self.c_count]
            self.c_count += 1
        else:
            self.c_count = 0
            x.STRING = " "
        print "SENDING DATA = "+x.STRING
        return x

    def execute_group(self, x):
        pass

    def get_description(self):
        return "F3 description"

    def get_author(self):
        pass

    def configure(self, x):
        print "GOT CONFIGURE REQUEST"
        f = open(str(x.STRING), "r+b")
        self.f_content = f.readline()
        self.c_count = 0
        f.close()
        print "FILE CONTENT = " + self.f_content

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def dispose(self):
        pass


class F4(ACEngine):

    f_content = ""
    c_count = 0

    def __init__(self):
        self.f_content = ""
        self.c_count = 0

    def execute(self, x):

        print "INPUT SERVICE .....> " + x.sender + " " + self.f_content
        if self.c_count < len(self.f_content):
            x.STRING = self.f_content[self.c_count]
            self.c_count += 1
        else:
            self.c_count = 0
            x.STRING = " "
        print "SENDING DATA = "+x.STRING
        return x

    def execute_group(self, x):
        pass

    def get_description(self):
        return "F4 description"

    def get_author(self):
        pass

    def configure(self, x):
        print "GOT CONFIGURE REQUEST"
        f = open(str(x.STRING), "r+b")
        self.f_content = f.readline()
        self.c_count = 0
        f.close()
        print "FILE CONTENT = "+self.f_content

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def dispose(self):
        pass


class EB(ACEngine):

    f_content = xMsgConstants.UNDEFINED
    c_count = 0

    def execute(self, x):
        pass

    def execute_group(self, x):
        print "MULTI-INPUT DATA .....> "
        d = ["", "", "", ""]
        for k in x:
            if "F1" in k.sender:
                d[0] = k.STRING
            elif "F2" in k.sender:
                d[1] = k.STRING
            elif "F3" in k.sender:
                d[2] = k.STRING
            elif "F4" in k.sender:
                d[3] = k.STRING
        s = ""
        for y in d:
            s += y
        x[0].STRING = s
        return x[0]

    def get_description(self):
        return "Event Builder"

    def get_author(self):
        pass

    def configure(self, x):
        f = open(str(x.STRING), "r+b")
        self.f_content = f.readline()
        f.close()

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def __init__(self):
        pass

    def dispose(self):
        pass


class R(ACEngine):

    result = ""

    def execute(self, x):
        self.result = self.result + x.STRING
        print self.result
        return x

    def execute_group(self, x):
        pass

    def get_description(self):
        return "R description"

    def get_author(self):
        pass

    def configure(self, x):
        print "GOT CONFIGURE REQUEST"
        self.result = ""

    def get_returned_data_type(self, x):
        pass

    def get_accepted_data_type(self, x):
        pass

    def get_current_state(self, x):
        pass

    def get_version(self):
        pass

    def get_states(self, x):
        pass

    def __init__(self):
        pass

    def dispose(self):
        pass


