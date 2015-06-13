import time, datetime, threading, logging, json, os, crawler
import autodl.pyload_client, autodl.plugins.mangaFrCom, autodl.plugins.scnsrcMe

# Logginf configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('autodl/logs/autodl.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
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

        supported_types = ["animes", "series"]
        for media_type in supported_types:
            thread = threading.Thread(target=self.check_type, args=(media_type,))
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution


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
                elif site == "animeservCom":
                    pass
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


#sched = Scheduler()
#while True:
#    time.sleep(1)



#next_call = time.time()
#
#def foo():
#    print datetime.datetime.now()
#
#def daemon(minutes):
#    while True:
#        global next_call
#        next_call = next_call+(60 * minutes)
#        threading.Timer( next_call - time.time(), foo ).start()
#        time.sleep(next_call - time.time())
#
#
#daemon(1)

#class ThreadingExample(object):
#    """ Threading example class
#
#    The run() method will be started and it will run in the background
#    until the application exits.
#    """
#
#    def __init__(self, interval=1):
#        """ Constructor
#
#        :type interval: int
#        :param interval: Check interval, in seconds
#        """
#        self.interval = 60 * interval
#        thread = threading.Thread(target=self.run, args=())
#        thread.daemon = True                            # Daemonize thread
#        thread.start()                                  # Start the execution
#
#    def run(self):
#        """ Method that runs forever """
#        while True:
#            # Do something
#            print('Doing something imporant in the background')
#                                
#            time.sleep(self.interval)
#
#example = ThreadingExample()
#while True:
#    time.sleep(1)



#time.sleep(3)
#print('Checkpoint')
#time.sleep(2)
#print('Bye')

