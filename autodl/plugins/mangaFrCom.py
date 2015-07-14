from lxml import html
import logging
import autodl.plugins.multiupOrg
import autodl.plugins.jhebergNet
import autodl.utils

# FIXME
# Logging configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MangaFrCom(object):
    """
    Class to interact with the with the site manga-fr.com
    Supported target_type "animes"
    Supported language "vostfr"
    Supported resolutions "720p", "1080p"

    methods:
    get_result_list
    parse_homepage_for_episodes
    parse_detailpage_for_mirrors
    parse_mirrors_for_links
    """
    def __init__(self, targets, url="http://manga-fr.com/"):
        """
        :param targets: list of dict (ie list of targets)
            [target1, ..., targetN]

        One target has the following form :
        {
            "target_type": "sometype",
            "lang": "somelang",
            "res": "someres",
            "title": "sometitle",
            "episode", "someepisode"
        }
        """
        self.url = url
        self.targets = targets
        # print url

    def get_result_list(self, **kwargs):
        """

        """
        homepage = autodl.utils.get_webpage(self.url)
        # print homepage

        result = []
        for target in self.targets:
            if target['site'] == "mangaFrCom":
                # print target
                title = target['title']
                episode = target['episode']
                # print title, episode
                detail_url = self.parse_homepage_for_episodes(homepage,
                                                              title,
                                                              episode)
                # print detail_url

                if detail_url is None:
                    target['links'] = None
                else:
                    detailpage = autodl.utils.get_webpage(detail_url)
                    # print detailpage

                    mirrors = self.parse_detailpage_for_mirrors(detailpage,
                                                                target['res'])
                    # print mirrors

                    links = self.parse_mirrors_for_links(mirrors, arg="test")
                    # print links

                    target['links'] = links

                result.append(target)
        # print result
        return result

    def parse_homepage_for_episodes(self, raw_html, title, episode):
        """
        Parse homepage for "title" and "episode"
        and return the detail url
        """
        self.raw_html = raw_html
        self.title = title
        self.episode = episode

        # TODO: Use a try bloc
        tree = html.fromstring(raw_html)
        elements = tree.xpath('//section[@class="content"]/h2/a/@href'
                              '| //div[@class="num-NR" or@class="num-Fin"]'
                              '/text()')
        # print elements

        # Look for "title" and "episode" in the homepage
        # and return the url of the detail page for this episode
        index = 0
        detail_url = None
        for i in elements:
            if index < len(elements):
                # print title
                # print i
                # print elements[index]
                if ((title in i) and (episode is None)) or \
                   ((title in i) and (episode in elements[index + 1])):
                    logger.info("Found title %s episode %s in %s" %
                                (title, episode, i))
                    detail_url = i
                    break
                index += 1
        else:
            logger.info("Did not find title %s episode %s in %s" %
                        (title, episode, self.url))

        # print detail_url
        return detail_url

    def parse_detailpage_for_mirrors(self, raw_html, res):
        """
        Parse the html provided as parameter for links containing supported
        platform return a list of mirrors (links to supported platform ie
        multiup, jheberg...)
        """
        # TODO: Add a try bloc
        tree = html.fromstring(raw_html)
        # print raw_html
        # print res

        # Find relevant urls
        if res == "720p":
            links = tree.xpath('//section/article/table[1]/tbody/tr[2]'
                               '/td[@class="table-links"]/a/@href')
        elif res == "1080p":
            links = tree.xpath('//section/article/table[2]/tbody/tr[2]'
                               '/td[@class="table-links"]/a/@href')
        # print links
        logger.debug("Found links %s for resolution %s" % (links, res))

        # look for supported mirrors in the links on the detail page
        # and add them to list of mirros to analyze
        supported_mirrors = ["multiup", "jheberg"]
        provided_mirrors = []
        for mirror in supported_mirrors:
            for link in links:
                if mirror in link:
                    # print link
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
                # TODO: use a try bloc and deal w/ error
                plugin = autodl.plugins.multiupOrg.MultiupOrg(mirror)
                links_list = plugin.get_links()
                logger.info("Successfully built links list: %s" % (links_list))
                break
            elif "jheberg" in mirror:
                # TODO: use a try bloc and deal w/ error
                plugin = autodl.plugins.jhebergNet.JhebergNet(mirror)
                links_list = plugin.get_links()
                logger.info("Successfully built links list: %s" % (links_list))
                break
            # else:
            #     #TODO: deal with error
            #     print "error mirror %s is not supported" % (mirror)
        return links_list
