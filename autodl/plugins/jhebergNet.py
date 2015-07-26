from lxml import html
import urllib, logging, requests, time
from selenium import webdriver
import autodl.utils


#TODO: make it consistent /w other files
# Logging configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class JhebergNet(object):
    """
    Class to interact with the website jeberg.net
    :para url: url as a string
    :param s: session object (obtain from requests.Session() )
    methods:
        get_links
        parse_homepage_for_detail_url
        parse_detailpage_for_redirection_link
    """
    def __init__(self, url):
        self.url = url
        self.s = requests.Session()
        #print url

    #TODO: Factorize the get_homepage and the get_detailpage methods
    #TODO: See for a replacement of the utils.get_webpage method
    def get_homepage(self):
        """

        """
        #Get homepage
        logger.debug("Trying to load webpage: %s" % (self.url))
        #s = requests.Session()
        try:
            raw_page = self.s.get(self.url)
        except IOError as e:
            logger.error("Could not find page %s"
                         % (self.url))
            raise e

        data = raw_page.content
        token = raw_page.cookies['csrftoken']
        cookies = dict(csrftoken=token)
        #print cookies
        #return [data, token, cookies]
        return [data, cookies]

    def get_detailpage(self, detailurl, cookies):
        """
        :param url: url as a string
        :param cookies is a dict of key:values cookies obtained by visiting the homepage
        """
        self.detailurl = detailurl
        self.cookies = cookies
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0', 'referer': self.url}
        #print headers

        logger.debug("Trying to load page: %s" % (self.detailurl))
        try:
             detail_page = self.s.get(self.detailurl, cookies=self.cookies, headers=headers)
        except IOError as e:
            logger.error("Could not fin page %s"
                         % (self.detailurl))
            raise e

        data = detail_page.content
        #print data
        return data


    def get_links(self):
        """

        """
        homepage_infos = self.get_homepage()
        homepage_html = homepage_infos[0]
        cookies = homepage_infos[1]
        #print homepage_html, cookies

        detail_url = self.parse_homepage_for_detail_url(homepage_html)
        #print detail_url

        detailpage = self.get_detailpage(detail_url, cookies)
        #print detailpage

        redir_links = self.parse_detailpage_for_redirection_link(detailpage)
        #print redir_links

        hosters_links = self.get_hoster_link_from_redirection_url(redir_links)

        return hosters_links



    def parse_homepage_for_detail_url(self, raw_html):
        """

        """
        self.raw_html = raw_html
        tree = html.fromstring(self.raw_html)
        #print data

        detail = tree.xpath('//div[@class="wrap"]/a[@class="dl-button"]/@href')
        logger.debug("Found detail page relative path: %s" % (detail))
        #print detail

        base_url = "http://www.jheberg.net"
        detail_url = base_url + detail[0]
        logger.debug("Built detail page url: %s" % (detail_url))
        #print detail_url

        return detail_url

    def parse_detailpage_for_redirection_link(self, raw_html):
        """

        """
        self.raw_html = raw_html
        tree = html.fromstring(self.raw_html)
        redirect_rel_path = tree.xpath('//a[@class="hoster-thumbnail"]/@href')

        activated_hosters = autodl.utils.get_activated_hosters()

        redirection_links = []
        for link in redirect_rel_path:
            #print link
            for hoster in activated_hosters:
                #print hoster
                if (hoster.lower() in link) and (link is not None):
                    redirection_url = "http://www.jheberg.net" + link
                    #print redirection_url
                    redirection_links.append(redirection_url)

        return redirection_links

    #TODO: find a way to test this method !
    def get_hoster_link_from_redirection_url(self,links_list):
        """

        """
        self.links_list = links_list
        returned_links = []
        for redirection_url in self.links_list:
            #Get the real link from the redirection urls
            logger.debug("Trying to load page: %s" % (redirection_url))
            #driver = webdriver.Firefox()
            driver = webdriver.PhantomJS()
            driver.get(redirection_url)

            #this waits for the new page to load
            #TODO: Do anything else but this infinite loop, like a if /w an increment or add a timer
            while(redirection_url == driver.current_url):
                  time.sleep(1)
                  #print driver.current_url
            redirected_url = driver.current_url
            driver.quit()
            #print redirected_url
            returned_links.append(redirected_url)

        if returned_links != []:
            #print returned_links
            return returned_links
        else:
            print "didn\'t find hoster"
