import StringIO
import gzip

__author__ = 'rmj'

import urllib
import urllib2

header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29'}

RENDER_PROXY = 'http://haproxy.crawler.yidian.com:9000'


def download(url, headers=None, proxy=None, data=None):
    if proxy:
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxy}))
    else:
        opener = urllib2.build_opener(urllib2.HTTPHandler())

    hs = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    if headers:
        hs.update(headers)

    encode_data = None
    if data:
        data = __convert_unicode_to_str(data)
        encode_data = urllib.urlencode(data, doseq=True)

    req = urllib2.Request(url, data=encode_data, headers=hs)
    resp = opener.open(req)
    encoding = resp.headers.get('Content-Encoding')
    if encoding == 'gzip':
        compresseddata = resp.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()
    else:
        data = resp.read()
    return data


def __is_unicode(v):
    return isinstance(v, unicode)


def __convert_to_str(v):
    if __is_unicode(v):
        return v.encode('utf-8')
    return v


def __convert_unicode_to_str(data):
    if data:
        new_data = {}
        for k, v in data.items():
            new_data[__convert_to_str(k)] = __convert_to_str(v)
        return new_data
    return data



