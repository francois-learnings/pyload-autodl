import urllib, logging, json

# FIXME
# Logginf configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('autodl/logs/autodl.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def get_webpage(url):
    logger.debug("Trying to load webpage: %s" % (url))
    try:
        raw_page = urllib.urlopen(url)
        data = raw_page.read()
        raw_page.close()
    
        return data
    
    except IOError as e:
        logger.error("Could not find page %s"
                        % (url))
        raise e

def get_activated_hosters(**kwargs):
    """
    get activated hosters from configuration file (optionally pass as a parameter)
    return them as a list
    """
    logger.debug("Trying to load configuration file")
    try:
        if ("config_file" in kwargs) and \
             os.path.isfile(kwargs["config_file"]):
            config_file_path = kwargs["config_file"]
        else:
            config_file_path = "/etc/autodl/autodl_config.json"

        with open(config_file_path, 'r+') as fichier:
            decoded = json.load(fichier)
        logger.debug("Successfully load config file from %s with \
            content %s" % (config_file_path, decoded))

    except IOError as e:
        logger.error("No configuration file found in %s"
                     % (config_file_path))
        raise e

    hosters = decoded["hosters"]
    #print hosters
    return hosters
