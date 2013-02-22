#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import time
import os
import sys
import logging
try:    # Python 3
    import http.client as httpclient
    import urllib.parse as urllibparse
except: # Python 2
    import httplib as httpclient
    import urllib as urllibparse

params = dict(
    login_email="email", # replace with your email
    login_password="password", # replace with your password
    format="json",
    domain_id=100, # replace with your domain_od, can get it by API Domain.List
    record_id=100, # replace with your record_id, can get it by API Record.List
    sub_domain="www", # replace with your sub_domain
    record_line="默认",
)
current_ip = None

logfile = 'log.txt'
def initlog():
    logpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), logfile)
    logging.basicConfig(filename = logpath, format = '%(asctime)s - %(levelname)s: %(message)s', level = 'INFO')

def ddns(ip):
    params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httpclient.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllibparse.urlencode(params), headers)
    
    response = conn.getresponse()
    logging.info("Status: " + str(response.status) + ' ' + response.reason)
    data = response.read()
    logging.info("Response: " + data)
    conn.close()
    return response.status == 200

def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip

if __name__ == '__main__':
    initlog()
    while True:
        try:
            ip = getip()
            logging.info("IP: " + ip)
            if current_ip != ip:
                if ddns(ip):
                    current_ip = ip
        except Exception as e:
            logging.error(e)
            pass
        time.sleep(30)