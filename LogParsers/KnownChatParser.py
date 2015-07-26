# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:17:49 2015

Known Chat specific log line enhancements.

@author: Marcus Povey
"""

from BasicParser import BasicParser
import re

class KnownChatParser(BasicParser):    
    """ #Knownchat specific LogLine Parser"""
    
    def ticketCallback(self, match):
        string = match.group(0)
        project = 'idno/Known'
        number = string[string.find('#')+1:]
        
        if string[0] != '#':
            project = string[:string.find('#')]
            
        return "<a href=\"https://github.com/%s/issues/%s\">%s</a>" % (project, number, string)
            
            
    
    def parse(self, line):
        
        # Get the basic line
        line = super(KnownChatParser, self).parse(line)

        ##        
        # Now do some extra processing on it.
        ##

        # Tickets
        line = re.sub('([0-9a-zA-Z]+\/[0-9a-zA-Z]+)?#[0-9]+', self.ticketCallback, line)
        
        
        
        return line