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
        #with open("/tmp/config.json", "w") as file_tmp:
        #    json.dump({"hosters": ["uplea", "1fichier", "Filefactory",
        #               "tuslfile"], "supported_sites": {"animes":
        #               ["mangaFrCom", "animeserv"], "series":
        #               ["scenesources", "telechargementz"]}, "target_titles":
        #               {"animes": {"naruto": "None", "shoukugeki": "9"},
        #               "series": {"atlantis": "10", "olympus": "None"}},
        #               "target_ep": {"shoukugeki": "9", "atlantis": "10"}},
        #              file_tmp)
        self.config_file = "/tmp/config_tmp.json"
        with open(self.config_file, "w") as file_tmp:
            json.dump({"hosters": ["Uplea", "1fichier"], "activated_plugins":
                       {"series": {"vo": {"all_res": ["scnsrcMe", 
                       "telechargementz"], "480p": ["site_serie_vo_480p"]}, 
                       "vf": {"all_res": ["site_serie_vf_all_res"]}}, 
                       "animes": {"vostfr": {"all_res": ["mangaFrCom", "zt"], 
                       "1080p": ["animeserv"]},"vosta": {"all_res": 
                       ["horriblesubsInfo"]}}}}, file_tmp)

        self.user_settings_file = "/tmp/user_settings_tmp.json"
        with open(self.user_settings_file, "w") as file_tmp:
            json.dump({"animes": {"vostfr": { "720p": {"naruto": "None", 
                "shoukugeki":"9"}, "1080p": {"shingeki": "8"}}, "vosta": 
                {"720p": {"step": "10"}}}, "series": {"vo": {"480p": 
                {"atlantis": "10", "olympus": "None"}}}}, file_tmp)

    def tearDown(self):
        os.remove("/tmp/config_tmp.json")

    def test_get_activated_hosters(self):
        autodl.utils.set_globals({"CONFIG_FILE": self.config_file, 
            "USER_SETTINGS_FILE": self.user_settings_file})
        # test the if condition
        hosters = autodl.utils.get_activated_hosters(
            config_file="/tmp/config.json")

        # print hosters

        assert isinstance(hosters, list)
        assert_equal(hosters, [u'Uplea', u'1fichier'])

        # test the else statement
        hosters = autodl.utils.get_activated_hosters()
        assert_equal(hosters, [u'Uplea', u'1fichier'])

        # test the error
        with self.assertRaises(IOError):
            autodl.utils.set_globals({"CONFIG_FILE": "/tmp/error.json",
                "USER_SETTINGS_FILE": self.user_settings_file})
            hosters = autodl.utils.get_activated_hosters()


class TestGetLoadConfig(unittest.TestCase):
    def setUp(self):
        self.config_file = "/tmp/config_tmp.json"
        with open(self.config_file, "w") as file_tmp:
            json.dump({"hosters": ["Uplea", "1fichier"], "activated_plugins":
                       {"series": {"vo": {"all_res": ["scnsrcMe", 
                       "telechargementz"], "480p": ["site_serie_vo_480p"]}, 
                       "vf": {"all_res": ["site_serie_vf_all_res"]}}, 
                       "animes": {"vostfr": {"all_res": ["mangaFrCom", "zt"], 
                       "1080p": ["animeserv"]},"vosta": {"all_res": 
                       ["horriblesubsInfo"]}}}}, file_tmp)

    def tearDown(self):
        os.remove(self.config_file)

    def test_with_file(self):
        content = autodl.utils.load_config_file(self.config_file)

        assert isinstance(content, dict)

        assert_equal(content['hosters'], [u'Uplea', u'1fichier'])

    def test_ioerror(self):
        with self.assertRaises(IOError):
            autodl.utils.load_config_file("/tmp/error.json")


class TestGetLoadUserSettingsFile(unittest.TestCase):
    def setUp(self):
        self.user_settings_file = "/tmp/user_settings_tmp.json"
        with open(self.user_settings_file, "w") as file_tmp:
            json.dump({"animes": {"vostfr": { "720p": {"naruto": "None", 
                "shoukugeki":"9"}, "1080p": {"shingeki": "8"}}, "vosta": 
                {"720p": {"step": "10"}}}, "series": {"vo": {"480p": 
                {"atlantis": "10", "olympus": "None"}}}}, file_tmp)
                               
    def tearDown(self):
        os.remove(self.user_settings_file)

    def test_with_file(self):
        content = autodl.utils.load_user_settings_file(self.user_settings_file)
        #print content

        assert isinstance(content, dict)

        assert_equal(content['series'], {u'vo': {u'480p': {u'atlantis': u'10', 
            u'olympus': u'None'}}})

    def test_ioerror(self):
        with self.assertRaises(IOError):
            autodl.utils.load_user_settings_file("/tmp/error.json")
