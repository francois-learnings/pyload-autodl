"""
Mocks for the jheberg plugin tests.
"""


#from httmock import response, urlmatch


#NETLOC = r'(.*\.)?jheberg\.net$'
#HEADERS = {'content-type': 'text/plain'}
#GET = 'get'
#
#
#@urlmatch(netloc=NETLOC, path='/repos', method=GET)
#def homepage(url, request):
#    name = url.path.split('/')[-1]
#    content = { <html><body></body></html> }
#    
#    return response(200, content, HEADERS, None, 5, request)


from httmock import urlmatch, HTTMock, response
import requests

## define matcher:
#@urlmatch(netloc=r'(.*\.)?jheberg\.net(/\S*)?$')
#def homepage(url, request):
#        return '<html><body><div class="wrap"><a class="dl-button" href="/shoukugei-detail.html"></a></div></body></html>'
#
#@urlmatch(netloc=r'(.*\.)?jheberg\.net(/\S*)?$')
#def detailpage(url, request):
#        return '<html><body><tr><td class="table-links"><a href="/tmp/multiup-home.html"></a></td></tr></body></html>'
#

@urlmatch(netloc=r'(.*\.)?jheberg\.net(/\S*)?$')
def homepage(url, request):
    name = url.path.split('/')[-1]
    content = '<html><body><div class="wrap"><a class="dl-button" href="/shoukugei-detail.html"></a></div></body></html>'
    headers = {'content-type': 'texy/html',
               'Set-Cookie': 'csrftoken=bar;'}
    return response(200, content, headers, None, 5, request)

@urlmatch(netloc=r'(.*\.)?jheberg\.net(/\S*)?$')
def detailpage(url, request):
    name = url.path.split('/')[-1]
    content = '<html><body><a class="hoster-thumbnail" href="/redirect/uplea"></a></body></html>'
    headers = {'content-type': 'texy/html',
               'Set-Cookie': 'csrftoken=bar;'}
    return response(200, content, headers, None, 5, request)

#TODO: used to test the get_hoster_link_from_redirection_url method
#@urlmatch(netloc=r'(.*\.)?google\.com$', path=r'^/$')
#def google_mock(url, request):
#        return 'Hello from Google'
#
#@urlmatch(netloc=r'(.*\.)?jheberg\.net(/\S*)?$')
#def redirectpage(url, request):
#    return {'status_code': 302, 'headers': {'Location': 'http://google.com/'}}
