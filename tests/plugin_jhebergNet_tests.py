from nose.tools import *
import unittest
import os
import autodl.utils
import autodl.plugins.jhebergNet
from httmock import with_httmock, HTTMock
import mocks.jhebergNet
import requests
from mock import patch


def test_JhebergNet():
    plugin = autodl.plugins.jhebergNet.JhebergNet("/tmp/detail.html")

    assert_equal(plugin.url, "/tmp/detail.html")

@with_httmock(mocks.jhebergNet.homepage)
def test_get_homepage():
    plugin = autodl.plugins.jhebergNet.JhebergNet("http://jheberg.net/homepage.html")
    result = plugin.get_homepage()
    #print result

    assert_equal(result[0], '<html><body><div class="wrap"><a class="dl-button" href="/shoukugei-detail.html"></a></div></body></html>')
    assert_equal(result[1], {'csrftoken': 'bar'})

@with_httmock(mocks.jhebergNet.detailpage)
def test_get_detailpage():
    plugin = autodl.plugins.jhebergNet.JhebergNet("http://jheberg.net/detailpage.html")
    result = plugin.get_detailpage("http://jheberg.net/detail.html", { "csrftoken":"foobar"})
    #print result
    assert_equal(result, '<html><body><a class="hoster-thumbnail" href="/redirect/uplea"></a></body></html>')

@with_httmock(mocks.jhebergNet.homepage)
@patch('autodl.utils.get_activated_hosters')
def test_parse_homepage_for_detail_url(get_activated_hosters):
    plugin = autodl.plugins.jhebergNet.JhebergNet("http://jheberg.net/homepage.html")
    homepage = plugin.get_homepage()[0]
    #print homepage

    autodl.utils.get_activated_hosters.return_value = ['Uplea', '1fichier']
    result = plugin.parse_homepage_for_detail_url(homepage)
    #print result

    assert_equal(result, "http://jheberg.net/shoukugei-detail.html")

@with_httmock(mocks.jhebergNet.detailpage)
@patch('autodl.utils.get_activated_hosters')
def test_parse_detailpage_for_redirection_link(get_activated_hosters):
    plugin = autodl.plugins.jhebergNet.JhebergNet("http://jheberg.net/homepage.html")
    detailpage = plugin.get_detailpage("http://jheberg.net/detail.html", { "csrftoken":"foobar"})
    #print detailpage

    autodl.utils.get_activated_hosters.return_value = ['Uplea', '1fichier']
    result = plugin.parse_detailpage_for_redirection_link(detailpage)
    #print result
    assert_equal(result, ['http://jheberg.net/redirect/uplea'])

#TODO: find a way to test this method...
#@unittest.skip("Need to be able to test method get_hoster_link_from_redirection_url")
#@with_httmock(mocks.jhebergNet.redirectpage, mocks.jhebergNet.google_mock)
#def test_get_hoster_link_from_redirection_url():
#    s=requests.Session()
#    plugin = autodl.plugins.jhebergNet.JhebergNet("http://jheberg.net/homepage.html", s)
#    result = plugin.get_hoster_link_from_redirection_url(["http://jheberg.net/redirect/uplea"])
#    print result

#TODO
@unittest.skip("Need to be able to test method get_hoster_link_from_redirection_url")
@patch('autodl.utils.get_activated_hosters')
def test_get_links(get_activated_hosters):
    with HTTMock(mocks.jhebergNet.homepage):
        # call requests
        plugin = autodl.plugins.jhebergNet.JhebergNet("http://jheberg.net/homepage.html")
        homepage_data = plugin.get_homepage()
    #print homepage_data
    homepage_html = homepage_data[0]
    cookies = homepage_data[1]
    #print homepage_html, cookies
    detail_url = plugin.parse_homepage_for_detail_url(homepage_html)
    #print detail_url

    with HTTMock(mocks.jhebergNet.detailpage):
        detailpage = plugin.get_detailpage(detail_url, cookies)
        #print detailpage

    autodl.utils.get_activated_hosters.return_value = ['Uplea', '1fichier']
    redir_links = plugin.parse_detailpage_for_redirection_link(detailpage)
    print redir_links
