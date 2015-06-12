import logging
import json
import os
#from plugins import *

# Logginf configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('autodl/logs/autodl.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class Targets(object):
    """create a target object from config files"""
    def __init__(self, **kwargs):
        self.config_file_path = ""
        logger.debug("Trying to load configuration file")
        try:
            if ("config_file" in kwargs) and \
               os.path.isfile(kwargs["config_file"]):
                self.config_file_path = kwargs["config_file"]
            else:
                self.config_file_path = "/etc/autodl/autodl_config.json"

            with open(self.config_file_path, 'r+') as fichier:
                self.decoded = json.load(fichier)
            logger.debug("Successfully load config file from %s with \
                    content %s" % (self.config_file_path, self.decoded))

        except IOError as e:
            logger.error("No configuration file found in %s"
                         % (self.config_file_path))
            raise e

    def is_valid_type(self, type_name):
        """
        check if the string provided is a supported type
        """
        self.type_name = type_name
        supported_types = ["animes", "series"]
        result = False

        for i in supported_types:
            if i == self.type_name:
                result = True

        if result is True:
                logger.debug("%s is a valid type" % (self.type_name))
        else:
                logger.error("%s is not a valid type" % (self.type_name))

        return result

    def is_valid_plugin(self, plugin):
        """
        check if the string provided is part of the plugins
        """
        self.plugin = plugin
        cwd = os.getcwd()
        plugins_list = os.listdir(cwd + "/autodl/plugins")
        result = False
        for i in plugins_list:
            if self.plugin in i:
                result = True
                break
        if result is True:
                logger.debug("%s is a valid plugin" % (plugin))
        else:
                logger.error("%s is not a valid plugin" % (plugin))

        return result

    def ep_to_dl(self, media_type, title):
        self.media_type = media_type
        self.title = title
        target_ep = None

        for i in self.decoded["target_titles"][self.media_type]:
            if i == self.title:
                 target_ep = self.decoded["target_titles"][self.media_type][i]

        return target_ep


    def create(self, **kwargs):
        """
        Create and return a list of targets from configuration file. Targets
        inside that list depend of the paramters passed to the create function.
        This list can passed to a crawler object to fetch actual urls.
        It can take 3 arguments in this order :
        target_type, target_site, target_title
        TODO: Raise an error line 78 instead of a print
        """
        target_type = None
        target_site = None
        target_title = None
        target_ep = None
        for i in kwargs:
            if i == "target_type":
                target_type = kwargs["target_type"]
            elif i == "target_site":
                target_site = kwargs["target_site"]
            elif i == "target_title":
                target_title = kwargs["target_title"]
            elif i == "target_ep":
                target_ep = kwargs["target_ep"]

        targets_list = []

        if len(kwargs) == 0:
            # no arguments provided => create all targets (every titles, for
            # every sites and for every types
            for i in self.decoded["supported_sites"]:
                for j in self.decoded["supported_sites"][i]:
                    for k in self.decoded["target_titles"][i]:
                        target_ep = self.ep_to_dl(i, k)
                        targets_list.append([i, j, k, target_ep])

        elif target_type is not None:
            if (target_type is not None) and (target_site is not None):
                if (target_type is not None) and (target_site is not None) \
                   and (target_title is not None):
                    # If all three arguments are provided
                    # TODO: Check if the 3 arguments provided are valids
                    target_ep = self.ep_to_dl(target_type, target_title)
                    targets_list.append([target_type, target_site,
                                        target_title, target_ep])
                else:
                    # If 2 arguments are provided (target_type and target_site)
                    # TODO: Check if the 2 arguments provided are valids
                    for i in self.decoded["target_titles"][target_type]:
                        target_ep = self.ep_to_dl(target_type, i)
                        targets_list.append([target_type, target_site, i, target_ep])
            else:
                # If 1 argument is provided (target_type)
                # TODO: Check if the argument provided is valid
                for i in self.decoded["supported_sites"][target_type]:
                    for j in self.decoded["target_titles"][target_type]:
                        target_ep = self.ep_to_dl(target_type, j)
                        targets_list.append([target_type, i, j, target_ep])
        else:
            print "ERROR - Il semble que je n'ai pas compris un des parametres"

        logger.debug("Successfully created a list of targets content %s"
                     % (targets_list))
        return targets_list


# TODO: LOG things
class Crawler(object):
    """ Crawler object to get url for some titles on some sites"""

    def __init__(self, target):
        self.target_type = target[0]
        self.target_site = target[1]
        self.target_title = target[2]

        if self.target_type == "animes":
            pass
        elif self.target_type == "series":
            pass
        else:
            print "Error - Type %s is not supported" % (self.target_type)

    def get():
        pass


#tgt = Targets()
#tgt.is_valid_plugin("test")
#tl = tgt.create(target_type="animes", target_site="mangaFrCom", target_title="shokugeki")
#print tl

#mangaFrCom.get_links(tl[0][2], tl[0][3])

#for i in tl:
#    print i
#    crawl = Crawler(i)
#    print crawl.target_type
#    print crawl.target_site
#    print crawl.target_title
#

#tgt.ep_to_dl("series", "atlantis")
