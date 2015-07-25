# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:17:49 2015

Known Chat specific log line enhancements.

@author: Marcus Povey
"""

from BasicParser import BasicParser

class KnownChatParser(BasicParser):    
    """ #Knownchat specific LogLine Parser"""
    
    def parse(self, line):
        
        line = super(KnownChatParser, self).parse(line)
        
        return line