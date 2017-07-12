#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib, urllib2, sys
import ssl
import json
def access_token():
    return token().access_token()
class token:
    access_token=None
    def __init__(self,client_id="hbFpUq7qMOGYQVCDpLjcsAR7",
                 client_secret="HyexuFgDqurUuoEYm2NWehmDGvyjo17o"):
        self.client_id=client_id
        self.client_secret=client_secret
            
    def access_token(self):
        host = ('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'+
            "&client_id="+self.client_id+
           "&client_secret="+self.client_secret)
        request = urllib2.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib2.urlopen(request, context=ctx)
        content = response.read()
        print type(content)
        if (content):
            print(content)
        access_token = json.loads(content)['access_token']
        return access_token
    
if __name__ == "__main__":
    token = token()
    print token.access_token()
