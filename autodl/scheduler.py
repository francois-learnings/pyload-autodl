import time, datetime, threading, logging, json, os, crawler
import autodl.pyload_client
import autodl.plugins.mangaFrCom 
import autodl.plugins.scnsrcMe
import autodl.plugins.horriblesubsInfo
import autodl.utils

# Logginf configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Scheduler(object):
    """

    """

    def __init__(self, DICT_OPTS, **kwargs):
        """ 
        Constructor 
        """
        self.DICT_OPTS = DICT_OPTS

        self.CONFIG_FILE = self.DICT_OPTS["CONFIG_FILE"]
        self.USER_SETTINGS_FILE = self.DICT_OPTS["USER_SETTINGS_FILE"]
        self.SERVER_IP = self.DICT_OPTS["SERVER_IP"]
        self.SERVER_PORT = self.DICT_OPTS["SERVER_PORT"]
        self.USER = self.DICT_OPTS["USER"]
        self.PASSWORD = self.DICT_OPTS["PASSWORD"]

        self.config_content = autodl.utils.load_config_file(self.CONFIG_FILE)
        self.user_settings_content = autodl.utils.load_user_settings_file(
                self.USER_SETTINGS_FILE)

    #TODO : move the wile loop in here ?   
    def run (self):    
        supported_types = ["animes", "series"]
        #TODO: Deal with the event of a thread crashing
        for media_type in supported_types:
            #print media_type
            thread = threading.Thread(target=self.check_type, 
                    args=(media_type,))
            # Daemonize thread
            thread.daemon = True
            # Start the execution
            thread.start()                                  


    def increment_episode(self, media_type, lang, res, title):
        self.media_type = media_type
        self.lang = lang
        self.res = res
        self.title = title

        with open(self.USER_SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            current_episode = int(data[self.media_type]
                    [lang][res][self.title])
            #print current_episode
            new_episode = str(current_episode + 1)
            #print new_episode

            data[self.media_type][lang][res][self.title] = new_episode
        
        with open(self.USER_SETTINGS_FILE, 'w') as f:
            f.write(json.dumps(data, indent=4))


    def get_links_from_plugin(self, target_list, site):
        self.target_list = target_list
        self.site = site

        links = None
        if self.site == "mangaFrCom":
            plugin = autodl.plugins.mangaFrCom.MangaFrCom(self.target_list)
            links = plugin.get_result_list()
            #print links
        elif self.site == "horriblesubsInfo":
            plugin = autodl.plugins.horriblesubsInfo.HorriblesubsInfo(
                    self.target_list)
            links = plugin.get_result_list()
        elif self.site == "scnsrcMe":
            links = autodl.plugins.scnsrcMe.get_result_list(self.target_list)

        return links

    def push_to_pyload(self, pltargets):
        """
        :param links:   type list
                        format [element1, element2, element3]

                        element: {  'media_type': 'sometype',
                                    'lang': 'somelang',
                                    'res': 'someres',
                                    'title': 'sometitle',
                                    'episode': 'someepisode',
                                    'links': [link1, link2, links3]
                                 } 
        """
        self.pltargets = pltargets
        #print self.pltargets
        if self.pltargets is not None:
            for element in self.pltargets:
                #print element
                if ((element['links'] is not None) and 
                        (element['links'] != [])):
                    #print element['links']
                    #push_to_pyload(links[element])
                    client = autodl.pyload_client.pyloadClient(self.SERVER_IP, 
                            self.SERVER_PORT, self.USER, self.PASSWORD)
                    #link = client.choose_link(links[element])
                    title = element['title']
                    # Try every links until one is valid
                    for link in element['links']:
                        #print element
                        #print link
                        if link is not None:
                            response = client.push_link(title, link)
                            #print response
                            if response == "success":
                                self.increment_episode(element['target_type'], 
                                        element['lang'], element['res'], 
                                        element['title'])
                                       
                                break

    def list_uniq_site(self, media_type):
        tgt = crawler.Crawler(user_settings_file=self.USER_SETTINGS_FILE, 
                config_file=self.CONFIG_FILE)
        pertinent_sites = tgt.get_pertinent_sites(media_type)
        #print pertinent_sites
        return_list = []
        for lang in pertinent_sites:
            for res in pertinent_sites[lang]:
                sites = pertinent_sites[lang][res]
                for site in sites:
                    if site not in return_list:
                        return_list.append(site)
        #print return_list            
        return return_list            


    def check_type(self, media_type):
        while self.keep_running() == True:
            now = time.time()
            check_interval = 15
            next_call = now + (60 * check_interval)

            list_sites = self.list_uniq_site(media_type)
            print datetime.datetime.now(), media_type

            for site in list_sites:
                links = []
                print site
                tgt = crawler.Crawler(user_settings_file=self.USER_SETTINGS_FILE, 
                        config_file=self.CONFIG_FILE)

                target_list = tgt.target_create(target_type=media_type, 
                        target_site=site)
                #print target_list

                links = self.get_links_from_plugin(target_list, site)
                #print links

                self.push_to_pyload(links)

            time.sleep(next_call - time.time())


    def keep_running(self):
        return True
