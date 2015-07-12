from nose.tools import *
from autodl.plugins import *
import os
import autodl.utils
from mock import patch

def create_fake_homepage(tmp_file):
    with open(tmp_file, "w") as file_tmp:
        file_tmp.write('<html><body><section class="content"><h2><a href="/tmp/shoukugeki-detail.html"></a></h2></section><div class="num-NR">Episode 009</div></body></html>')

def create_fake_detailpage(tmp_file):
    with open(tmp_file, "w") as file_tmp:
        file_tmp.write('<html><body><tr><td class="table-links"><a href="/tmp/multiup-home.html"></a></td></tr></body></html>')

def create_fake_multiup_homepage(tmp_file):
    with open(tmp_file, "w") as file_tmp:
        file_tmp.write('<html><body><a class="btn" href="/detail.html"></body></html>')

def create_fake_multiup_detailpage(tmp_file):
    with open(tmp_file, "w") as file_tmp:
        file_tmp.write('<html><body><a class="btn btn-small disabled link host" href="/success/uplea"></a></body></html>')

def delete_fake_file(tmp_file):
    os.remove(tmp_file)


def test_mangaFrCom():
    plugin = autodl.plugins.mangaFrCom.MangaFrCom(["animes", "mangaFrCom", "shoukugeki", "9"])

    assert_equal(plugin.targets, ["animes", "mangaFrCom", "shoukugeki", "9"])
    assert_equal(plugin.url, "http://manga-fr.com/")

def test_parse_homepage_for_episodes():
    tmp_file = "/tmp/home.html"
    create_fake_homepage(tmp_file)

    raw_html = autodl.utils.get_webpage(tmp_file)
    #print raw_html

    plugin = autodl.plugins.mangaFrCom.MangaFrCom([{"target_type": "animes", 
        "lang": "vostfr", "res": "720p", "site": "mangaFrCom", 
        "title": "shoukugeki", "episode": "9"}])
    result = plugin.parse_homepage_for_episodes(raw_html, "shoukugeki", "9")
    #print result
    assert_equal(result, "/tmp/shoukugeki-detail.html")

    delete_fake_file(tmp_file)

def test_parse_detailpage_for_mirrors():
    tmp_file = "/tmp/shoukugeki-detail.html"
    create_fake_detailpage(tmp_file)

    raw_html = autodl.utils.get_webpage(tmp_file)
    print raw_html

    plugin = autodl.plugins.mangaFrCom.MangaFrCom([{"target_type": "animes", 
        "lang": "vostfr", "res": "720p", "site": "mangaFrCom", 
        "title": "shoukugeki", "episode": "9"}])
    result = plugin.parse_detailpage_for_mirrors(raw_html)
    print result
#    assert_equal(result, ['/tmp/multiup-home.html'])

    delete_fake_file(tmp_file)

@patch('autodl.utils.get_activated_hosters')
def test_parse_mirrors_for_links_multpiup(get_activated_hosters):
    tmp_file = "/tmp/multiup-home.html"
    tmp_file_detail = "/tmp/detail.html"
    create_fake_multiup_homepage(tmp_file)
    create_fake_multiup_detailpage(tmp_file_detail)

    raw_html = autodl.utils.get_webpage(tmp_file)
    #print raw_html

    plugin = autodl.plugins.mangaFrCom.MangaFrCom(["animes", "mangaFrCom", "shoukugeki", "9"])

    autodl.utils.get_activated_hosters.return_value = ['Uplea', '1fichier']
    result = plugin.parse_mirrors_for_links([tmp_file], baseurl="/tmp")
    #print result

    assert_equal(result, ['/success/uplea'])

    delete_fake_file(tmp_file)
    delete_fake_file(tmp_file_detail)

#TODO
def test_parse_mirrors_for_links_jheberg():
    pass

@patch('autodl.utils.get_activated_hosters')
def test_get_result_list(get_activated_hosters):
    tmp_file = "/tmp/home.html"
    tmp_file2 = "/tmp/shoukugeki-detail.html"
    tmp_file_multiup_home = "/tmp/multiup-home.html"
    tmp_file_multiup_detail = "/tmp/detail.html"
    create_fake_homepage(tmp_file)
    create_fake_detailpage(tmp_file2)
    create_fake_multiup_homepage(tmp_file_multiup_home)
    create_fake_multiup_detailpage(tmp_file_multiup_detail)

    plugin = autodl.plugins.mangaFrCom.MangaFrCom([{"target_type": "animes", 
        "lang": "vostfr", "res": "720p", "site": "mangaFrCom", 
        "title": "shoukugeki", "episode": "9"}], "/tmp/home.html")
    autodl.utils.get_activated_hosters.return_value = ['Uplea', '1fichier']
    links = plugin.get_result_list(test="test")
    print links
    assert_equal(links[0]["links"], ["/success/uplea"])

    plugin = autodl.plugins.mangaFrCom.MangaFrCom([{"target_type": "animes",
        "lang": "vostfr", "res": "720p", "site": "mangaFrCom",
        "title": "shoukugeki", "episode": None}], "/tmp/home.html")
    #print links
    assert_equal(links[0]["links"], ["/success/uplea"])


    delete_fake_file(tmp_file)
    delete_fake_file(tmp_file2)
    delete_fake_file(tmp_file_multiup_home)
    delete_fake_file(tmp_file_multiup_detail)
