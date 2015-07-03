import time, datetime, threading, logging, json, os, crawler
import autodl.pyload_client
import autodl.plugins.mangaFrCom 
import autodl.plugins.scnsrcMe
import autodl.plugins.horriblesubsInfo

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
        self.SERVER_IP = self.DICT_OPTS["SERVER_IP"]
        self.SERVER_PORT = self.DICT_OPTS["SERVER_PORT"]
        self.USER = self.DICT_OPTS["USER"]
        self.PASSWORD = self.DICT_OPTS["PASSWORD"]

        #self.config_file_path = ""
        #if ("config_file" in kwargs) and \
        #   os.path.isfile(kwargs["config_file"]):
        #    self.config_file_path = kwargs["config_file"]
        #else:
        #    self.config_file_path = "/etc/autodl/autodl_config.json"

        logger.debug("Trying to load configuration file")
        try:
            with open(self.CONFIG_FILE, 'r+') as fichier:
                self.decoded = json.load(fichier)
            logger.debug("Successfully load config file from %s with \
                    content %s" % (self.CONFIG_FILE, self.decoded))

        except IOError as e:
            logger.error("No configuration file found in %s"
                         % (self.CONFIG_FILE))
            raise e

        supported_types = ["animes", "series", "vosta"]
        for media_type in supported_types:
            thread = threading.Thread(target=self.check_type, args=(media_type,))
            # Daemonize thread
            thread.daemon = True
            # Start the execution
            thread.start()                                  


    def increment_episode(self, media_type, title):
        self.media_type = media_type
        self.title = title

        with open(self.CONFIG_FILE, 'r') as f:
            data = json.load(f)
            current_episode = int(data["target_titles"][self.media_type][self.title])
            #print current_episode
            new_episode = str(current_episode + 1)
            #print new_episode

            data["target_titles"][self.media_type][self.title] = new_episode
        
        with open(self.CONFIG_FILE, 'w') as f:
            f.write(json.dumps(data, indent=4))


    def check_type(self, media_type):
        while True:
            now = time.time()
            check_interval = 15
            next_call = now + (60 * check_interval)

            print datetime.datetime.now()
            for site in self.decoded["supported_sites"][media_type]:
                links = []
                #print site
                tgt = crawler.Targets()
                target_list = tgt.create(target_type=media_type, target_site=site)
                #print target_list

                if site == "mangaFrCom":
                    plugin = autodl.plugins.mangaFrCom.MangaFrCom(target_list)
                    links = plugin.get_result_list()
                    #print links
                elif site == "horriblesubsInfo":
                    plugin = autodl.plugins.horriblesubsInfo.HorriblesubsInfo(target_list)
                    links = plugin.get_result_list()
                elif site == "scnsrcMe":
                    links = autodl.plugins.scnsrcMe.get_result_list(target_list)
                    #print links

                for element in links:
                    #print element
                    if (links[element] is not None) and (links[element] != []):
                        #print links[element]
                        #push_to_pyload(links[element])
                        client = autodl.pyload_client.pyloadClient(self.SERVER_IP, self.SERVER_PORT, self.USER, self.PASSWORD)
                        #link = client.choose_link(links[element])
                        title = element
                        # Try every links until one is valid
                        for link in links[element]:
                            #print element
                            #print link
                            if link is not None:
                                response = client.push_link(title, link)
                                #print response
                                if response == "success":
                                    self.increment_episode(media_type, title)
                                    break

            time.sleep(next_call - time.time())


