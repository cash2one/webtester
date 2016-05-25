import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

def get_from_url(url, params):
    params = urllib.urlencode(params)
    res = urllib.urlopen("%s?%s" % (url, params))
    if res.getcode() == 200:
        page = res.read()
        return page
    else:
        raise Exception('get from url %s with return code %d' % (url, res.getcode()))


def post_to_url(url, params):
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    res = urllib2.urlopen(request)
    if res.getcode() == 200:
        return res.read()
    else:
        raise Exception('post ot url %s with return code %d' % (url, res.getcode()))
