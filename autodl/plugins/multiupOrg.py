from lxml import html
import urllib, logging
import autodl.utils


# Logging configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MultiupOrg(object):
    """
    Class to interact with the site multiup.org
    methods:
        get_links
        parse_homepage_for_detail_url
        parse_detail_page_for_links
    """
    def __init__(self, url):
        """
        constructor
        """
        self.url = url
        #print self.url

    def get_links(self, **kwargs):
        '''
        Return a list of links from hosts in "desired_hosts" list
        '''
        #get homepage
        homepage = autodl.utils.get_webpage(self.url)

        #FIXME: Added for test purpose (use a MOCK in the test instead ?)
        if len(kwargs) == 0:
            #parse homepage for detail url
            detail_url = self.parse_homepage_for_detail_url(homepage)
        else:
            detail_url = self.parse_homepage_for_detail_url(homepage, baseurl="/tmp")
        #print detail_url    

        #get detailpage
        detailpage = autodl.utils.get_webpage(detail_url)

        #parse detailpage for links
        links = self.parse_detail_page_for_links(detailpage)

        return links

    def parse_homepage_for_detail_url(self, raw_html, **kwargs):
        """
        parse webpage for detail_url
        return detail_url
        """
        tree = html.fromstring(raw_html)
        #print raw_html

        detail = tree.xpath('//a[@class="btn"]/@href')
        logger.debug("Found detail page relative path: %s" % (detail))
        #print detail

        # FIXME: Added for test purpose
        if len(kwargs) is 0:
            base_url = "http://www.multiup.org"
        else:
            base_url = kwargs["baseurl"]
        detail_url = base_url + detail[0]
        logger.debug("Built detail page url: %s" % (detail_url))

        #print detail_url
        return detail_url

    def parse_detail_page_for_links(self, raw_html):
        """
        parse detail webpage for links
        return list of links
        """
        tree = html.fromstring(raw_html)
        #print data

        links = tree.xpath('//a[@class="btn btn-small disabled link host"]/@href')
        logger.debug("Found raw links list: %s" % (links))
        #print links

        desired_hosts = autodl.utils.get_activated_hosters()
        returned_links = []
        for host in desired_hosts:
            for link in links:
                #TODO: fix the mandatory "CamelCase in config file because of some plugin
                if host.lower() in link:
                    returned_links.append(link)
        logger.debug("Built returned links list: %s" % (returned_links))
        return returned_links

