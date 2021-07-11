#!/usr/bin/env python3

import os
import argparse
import urllib.request
import socket
import datetime

# variables
cfg = {}
cfg['host'] = 'localhost'
cfg['port'] = '8123'
cfg['user'] = 'default'
cfg['password'] = ''
cfg['timeout'] = 0.01

urls = [ # urls to ping for healtcheck
    '/ping',
    '/replicas_status'
]

tt = {} # for measuring time on calls

# end variables

# functions
def parse_args ():
    parser = argparse.ArgumentParser (
        description = "Basic check for ClickHouse health (uses HTTP interface)",
        usage = "%(prog)s"
    )
    parser.add_argument ("--host", help="ClickHouse host", default=cfg['host'])
    parser.add_argument ("--port", help="ClickHouse port", default=cfg['port'])
    parser.add_argument ("--user", help="ClickHouse user", default=cfg['user'])
    parser.add_argument ("--password", help="ClickHouse password", default=cfg['password'])
    parser.add_argument ("--timeout", help="Connection timeout", default=cfg['timeout'])

    args = parser.parse_args()
    if args.host is not None:
        cfg['host'] = args.host
    if args.port is not None:
        cfg['port'] = args.port
    if args.user is not None:
        cfg['user'] = args.user
    if args.password is not None:
        cfg['password'] = args.password
    if args.timeout is not None:
        cfg['timeout'] = args.timeout

def TT (s = ''):
    if tt.get(s) is None: # if key doesn't exist, means that the first call (start)
        tt[s] = datetime.datetime.now()
    else: # calculate time diff (end)
        tt[s] = (datetime.datetime.now() - tt[s]).total_seconds()

if __name__ == "__main__":
    parse_args()
    socket.setdefaulttimeout(cfg['timeout'])

    for path in urls:
        url = "http://" + cfg['host'] + ":" + cfg['port'] + path
        req = urllib.request.Request(url)
        req.add_header('X-ClickHouse-User', cfg['user'])
        req.add_header('X-ClickHouse-Key', cfg['password'])

        TT(path)
        try:
            r = urllib.request.urlopen(req, timeout=cfg['timeout'])
        except urllib.error.HTTPError as err:
            print(url + " : Error code: " + str(err.code) + ", Reason: " + str(err.reason))
            exit(2)
        except urllib.error.URLError as e:
            print(url + " : Error: " + str(e.reason))
            exit(2)
        except socket.error as e:
            print ("Socket error " + url)
            exit(2)
        except Exception as e:
            print ("Unknown error: {}",format(e).rstrip())
            exit(2)

        data = r.read().decode('utf-8').strip()
        TT(path)
        print ("{} {} req/time {} sec".format(path, data, tt[path]), end=" ")
    print()
