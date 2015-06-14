from nose.tools import assert_equal
import unittest
import autodl.utils
import autodl.settings
import os
import json


class TestGetWebpage(unittest.TestCase):
    """

    """

    def setUp(self):
        with open("/tmp/testpage.html", "w") as file_tmp:
            file_tmp.write('<html><body>yeah</body></html>')

    def tearDown(self):
        os.remove("/tmp/testpage.html")

    def test_get_webpage(self):
        raw_page = autodl.utils.get_webpage("/tmp/testpage.html")

        assert_equal(raw_page, '<html><body>yeah</body></html>')
        assert isinstance(raw_page, str)
        with self.assertRaises(IOError):
            autodl.utils.get_webpage("/tmp/errorpage.html")


class TestGetActivatedHosters(unittest.TestCase):

    def setUp(self):
        with open("/tmp/config.json", "w") as file_tmp:
            json.dump({"hosters": ["uplea", "1fichier", "Filefactory",
                       "tuslfile"], "supported_sites": {"animes":
                       ["mangaFrCom", "animeserv"], "series":
                       ["scenesources", "telechargementz"]}, "target_titles":
                       {"animes": {"naruto": "None", "shoukugeki": "9"},
                       "series": {"atlantis": "10", "olympus": "None"}},
                       "target_ep": {"shoukugeki": "9", "atlantis": "10"}},
                      file_tmp)

    def tearDown(self):
        os.remove("/tmp/config.json")

    def test_get_activated_hosters(self):
        autodl.settings.set_globals({"CONFIG_FILE": "/tmp/config.json"})
        # test the if condition
        hosters = autodl.utils.get_activated_hosters(
            config_file="/tmp/config.json")

        # print hosters

        assert isinstance(hosters, list)
        assert_equal(hosters, [u'uplea', u'1fichier', u'Filefactory',
                               u'tuslfile'])

        # test the else statement
        hosters = autodl.utils.get_activated_hosters()
        assert_equal(hosters, [u'uplea', u'1fichier', u'Filefactory',
                               u'tuslfile'])

        # test the error
        with self.assertRaises(IOError):
            autodl.settings.set_globals({"CONFIG_FILE": "/tmp/error.json"})
            hosters = autodl.utils.get_activated_hosters()
            print hosters
