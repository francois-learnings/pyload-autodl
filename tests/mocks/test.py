from httmock import urlmatch, HTTMock, with_httmock
import requests
import jhebergNet

# open context to patch
with HTTMock(jhebergNet.homepage):
    # call requests
    r = requests.get('http://jheberg.net/homepage.html')
print r.content

with HTTMock(jhebergNet.detailpage):
    # call requests
    r = requests.get('http://jheberg.net/detailpage.html')
print r.content


@with_httmock(jhebergNet.testpage)
def test_mock():
    r = requests.get('http://jheberg.net/detailpage.html')
    return r


raw_html = test_mock()
print raw_html.content

