# -*- coding: utf-8 -*-
"""
Basic log line parser.

Override for more features.

Created on Sat Jul 25 12:37:09 2015

@author: Marcus Povey
"""

import time
import re

class BasicParser(object):
    """ Basic LogLine Parser"""

    currentUser = ''

    def actionCallback(self, match):
        string = match.group(1)
        string = string.strip(" ")
        
        return "*%s %s*" % (self.currentUser, string)
    
    def parse(self, line):
        # Remove beginning :
        line = line.lstrip(":")
        
        # Username
        user = line;
        user = user.split("!", 1)[0]
        
        # Get body of text
        text = line[line.find('PRIVMSG'):]
        text = text[text.find(':')+1:]
        text = text.strip(" \t\n\r")
        
        # Look for actions
        
        self.currentUser = user
        text = re.sub('\x01ACTION (.*)\x01', self.actionCallback, text)
        self.currentUser = ''
        
        # Parse out string and format appropriately    (time, username, text)
        return "* <a href=\"#%s\" id=\"%s\">%s</a> - __[%s](https://github.com/%s)__: %s" % (time.strftime("%H:%M.%S"), time.strftime("%H:%M.%S"), time.strftime("%H:%M.%S (%Z)"), user, user, text)
     