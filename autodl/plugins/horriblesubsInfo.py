from lxml import html
import urllib, logging
import autodl.utils
from selenium import webdriver 
from selenium.webdriver.common.by import By


# Logging configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HorriblesubsInfo(object):
    """
    Class to interact with the site horriblesubs.info
    methods:
        get_result_list
    """
    def __init__(self, targets, url="http://horriblesubs.info"):
        """
        constructor
        """
        self.url = url
        self.targets = targets
        #print self.url

    def get_result_list(self):
        driver = webdriver.PhantomJS()
        activated_hosters = autodl.utils.get_activated_hosters()
        #activated_hosters = ["Uplea", "Filefactory"]
        #TODO: use a try bloc
        driver.get(self.url)
        elements = driver.find_elements(By.XPATH, '//div[@class="latest"]/div')

        result = {}
        for target in self.targets:
            if target[1] == "horriblesubsInfo":
                #print target
                title = target[2]
                episode = target[3]
                #print title, episode
                for element in elements:
                    #print element
                    ref =  element.get_attribute("id")
                    #print ref
                    if (title in ref) and (episode in ref):
                        logger.info("Found title %s episode %s in %s"  %
                                    (title, episode, self.url))
                        links_list = driver.find_elements(By.XPATH, '//div[@id="' + ref + '"]/div[@class="resolutions-block"]/div[@class="linkful resolution-block"]/span[@id="720p"]/span[@class="ind-link"]/a')
                        returned_links = []
                        for link in links_list:
                            #print link.get_attribute("href")
                            for i in activated_hosters:
                                if i.lower() in link.get_attribute("href"):
                                    returned_links.append(link.get_attribute("href"))
                        logger.info("Successfully built links list: %s for %s %s" % (returned_links, title, episode))            
                        result[target[2]] = returned_links
                else:      
                    logger.info("Did not find title %s episode %s in %s" % (target[2], target[3], self.url))

        driver.quit()
        #print result
        return result

