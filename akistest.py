# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:00:24 2017
Test akismet
@author: lenovo
"""

import akismet

defaultkey = "YOURKEYHERE"

pageurl="http://yourkeyhere.com"

defaultagent = "Mozilla/5.0 (Windows; U; Windows NT 5.1;en-US; rv:1.8.0.7)"
defaultagent += "Gecko/20060909 Firefox/1.5.0.7"

def isspam(comment,author,ipaddress,agent=defaultagent,apikey=defaultkey):
    try:
        valid = akismet.verify_key(apikey,pageurl)
        if valid:
            return akismet.comment_check(apikey,pageurl,
                                         ipaddress,agent,comment_content=comment,
                                         comment_author_email=author,comment_type="comment")
        else:
            print 'Invalid key'
            return False
    except akismet.AkismetError as e:
        print e.response, e.statuscode
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    