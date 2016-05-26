import urllib
try:
    import urllib.request as urllib2
    from urllib.parse import urlencode
except ImportError:
    import urllib2
    from urllib import urlencode
    

def get_from_url(url, params):
    params = urlencode(params)
    res = urllib.urlopen("%s?%s" % (url, params))
    if res.getcode() == 200:
        page = res.read()
        return page
    else:
        raise Exception('get from url %s with return code %d' % (url, res.getcode()))


def post_to_url(url, params):
    params = urlencode(params).encode('utf8')
    request = urllib2.Request(url, params)
    res = urllib2.urlopen(request)
    if res.getcode() == 200:
        return res.read()
    else:
        raise Exception('post ot url %s with return code %d' % (url, res.getcode()))
