from nose.tools import *
import unittest
import autodl.utils
import autodl.plugins.horriblesubsInfo
from mock import patch
import os



class Test_horriblesubsInfo(unittest.TestCase):

    def setUp(self):
        with open("/tmp/homepage.html", "w") as file_tmp:
            file_tmp.write('<html><body><div class="latest"><div id="shokugeki-11"><div class="resolutions-block"><div class="linkful resolution-block"><span id="720p"><span class="ind-link"><a href="http://success/filefactory"></a></span></span></div></div></div></div></body></html>')

    def tearDown(self):
        os.remove("/tmp/homepage.html")

    def test_horriblesubsInfo(self):
        plugin = autodl.plugins.horriblesubsInfo.HorriblesubsInfo([{
            'target_type': 'animes', 'lang': 'vosta', 'res': '720p', 
            'site': 'horriblesubsInfo', 'title': 'shokugeki', 
            'episode': '11'}], url="/tmp/homepage.html")
    
        assert_equal(plugin.url, "/tmp/homepage.html")
        assert_equal(plugin.targets, [{'target_type': 'animes', 
            'lang': 'vosta', 'res': '720p', 'site': 'horriblesubsInfo', 
            'title': 'shokugeki', 'episode': '11'}])
    

    @patch('autodl.utils.get_activated_hosters')
    def test_get_result_list(self, get_activated_hosters):
        plugin = autodl.plugins.horriblesubsInfo.HorriblesubsInfo([{
            'target_type': 'animes', 'lang': 'vosta', 'res': '720p', 
            'site': 'horriblesubsInfo', 'title': 'shokugeki', 
            'episode': '11'}], url="/tmp/homepage.html")
        autodl.utils.get_activated_hosters.return_value = ['Filefactory', '1fichier']
        result = plugin.get_result_list()
        #print result
        assert_equal(result[0]['links'], [u'http://success/filefactory'])
