import time
import _thread
import socket

from webpage import webpage
from spider import Spider, Command
from spidersettings import *

ipaddr = '0.0.0.0'
port = 8025

# =======================================================================================================
spider = Spider(POWERON, SPIDERDEBUG, WALKDEBUG, NUDGEDEBUG, PICODEBUG)
command = Command()
terminate = False

# =======================================================================================================
def spiderserver():
    global terminate, spider, command
    # Set up socket and start listening
    addr = socket.getaddrinfo(ipaddr, port)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen()
    print('server running, listening on', addr)

    # Main loop to listen for connections
    while not terminate:
        try:
            # wait, receive, and parse the request
            conn, addr = s.accept()
            try:
                cmd = str(conn.recv(1024))
                if cmd[:6] == "b'POST":
                    index = cmd.find("spider.")
                    cmd = cmd[index:-1]
                    if cmd == "spider.quit":
                        terminate = True
                        continue
                    elif cmd == "spider.halt=True":
                        exec(cmd)
                    else:
                        print(cmd)
                        command.set(cmd)
            except IndexError:
                pass

            # Send the HTTP response and close the connection
            conn.send(b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(webpage)
            conn.close()

        except OSError as e:
            conn.close()
            print(e, 'Connection closed')

    s.close()
    print("server loop terminated")

# =======================================================================================================
# when timing is good, do a nudge if spidermoving, always update the servos
def spidermoveloop():
    global terminate, spider
    print("move loop started")
    while not terminate:
        debug = spider.debug or spider.movedebug
        if spider.timing.iswriteready():
            if spider.spidermoving:
                spider.nudgecount += 1
                spider.spidermoving = sum([leg.nudgeleg() for leg in spider.legs])
                if not spider.spidermoving:
                    spider.movecompleted = True
                    if debug and spider.nudgecount:
                        spider.elapsedtime = time.time() - spider.elapsedtime
                        print("moved all legs {} nudges in {:.3f}S".format(spider.nudgecount, spider.elapsedtime))
                        spider.printstatus(False)
            spider.pico.writeallservos()

    print("move loop terminated")
    _thread.exit()

# =======================================================================================================
# runs on separate thread from serverloop, terminates on signal (runspider) from serverloop
def spidercontrolloop():
    global terminate, spider, command
    print("control loop started")
    spider.kickwatchdog()

    while not terminate:
        if command.commandpresent:
            try:
                raw = command.get()
                if raw:
                    exec(raw)
                    time.sleep(0.1)
                    print("command complete, enter new command")
                    spider.kickwatchdog()
            except Exception as e:
                print(e)
                pass
        spider.testpowerdown()
        spider.autorecentre()

    time.sleep(0.1)
    print("control loop terminated")
    _thread.exit()

# =======================================================================================================
# main routine
# start threads and then main (server) loop
_thread.start_new_thread(spidercontrolloop, ())
time.sleep(0.1)
_thread.start_new_thread(spidermoveloop, ())
time.sleep(0.1)
spiderserver()

# =======================================================================================================
