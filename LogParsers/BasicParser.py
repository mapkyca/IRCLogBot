# -*- coding: utf-8 -*-
"""
Basic log line parser.

Override for more features.

Created on Sat Jul 25 12:37:09 2015

@author: Marcus Povey
"""

import time

class BasicParser:
    """ Basic LogLine Parser"""
    
    def parse(self, line):
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
        return "* %s - __[%s](https://github.com/%s)__: %s" % (time.strftime("%H:%M.%S (%Z)"), user, user, text)
     