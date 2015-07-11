from nose.tools import *
import autodl.crawler
import os
import json
import unittest

class Test_crawler(unittest.TestCase):


    def setUp(self):
        self.config_file = "/tmp/tmp_config.json"
        self.user_settings_file = "/tmp/tmp_user_settings.json"
        with open(self.user_settings_file, "w") as file_tmp:
            json.dump({"animes": {"vostfr": { "720p": {"naruto": "None", 
                "shoukugeki":"9"}, "1080p": {"shingeki": "8"}}, "vosta": 
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

            

    def test_load_user_settings_file(self):
        user_settings_file = self.user_settings_file
        config_file = self.config_file

        tgt = autodl.crawler.Crawler(user_settings_file=user_settings_file, 
                config_file=config_file).load_user_settings_file(
                        user_settings_file=user_settings_file)
    
        assert isinstance(tgt, dict)
    

    def test_load_config_file(self):
        user_settings_file = self.user_settings_file
        config_file = self.config_file
    
        tgt = autodl.crawler.Crawler(user_settings_file=user_settings_file, 
                config_file=config_file).load_config_file(
                        config_file=config_file)
    
        assert isinstance(tgt, dict)
    
    def test_Crawler(self):
        user_settings_file = self.user_settings_file
        config_file = self.config_file
    
        tgt = autodl.crawler.Crawler(user_settings_file=user_settings_file, 
                config_file=config_file)
        #assert_equal(tgt.user_settings_file_path, user_settings_file)
        #print tgt.user_settings
        assert isinstance(tgt.user_settings, dict)
        assert isinstance(tgt.config, dict)
    
    def test_ep_to_dl(self):
        user_settings_file = self.user_settings_file
        config_file = self.config_file
    
        tgt = autodl.crawler.Crawler(user_settings_file=user_settings_file,
                config_file=config_file)
        val = tgt.ep_to_dl("animes", "vostfr", "720p","shoukugeki")
        assert_equal(val, "9")
    
    def test_get_activated_res(self):
        user_settings_file = self.user_settings_file
        config_file = self.config_file
    
        tgt = autodl.crawler.Crawler(user_settings_file=user_settings_file,
                config_file=config_file)
        res = tgt.get_activated_res("animes")
        assert_equal(res["vosta"], [u'720p'])
        assert_equal(res["vostfr"], [u'720p', u'1080p'])
    
    def test_get_pertinent_sites(self):
        user_settings_file = self.user_settings_file
        config_file = self.config_file
    
        tgt = autodl.crawler.Crawler(user_settings_file=user_settings_file,
                config_file=config_file)
        #res = tgt.get_activated_res("animes")
        #print res
        sites = tgt.get_pertinent_sites("animes") 
    
        assert_equal(sites["vosta"]['720p'], [u'horriblesubsInfo'])
        assert isinstance(sites, dict)
    
    def test_targets_create(self):
        user_settings_file = self.user_settings_file
        config_file = self.config_file
    
        plugin = autodl.crawler.Crawler(user_settings_file=user_settings_file,
                config_file=config_file)
        tgt = plugin.target_create("animes", 'mangaFrCom')
        #print tgt
        assert_equal(tgt[0],{'res': u'720p', 'lang': u'vostfr', 'title': u'naruto', 
            'episode': u'None', 'target_type': 'animes', 
            'site': u'mangaFrCom'}) 
            
            
        assert isinstance(tgt, list)
        assert isinstance(tgt[0], dict)
