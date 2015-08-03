from nose.tools import *
import autodl.plugins.multiupOrg
import os
from mock import patch

def create_fake_homepage(tmp_file):
    with open(tmp_file, "w") as file_tmp:
        file_tmp.write('<html><body><a class="btn" href="/detail.html"></body></html>')

def create_fake_detailpage(tmp_file):
    with open(tmp_file, "w") as file_tmp:
        file_tmp.write('<html><body><a class="btn btn-small disabled link host" href="/success/uplea"></a></body></html>')

def delete_fake_file(tmp_file):
    os.remove(tmp_file)


def test_MultiupOrg():
    plugin = autodl.plugins.multiupOrg.MultiupOrg("/tmp/home.html")
    assert_equal(plugin.url, "/tmp/home.html")

def test_parse_homepage_for_detail_url():
    tmp_file = "/tmp/home.html"
    create_fake_homepage(tmp_file)
    
    raw_html = autodl.utils.get_webpage(tmp_file)

    plugin = autodl.plugins.multiupOrg.MultiupOrg(tmp_file)
    result = plugin.parse_homepage_for_detail_url(raw_html, baseurl="/tmp")
    #print result
    
    assert_equal(result, "/tmp/detail.html")

    delete_fake_file(tmp_file)


@patch('autodl.utils.get_activated_hosters')
def test_parse_detail_page_for_links(get_activated_hosters):
    tmp_file = "/tmp/detail.html"
    create_fake_detailpage(tmp_file)

    raw_html = autodl.utils.get_webpage(tmp_file)

    plugin = autodl.plugins.multiupOrg.MultiupOrg(tmp_file)

    autodl.utils.get_activated_hosters.return_value = ['Uplea', '1fichier']
    result = plugin.parse_detail_page_for_links(raw_html)

    assert_equal(result, ["/success/uplea"])

    delete_fake_file(tmp_file)


@patch('autodl.utils.get_activated_hosters')
def test_get_links(get_activated_hosters):
    tmp_file = "/tmp/download-home.html"
    tmp_file2 = "/tmp/detail.html"
    create_fake_homepage(tmp_file)
    create_fake_detailpage(tmp_file2)

    autodl.utils.get_activated_hosters.return_value = ['Uplea', '1fichier']
    plugin = autodl.plugins.multiupOrg.MultiupOrg(tmp_file)
    result = plugin.get_links(url=tmp_file)

    assert_equal(result, ["/success/uplea"])

    delete_fake_file(tmp_file)
    delete_fake_file(tmp_file2)
