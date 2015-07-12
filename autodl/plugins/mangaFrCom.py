from lxml import html
import urllib
import logging
import autodl.plugins.multiupOrg, autodl.plugins.jhebergNet
import autodl.utils

# FIXME
# Logging configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MangaFrCom(object):
    """
    Class to interact with the with the site manga-fr.com

    methods:
    get_result_list
    parse_homepage_for_episodes
    parse_detailpage_for_mirrors
    parse_mirrors_for_links
    """
    def __init__(self, targets, url="http://manga-fr.com/"):
        """
        :param targets: list of list (ie list of targets)
        """
        self.url = url
        self.targets = targets
        #print url


    def get_result_list(self, **kwargs):
        homepage = autodl.utils.get_webpage(self.url)
        #print homepage

        result = []
        for target in self.targets:
            if target['site'] == "mangaFrCom": 
                #print target
                title = target['title']
                episode = target['episode']
                #print title, episode
                detail_url = self.parse_homepage_for_episodes(homepage, title, episode)
                #print detail_url
                
                if detail_url is None:
                    target['links'] = None
                else:
                    detailpage = autodl.utils.get_webpage(detail_url)
                
                    mirrors = self.parse_detailpage_for_mirrors(detailpage)
                    #print mirrors
                
                    #FIXME: Added for test purpose - remove from here an replace /w a mock ?
                    if len(kwargs) is 0:
                        links = self.parse_mirrors_for_links(mirrors)
                    else:
                        links = self.parse_mirrors_for_links(mirrors, arg="test")
                    #print links
                    target['links'] = links
                    result.append(target)
        #print result
        return result

    def parse_homepage_for_episodes(self, raw_html, title, episode):
        """
        Parse homepage for "title" and "episode"
        and return the detail url
        """
        self.raw_html = raw_html
        self.title = title
        self.episode = episode

        #TODO: Use a try bloc
        tree = html.fromstring(raw_html)
        elements = tree.xpath('//section[@class="content"]/h2/a/@href | //div[@class="num-NR" or@class="num-Fin"]/text()')
        #print elements

        # Look for "title" and "episode" in the homepage
        # and return the url of the detail page for this episode
        index = 0
        detail_url = None
        for i in elements:
            if index < len(elements):
                #print title
                #print i
                #print elements[index]
                if ((title in i) and (episode is None)) or \
                   ((title in i) and (episode in elements[index + 1])):
                    logger.info("Found title %s episode %s in %s" %
                                 (title, episode, i))
                    # print "found title %s episode %s in %s" % (title,
                    #                                            elements[index], i)
                    detail_url = i
                    break
                index += 1
        else:
            logger.info("Did not find title %s episode %s in %s" %
                         (title, episode, self.url))

        #print detail_url
        return detail_url    
    
    def parse_detailpage_for_mirrors(self, raw_html):
        """
        Parse the html provided as parameter for links containing supported platform
        return a list of mirrors (links to supported platform ie multiup, jheberg...)
        """
        # TODO: Add a try bloc
        tree = html.fromstring(raw_html)
        #print raw_html

        # Find relevant urls
        links = tree.xpath('//td[@class="table-links"]/a/@href')
        logger.debug("Found links %s" % (links))
        #print links

        # look for supported mirrors in the links on the detail page
        # and add them to list of mirros to analyze
        supported_mirrors = ["multiup", "jheberg"]
        provided_mirrors = []
        for mirror in supported_mirrors:
            for link in links:
                if mirror in link:
                    #print link
                    provided_mirrors.append(link)

        logger.debug("Built mirrors list: %s" % (provided_mirrors))
        # print provided_mirrors
        return provided_mirrors

    def parse_mirrors_for_links(self, mirrors, **kwargs):
        """
        Parse a list of mirrors looking for links
        return a list of links
        """
        self.mirrors = mirrors

        for mirror in self.mirrors:
            if "multiup" in mirror:
                # condition added for test purpose
                if len(kwargs) is not 0:
                    plugin = autodl.plugins.multiupOrg.MultiupOrg(mirror)
                    links_list = plugin.get_links(url="/tmp")
                    #print links_list
                else:
                    plugin = autodl.plugins.multiupOrg.MultiupOrg(mirror)
                    links_list = plugin.get_links()
                logger.info("Successfully built links list: %s" % (links_list))
                break
            elif "jheberg" in mirror:
                # condition added for test purpose
                # TODO: should be removable now : TO TEST
                if len(kwargs) is not 0:
                    links_list = autodl.plugins.jhebergNet.get_links(mirror, baseurl="/tmp")
                else:
                    plugin = autodl.plugins.jhebergNet.JhebergNet(mirror)
                    links_list = plugin.get_links()
                logger.info("Successfully built links list: %s" % (links_list))
                break
            else:
                #TODO: deal with error
                print "error"
        return links_list
