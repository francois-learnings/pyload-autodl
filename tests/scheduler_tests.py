from nose.tools import assert_equal
import unittest
import autodl.utils
import os
import json
from mock import patch
from tl.testing.thread import ThreadJoiner
from tl.testing.thread import ThreadAwareTestCase
import time
import threading
import custom_errors


class TestScheduler(ThreadAwareTestCase):
    """

    """

    def setUp(self):
        self.config_file = "/tmp/tmp_config.json"
        self.user_settings_file = "/tmp/tmp_user_settings.json"
        with open(self.user_settings_file, "w") as file_tmp:
            json.dump({"animes": {"vostfr": { "720p": {"naruto": "None", 
                "shokugeki":"9"}, "1080p": {"shingeki": "8"}}, "vosta": 
                {"720p": {"step": "10"}}}, "series": {"vo": {"480p": 
                {"atlantis": "10", "olympus": "None"}}}}, file_tmp)

        with open(self.config_file, "w") as file_tmp:
            json.dump({"hosters": ["Uplea", "1fichier"], "activated_plugins": 
                {"series": {"vo": {"all_res": ["scnsrcMe", "telechargementz"], 
                "480p": ["site_serie_vo_480p"]}, "vf": {"all_res": 
                ["site_serie_vf_all_res"]}}, "animes": {"vostfr": {"all_res": 
                ["mangaFrCom", "zt"], "1080p": ["animeserv"]},"vosta": 
                {"all_res": ["horriblesubsInfo"]}}}}, file_tmp)

    def tearDown(self):
        os.remove(self.user_settings_file)
        os.remove(self.config_file)

    @unittest.skip("Until learn to test threads")
    @patch('autodl.scheduler.Scheduler.check_type')
    def test_run(self, check_type):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}

        #check_type = time.sleep(0.2)

        #with ThreadJoiner(1):
        #    scheduler = autodl.scheduler.Scheduler(DICT)
        #    self.run_in_thread(scheduler.run())

        #    #self.assertEqual(1, self.active_count())
        #    print self.active_count()
        #    print threading.active_count()
        #    #print type(threads)


    def test_increment_episode(self):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}

        scheduler = autodl.scheduler.Scheduler(DICT)
        scheduler.increment_episode("animes", "vostfr", "720p", "shokugeki")

        with open(self.user_settings_file, 'r') as f:
            data = json.load(f)
            #print data
        assert_equal(data["animes"]["vostfr"]["720p"]["shokugeki"], u'10')
        assert isinstance(data, dict)
        #with self.assertRaises(IOError):
        #    autodl.utils.get_webpage("/tmp/errorpage.html")

    @patch('autodl.plugins.mangaFrCom.MangaFrCom.get_result_list')
    def test_get_links_from_plugin_mangafr(self, mangafr):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}
               
        target_list_scnsrcMe = []
        
        scheduler = autodl.scheduler.Scheduler(DICT)

        # Test mangaFrCom
        target_list_mangaFrCom = [{'res': u'720p', 'title': u'naruto', 
            'episode': u'None', 'target_type': 'animes', 
            'site': u'mangaFrCom'}, {'res': u'720p', 'title': u'shokugeki', 
            'episode': u'9', 'target_type': 'animes', 'site': u'mangaFrCom'}, 
            {'res': u'1080p', 'title': u'shingeki', 'episode': u'8', 
            'target_type': 'animes', 'site': u'mangaFrCom'}]
            
        mangafr.return_value = "ok"    

        links = scheduler.get_links_from_plugin(target_list_mangaFrCom, 
                "mangaFrCom")
        assert_equal(links, "ok")

    @patch('autodl.plugins.horriblesubsInfo.HorriblesubsInfo.get_result_list')
    def test_get_links_from_plugin_horrible(self, horrible):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}
               
        scheduler = autodl.scheduler.Scheduler(DICT)
        # Test horriblesubs
        target_list_horriblesubsInfo = [{'res': u'720p', 'title': u'step', 
            'episode': u'10', 'target_type': 'animes', 
            'site': u'horriblesubsInfo'}]

        horrible.return_value = "ok"    

        links = scheduler.get_links_from_plugin(target_list_horriblesubsInfo, 
                "horriblesubsInfo")
        assert_equal(links, "ok")

    @patch('autodl.plugins.scnsrcMe.get_result_list')
    def test_get_links_from_plugin_scnsrc(self, horrible):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}
               
        scheduler = autodl.scheduler.Scheduler(DICT)
        # Test horriblesubs
        target_list_scnsrcMe = [{'res': u'720p', 'title': u'step', 
            'episode': u'10', 'target_type': 'animes', 
            'site': u'scnsrcMe'}]

        horrible.return_value = "ok"    

        links = scheduler.get_links_from_plugin(target_list_scnsrcMe, 
                "scnsrcMe")
        assert_equal(links, "ok")


    @patch('autodl.pyload_client.pyloadClient')
    def test_push_to_pyload(self, plclient):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}
        #Mock values
        client = plclient.return_value
        client.push_link.return_value = "success"

        scheduler = autodl.scheduler.Scheduler(DICT)
        scheduler.push_to_pyload([{"target_type": "animes", "lang": "vostfr",
            "res": "720p", "title": "shokugeki","episode": "9", 
            "links": ["somelink1", "somelink2"]}])
                                

    def test_list_uniq_site(self):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}

        scheduler = autodl.scheduler.Scheduler(DICT)
        returned_list = scheduler.list_uniq_site("animes")

        assert_equal(returned_list, [u'horriblesubsInfo', u'mangaFrCom', u'zt', 
            u'animeserv'])
        assert isinstance(returned_list, list)


    @patch('autodl.pyload_client.pyloadClient')
    @patch('autodl.scheduler.Scheduler.get_links_from_plugin')
    @patch('time.sleep')
    @patch('autodl.scheduler.Scheduler.keep_running')
    def test_check_type(self, running, sleep, get_links, plclient):
        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}

        running.side_effect = [True, False]

        sleep = time.sleep(1)

        get_links.return_value = [{'lang': u'vosta', 'episode': u'10', 
            'title': u'step', 'res': u'720p', 'target_type': 'animes', 
            'site': u'horriblesubsInfo', 'links': ['link1', 'link2']}]

        client = plclient.return_value
        client.push_link.return_value = "success"

        scheduler = autodl.scheduler.Scheduler(DICT)
        scheduler.check_type("animes")

        #TODO: assert things...


    def test_keep_running(self):

        DICT = {'CONFIG_FILE': '/tmp/tmp_config.json', 'USER_SETTINGS_FILE': 
                '/tmp/tmp_user_settings.json', 'SERVER_IP': '', 
                'SERVER_PORT': '', 'USER': '', 'PASSWORD': ''}

        scheduler = autodl.scheduler.Scheduler(DICT)

        assert_equal(scheduler.keep_running(), True)
