#!/usr/bin/python
###
# Simple IRC Log bot
###

import signal
import socket
import ssl
import sys
import time
import getopt
import os
import errno

server = "irc.freenode.net"
port = 6697
channel = ""
botnick = ""
logdir = "logs"
password = ""

irc_C = None
irc = None

def logline(line, logdir):
    
    filename = time.strftime("%Y-%m-%d") + ".md"
    
    # Remove beginning :
    line = line.lstrip(":")
    
    # Username
    user = line;
    user = user.split("!", 1)[0]
    
    # Get body of text
    text = line[line.find('PRIVMSG'):]
    text = text[text.find(':')+1:]
    text = text.strip(" \t\n\r");
    
    # Parse out string and format appropriately    (time, username, text)
    newline = "* %s - __[%s](https://github.com/%s)__: %s" % (time.strftime("%H:%M.%S (%Z)"), user, user, text)
    
    with open(logdir + "/" + filename, "a") as logfile:
        print "[LOGGING] " + newline
        logfile.write(newline + "\n")
        logfile.close()
        

def sig_int_handler(signal, frame):
    print("SIGINT: Shutting down nicely...")
    irc.send("QUIT (Botdeath)\r\n")
    sys.exit()

def send(command):
    global irc
    print "[SENT] " + command
    irc.send(command)
    
def usage():
    print("IRC Log bot by Marcus Povey <marcus@marcus-povey.co.uk>");
    print;
    print("Usage:");
    print("\t./bot -s server -p port -c channel -n nick -d logdirectory -a nickservpass");

def runbot(server, port, channel, botnick, logdir, password):
    global irc_C, irc
    
    irc_C = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    irc = ssl.wrap_socket(irc_C)
    
    print "Establishing connection to %s on %s:%d" % (channel, server, port)
    print "Logging to %s" % (logdir)
    
    # Connect
    irc.connect((server, port))
    irc.setblocking(False)
    send("USER " + botnick + " " + botnick + " bla :" + botnick + "\r\n")
    send("NICK " + botnick + "\r\n")
    if len(password) > 0:
        send("PRIVMSG NickServ :IDENTIFY "+ botnick + " " + password + "\r\n")    #auth
    send("JOIN " + channel + "\r\n")
    
    while True:
        time.sleep(1)
        	    
        try:
            for text in irc.makefile('r'):
            
                print "[RECEIVED] " + text.strip()
            
                # Prevent Timeout
                if text.find('PING') != -1:
                    send('PONG ' + text.split() [1] + '\r\n')
                    
                # Someone on IRC said something on the channel, so log it, and mayby parse it for meaning
                if text.find('PRIVMSG '+ channel) != -1:
                    logline(text, logdir)
        	    
        except Exception:
            continue

def main():
    global server
    global port
    global channel
    global botnick
    global logdir
    global password
    
    signal.signal(signal.SIGINT, sig_int_handler)
    
    try:
		opts, args = getopt.getopt(sys.argv[1:], "s:p:c:n:d:a:h", ["help"])
    except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit()

    for o, a in opts:
        if o == "-s":
            server = a
        elif o == "-p":
            port = int(a)
        elif o == "-c":
            channel = a
        elif o == "-n":
            botnick = a
        elif o == "-d":
            logdir = a
        elif o == "-a":
            password = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit()    
            
    # Check channel is defined
    if len(channel) == 0:
        usage()
        sys.exit()
        
    # Check nick is defined
    if len(botnick) == 0:
        usage()
        sys.exit()

    # Normalise log path and create dirs
    logdir = os.path.abspath(logdir) + "/" + channel
    try:
        os.makedirs(logdir)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(logdir):
            pass
        else: raise
    
    # Can't put # on command line, so add it
    channel = "#" + channel
    
    runbot(server, port, channel, botnick, logdir, password)

if __name__ == "__main__":
    main()
