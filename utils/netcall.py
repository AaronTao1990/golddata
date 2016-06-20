# -*- coding: utf-8 -*-
import urllib2
import StringIO
import gzip
import logging
import sys

def uncompress(data):
    steram = StringIO.StringIO(data)
    gzipper = gzip.GzipFile(fileobj=stream)
    return gzipper.read()


def api_request(url, headers, body=None, timeout=5, use_proxy=False, proxy_addr=None):
    opener = None
    if use_proxy:
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy_addr}))
    else:
        opener = urllib2.build_opener(urllib2.BaseHandler())
    urllib2.install_opener(opener)

    #if body:
    #    if headers.get('Content-Type', None) == 'application/json':
    #        body = json.dumps(body)
    #    else:
    #        body = urllib.urlencode(body)
    request = urllib2.Request(url, body, headers)
    try:
        f = urllib2.urlopen(request, timeout=timeout)
        coding = f.info().get('Content-Encoding')
        if coding == 'gzip':
            result = uncompress(f.read())
        else:
            result = f.read()
    except Exception:
        #import traceback
        #logging.error('exception while trying to fetch url : %s, reason : %s' % (url, traceback.format_exc()))
        return None
    else:
        return result

def fetch_html(url, headers={}, body=None, timeout=10, retry_count=2, use_proxy=False, proxy_addr=None):
    for i in range(retry_count):
        resp = api_request(url, headers, body, timeout, use_proxy, proxy_addr)
        if resp:
            return resp
    return None

def main():
    url = sys.argv[1]
    body = '231312'
    html = fetch_html(url, body=body)
    print html

if __name__ == "__main__":
    main()

