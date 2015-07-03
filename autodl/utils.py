import urllib
import logging
import json
import settings
import os

# FIXME
# Logginf configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def set_globals(DICT_OPTS):
    global CONFIG_FILE
    CONFIG_FILE = DICT_OPTS["CONFIG_FILE"]

    global USER_SETTINGS_FILE
    USER_SETTINGS_FILE = DICT_OPTS["USER_SETTINGS_FILE"]
            

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
    get activated hosters from configuration file (optionally pass as a
    parameter)
    return them as a list
    """
    # print settings.CONFIG_FILE + " - test variable globale"
    logger.debug("Trying to load configuration file")
    try:
        # TODO: make the work to remove this if
        if ("config_file" in kwargs) and os.path.isfile(kwargs["config_file"]):
            config_file_path = kwargs["config_file"]
        else:
            config_file_path = settings.CONFIG_FILE

        with open(config_file_path, 'r+') as fichier:
            decoded = json.load(fichier)
        logger.debug("Successfully load config file from %s with \
            content %s" % (config_file_path, decoded))

    except IOError as e:
        logger.error("No configuration file found in %s"
                     % (config_file_path))
        raise e

    hosters = decoded["hosters"]
    # print hosters
    return hosters
