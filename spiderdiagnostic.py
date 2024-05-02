from spidersettings import *

class Diagnostic(object):

    def __init__(self, spider):
        self.spider = spider

    def jointtuning(self):
        leg = 0
        joint = 0
        value = 1500
        while True:
            s = input("=, -, > X: ")
            if s == '=':
                value += 10
                print("leg {}, joint {}, value {}".format(leg, joint, value))
                self.spider.legjointservo(leg, joint, value)
            if s == '-':
                value -= 10
                print("leg {}, joint {}, value {}".format(leg, joint, value))
                self.spider.legjointservo(leg, joint, value)
            if s == '>':
                joint = (joint + 1) % 3
                if not joint:
                    leg = (leg + 1) % 6
                value = self.spider.servotimes[leg][joint]
                print("select leg {}, joint {}, value is {}".format(leg, joint, value))
            if s == 'X':
                break

    def cartesian(self, legnumber):
        while True:
            leg = self.spider.legs[legnumber]
            s = input("input [x, y, z]: ")
            if len(s) < 2:
                break
            leg.foottarget = [int(n) for n in s.split()]
            leg.computeservos()
            self.spider.sendservobytestream()

    def execute(self):
        while True:
            try:
                exec(input("> "))
            except:
                print("error")
                pass

    # set all servo positions to servo nominal midpoints
    def set1500(self):
        self.spider.servotimes = [[1500, 1500, 1500] for _ in self.spider.legs]
        print(self.spider.servotimes)
        self.spider.pico.writeallservos()

    # set all servos to their centre positions
    def setcentre(self):
        self.spider.servotimes = CENTRES
        print(self.spider.servotimes)
        self.spider.pico.writeallservos()

    # set a particular leg's joint servo
    def setlegjointservo(self, legnumber, jointnumber, value):
        self.spider.servotimes[legnumber][jointnumber] = value
        print(self.spider.servotimes)
        self.spider.pico.writeallservos()

