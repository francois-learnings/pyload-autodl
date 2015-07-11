import logging
import json
import os
#from plugins import *

# Logginf configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Crawler(object):
    """
    create a target object from config files
    """
    def __init__(self, **kwargs):
        self.user_settings = self.load_user_settings_file(
                kwargs["user_settings_file"])
        self.config = self.load_config_file(
                kwargs["config_file"])


    def load_user_settings_file(self, user_settings_file):
        """
        Load user_settings file
        """
        self.user_settings_file_path = ""

        logger.debug("Trying to load user_settings file")
        try:
            self.user_settings_file_path = user_settings_file

            with open(self.user_settings_file_path, 'r+') as fichier:
                self.user_settings = json.load(fichier)
            logger.debug("Successfully load config file from %s"
                % (self.user_settings_file_path))

            return self.user_settings

        except (IOError, OSError) as e:
            logger.error("No user_settings file found in %s"
                         % (self.user_settings_file_path))
            raise e

    def load_config_file(self, config_file):
        """
        Load config file
        """
        self.config_file_path = ""

        logger.debug("Trying to load config file")
        try:
            self.config_file_path = config_file

            with open(self.config_file_path, 'r+') as fichier:
                self.config = json.load(fichier)
            logger.debug("Successfully load config file from %s"
                % (self.config_file_path,))

        except IOError as e:
            logger.error("No configuration file found in %s"
                         % (self.config_file_path,))
            raise e

        return self.config

    def ep_to_dl(self, media_type, lang, res, title):
        """
        return from the user_settings file, the number of the episode matching 
        parameters
        """
        self.media_type = media_type
        self.lang = lang
        self.res = res
        self.title = title
        target_ep = None

        for i in self.user_settings[self.media_type][self.lang][self.res]:
            if i == self.title:
                 target_ep = self.user_settings[self.media_type][self.lang]\
                         [self.res][i]

        return target_ep

    def get_activated_res(self, target_type):
        """
        return a dictionary with resolution used in user_settings.json for a 
        given type with the form {lang1: [res1, res2]}
        """
        self.target_type = target_type

        return_dict = {}
        
        for lang in self.user_settings[self.target_type]:
            #print lang
            res_list = []
            for res in self.user_settings[self.target_type][lang]:
                #print res
                res_list.append(res)
            #print res_list    
            return_dict[lang] = res_list
        #print return_dict    
        return return_dict    


    def get_pertinent_sites(self, target_type):
        """
        return a dict of site to check for links
        Those sites are chosen depending on the activated languages and 
        resolutions in the user_settings.json file
        """
        self.target_type = target_type
        self.resolutions = self.get_activated_res(self.target_type)

        # print self.resolutions
        # print self.config
        # print self.user_settings

        return_dict = {}
        for lang in self.resolutions:
            return_dict[lang] = {}
            #return_list.append(self.config["activated_plugins"]
            #        [self.target_type][lang]["all_res"])
            res_list = self.resolutions[lang]
            #print res_list

            for activated_res in res_list:
                return_dict[lang][activated_res] = []

                #print lang, activated_res
                avail_res_list = (self.config["activated_plugins"]
                        [self.target_type][lang])
                    
                #print avail_res_list
                
                for avail_res in avail_res_list:
                    # for every resolutions activated in the user_settings, we
                    # add to the return_list the sites for "all_res"
                    if avail_res == "all_res":
                        #print avail_res_list["all_res"]
                        return_dict[lang][activated_res].extend(
                                avail_res_list["all_res"])
                    if activated_res == avail_res:
                        #print avail_res, (self.config["activated_plugins"]
                        #        [self.target_type][lang][activated_res])
                        return_dict[lang][activated_res].extend(
                                avail_res_list[activated_res])
        #print return_dict
        return return_dict

    def target_create(self, target_type, target_site):
        """
        Create and return a list of targets from configuration file. 
        This list can passed to a plugin object to fetch actual urls.
        One target has the following structure:
        {
            "type": "sometype",
            "site": "somesite",
            "title": "sometitle",
            "episode": "someepisode",
            "res": "someres"
            
        }
        The returned structure is with the following form :
        [target1, target2, target3]
        """
        self.target_type = target_type
        self.target_site = target_site
        sites = self.get_pertinent_sites(self.target_type)

        targets_list = []
        for lang in sites:
            #print lang
            for res in sites[lang]:
                #print res
                for site in sites[lang][res]:
                    #print res, site
                    #print self.user_settings[self.target_type][lang][res]
                    if site == self.target_site:
                        for title in (self.user_settings[self.target_type][lang]
                                [res]):
                            #print title
                            episode = self.ep_to_dl(self.target_type, lang, res, 
                                    title)
                            target = {
                                    'target_type': self.target_type,
                                    'lang': lang,
                                    'res': res,
                                    'site': site,
                                    'title': title,
                                    'episode': episode
                                    }
                            targets_list.append(target)
        #print targets_list
        return targets_list
