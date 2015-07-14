from nose.tools import assert_equal
import unittest
import os
import autodl.utils
from mock import patch


class TestMangaFrCom(unittest.TestCase):

    def setUp(self):
        # Fake homepage
        self.homepage = "/tmp/homepage_tmp.html"
        with open(self.homepage, "w") as file_tmp:
            file_tmp.write('<html><body><section class="content"><h2>'
                           '<a href="/tmp/shoukugeki-detail.html"></a></h2>'
                           '</section><div class="num-NR">Episode 009</div>'
                           '</body></html>')

        # Fake detail page
        self.detailpage = "/tmp/detailpage_tmp.html"
        with open(self.detailpage, "w") as file_tmp:
            file_tmp.write('<html><body><section><article><table>'
                           '<tbody><tr><td></td><td>720p</td></tr>'
                           '<tr><td class="table-links">'
                           '<a href="/tmp/multiup-720p-home.html"></a></td>'
                           '</tr></tbody></table>'
                           '<table><tbody><tr><td></td><td>1080p</td></tr>'
                           '<tr><td class="table-links">'
                           '<a href="/tmp/multiup-1080p-home.html"></a></td>'
                           '</tr></body></html>')

        # Fake multiup Homepage
        self.multiup_homepage = "/tmp/multiup_homepage_tmp.html"
        with open(self.multiup_homepage, "w") as file_tmp:
            file_tmp.write('<html><body><a class="btn" href="/detail.html">'
                           '</body></html>')

        # Fake multiup Detailpage
        self.multiup_detailpage = "/tmp/multiup_detailpage_tmp.html"
        with open(self.multiup_detailpage, "w") as file_tmp:
            file_tmp.write('<html><body>'
                           '<a class="btn btn-small disabled link host"'
                           'href="/success/uplea"></a></body></html>')

    def tearDown(self):
        os.remove(self.homepage)
        os.remove(self.detailpage)
        os.remove(self.multiup_homepage)
        os.remove(self.multiup_detailpage)

    def test_init(self):
        plugin = autodl.plugins.mangaFrCom.MangaFrCom([{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangaFrCom",
            "title": "shoukugeki",
            "episode": "9"}])

        assert_equal(plugin.targets, [{
                     "target_type": "animes",
                     "lang": "vostfr",
                     "res": "720p",
                     "site": "mangaFrCom",
                     "title": "shoukugeki",
                     "episode": "9"}])
        assert_equal(plugin.url, "http://manga-fr.com/")

    def test_parse_homepage_for_episodes(self):
        raw_html = autodl.utils.get_webpage(self.homepage)
        # print raw_html

        plugin = autodl.plugins.mangaFrCom.MangaFrCom([{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangaFrCom",
            "title": "shoukugeki",
            "episode": "9"}])

        result = plugin.parse_homepage_for_episodes(raw_html,
                                                    "shoukugeki",
                                                    "9")
        # print result

        assert_equal(result, "/tmp/shoukugeki-detail.html")

        # Test with no result for title
        result = plugin.parse_homepage_for_episodes(raw_html,
                                                    "shingeki",
                                                    "9")
        # print result
        assert_equal(result, None)

    def test_parse_detailpage_for_mirrors(self):
        raw_html = autodl.utils.get_webpage(self.detailpage)
        # print raw_html

        plugin = autodl.plugins.mangaFrCom.MangaFrCom([{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangafrcom",
            "title": "shoukugeki",
            "episode": "9"}])
        result_720p = plugin.parse_detailpage_for_mirrors(raw_html, "720p")
        # print result

        assert_equal(result_720p, ['/tmp/multiup-720p-home.html'])

        result_1080p = plugin.parse_detailpage_for_mirrors(raw_html, "1080p")
        # print result

        assert_equal(result_1080p, ['/tmp/multiup-1080p-home.html'])

    @patch('autodl.plugins.jhebergNet.JhebergNet.get_links')
    @patch('autodl.plugins.multiupOrg.MultiupOrg.get_links')
    @patch('autodl.utils.get_activated_hosters')
    def test_parse_mirrors_for_links(self,
                                     get_activated_hosters,
                                     multiup,
                                     jheberg):
        plugin = autodl.plugins.mangaFrCom.MangaFrCom([{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangafrcom",
            "title": "shoukugeki",
            "episode": "9"}])

        get_activated_hosters.return_value = ['Uplea', '1fichier']
        multiup.return_value = [{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangafrcom",
            "title": "shoukugeki",
            "episode": "9",
            "links": ["/success/uplea"]}]
        jheberg.return_value = [{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangafrcom",
            "title": "shoukugeki",
            "episode": "9",
            "links": ["/success/uplea"]}]

        # Test Horriblesubs
        result = plugin.parse_mirrors_for_links(["link_multiup"])
        # print result

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert_equal(result[0]['links'], ['/success/uplea'])

        # Test jheberg
        result = plugin.parse_mirrors_for_links(["link_jheberg"])
        # print result

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert_equal(result[0]['links'], ['/success/uplea'])

    def open_file(self, file_to_open):
        with open(file_to_open, 'r') as tmp_file:
            return tmp_file.read()

    @patch('autodl.utils.get_activated_hosters')
    @patch('autodl.utils.get_webpage')
    def test_get_result_list(self, get_webpage, get_activated_hosters):
        plugin = autodl.plugins.mangaFrCom.MangaFrCom([{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangaFrCom",
            "title": "shoukugeki",
            "episode": "9"}])

        get_webpage.side_effect = [self.open_file(self.homepage),
                                   self.open_file(self.detailpage),
                                   self.open_file(self.multiup_homepage),
                                   self.open_file(self.multiup_detailpage)]

        get_activated_hosters.return_value = ['Uplea', '1fichier']

        links = plugin.get_result_list()
        # print links
        assert_equal(links[0]["links"], ["/success/uplea"])

    @patch('autodl.plugins.mangaFrCom.MangaFrCom.parse_homepage_for_episodes')
    def test_get_result_list_with_None_detailpage(self, detail_url):
        plugin = autodl.plugins.mangaFrCom.MangaFrCom([{
            "target_type": "animes",
            "lang": "vostfr",
            "res": "720p",
            "site": "mangaFrCom",
            "title": "shoukugeki",
            "episode": "9"}])

        detail_url.return_value = None

        links = plugin.get_result_list()
        # print links
        assert_equal(links[0]["links"], None)
