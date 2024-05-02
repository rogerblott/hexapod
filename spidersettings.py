try:
    from micropython import const
    makeconst = False
except:
    def const(arg):
        return arg

ssid = 'Kronk'
password = 'karotnik'

# ------------------------------------------------------------------------------------

TRIPODWALK = const(0)
WAVEWALK = const(1)

POWERDOWNTIMEOUT = const(60)
RECENTRETIMEOUT = const(15)

# ------------------------------------------------------------------------------------
SPIDERDEBUG = True
WALKDEBUG = True
NUDGEDEBUG = False
PICODEBUG = False

UNFREQ = const(150000000)
BASEFREQ = const(125000000)

PICOADDR = const(0x20)
I2CCHANNEL = const(0)
I2CCLOCKSPEED = const(400000)

TIMINGPIN = const(4)
RELAYPIN = const(27)

# ------------------------------------------------------------------------------------
TOTALLEGS = const(6)
JOINTSPERLEG = const(3)
TOTALJOINTS = const(18)
TOTALSERVOS = const(21)

LEG0BASEADDR = const(0)
LEG3BASEADDR = const(18)

POWERON = const(1)
POWEROFF = const(0)

HIP = const(0)
KNEE = const(1)
ANKLE = const(2)

HIP0 = (-70, 90, 0)
HIP1 = (-100, 0, 0)
HIP2 = (-70, -90, 0)
HIP3 = (70, 90, 0)
HIP4 = (100, 0, 0)
HIP5 = (70, -90, 0)

LEG0ACTIVE = const(True)
LEG1ACTIVE = const(True)
LEG2ACTIVE = const(True)
LEG3ACTIVE = const(True)
LEG4ACTIVE = const(True)
LEG5ACTIVE = const(True)

SERVOOFFSETHIP0 = 2.35
SERVOOFFSETHIP1 = 3.14
SERVOOFFSETHIP2 = -2.35
SERVOOFFSETHIP3 = 0.78
SERVOOFFSETHIP4 = 0.00
SERVOOFFSETHIP5 = -0.78
SERVOOFFSETKNEE = 0
SERVOOFFSETANKLE = -1.57

FEMURLENGTH = const(55)
TIBIALENGTH = const(65)
FOOTLENGTH = const(85)

SERVOMAX = const(2300)
SERVOMIN = const(700)
USECPERRAD = const(636)

MAXHIPHEIGHT = const(50)
MINHIPHEIGHT = const(-50)
ZSIT = const(-70)
ZSTAND = const(-110)
LIFTDISTANCE = const(25)

LIFT = const(True)
NOLIFT = const(False)
ROTATE = const(True)
NOROTATE = const(0)
ROTATELEFT = const(1)
ROTATERIGHT = const(-1)
MAXROTATEANGLE = 0.524
NOLATERAL = [0, 0, 0]

LIFTNUDGES = const(5)
MINNUDGES = const(2 * LIFTNUDGES)
STDNUDGES = const(20)
SITNUDGES = const(15)
STANDNUDGES = const(15)
STDWALKNUDGES = const(20)
STEPDISTANCE = const(100)
STEPANGLE = 0.524  # 30 degrees

INITFOOT0REL = (-70, 70, -50)
INITFOOT1REL = (-90, 0, -50)
INITFOOT2REL = (-70, -70, -50)
INITFOOT3REL = (70, 70, -50)
INITFOOT4REL = (90, 0, -50)
INITFOOT5REL = (70, -70, -50)

CENTRE0 = [1500, 1550, 1600]
CENTRE1 = [1500, 1580, 1580]
CENTRE2 = [1500, 1590, 1470]
CENTRE3 = [1500, 1580, 1480]
CENTRE4 = [1500, 1520, 1560]
CENTRE5 = [1500, 1490, 1490]
CENTRES = [CENTRE0, CENTRE1, CENTRE2, CENTRE3, CENTRE4, CENTRE5]

def intvec(anylist):
    result = []
    for item in anylist:
        if isinstance(item, list):
            result.append(invec(item))
        else:
            result.append(round(item))
    return result
