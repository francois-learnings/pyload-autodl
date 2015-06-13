from lxml import html
import urllib
import logging
import multiupOrg


# Logginf configuration and setting
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_result_list(list, **kwargs):
    """
    The param list is a list or targets. Each target is a list
    :param list
    :type list = list of list
    """
    if len(kwargs) == 0:
        site_url = "http://www.scnsrc.me/"
    else:
        if "url" in kwargs:
            site_url = kwargs["url"]
    logger.debug("Trying to load webpage: %s" % (site_url))
    try:
        raw_page = urllib.urlopen(site_url)
        data = raw_page.read()
        raw_page.close()
    except IOError as e:
        logger.error("Could not find page %s"
                     % (site_url))
        raise e

    #print data
    tree = html.fromstring(data)

    result = {}
    for target in list:
        #print target
        if target[1] == "scnsrcMe":
            links = get_links(tree, target[2], target[3])
            result[target[2]] = links
    return result

def get_links(tree, title, episode, **kwargs):
    '''
    '''
    #TODO: Check if this is still relevant
    if len(kwargs) == 0:
        site_url = "http://www.scnsrc.me/"
    else:
        if "url" in kwargs:
            site_url = kwargs["url"]

    if len(episode) == 1:
        episode = "e0" + episode
    elif len(episode) > 1:
        episode = "e" + episode

    elements = tree.xpath('//div[@class="post"]/h2/a/@href')
    #print elements
    detail_url = None
    for i in elements:
        #print i
        if "180p" in i:
            detail_url = None
            break
        elif (title in i) and (episode in i):
            logger.info("Found title %s episode %s in %s" %
                         (title, episode, i))
            # print "found title %s episode %s in %s" % (title,
            #                                            elements[index], i)
            detail_url = i
            break
    else:
        logger.info("Did not find title %s episode %s in %s" %
                     (title, episode, site_url))

    if detail_url is None:
        return None
    else:
        logger.debug("Trying to load webpage: %s" % (detail_url))
        try:
            raw_page = urllib.urlopen(detail_url)
            data = raw_page.read()
            raw_page.close()
        except IOError as e:
            logger.error("Could not find page %s"
                         % (detail_url))
            raise e

        tree = html.fromstring(data)
        # print data

        #authors = tree.xpath('//span[@class="author"]/text()')
        #print authors
        links = tree.xpath('//div[@class="comm_content"]/p/a/@href')
        #print links
        links_list = []
        for link in links:
            if ("filefactory" in link) and ("mp4" in link):
                #print link
                if link not in links_list:
                    links_list.append(link)

        return links_list

#        logger.debug("Found links %s" % (links))
#        # print links
#
#        supported_mirrors = ["multiup", "jheberg"]
#        provided_mirrors = []
#        for mirror in supported_mirrors:
#            for link in links:
#                if mirror in link:
#                    # print link
#                    provided_mirrors.append(link)
#
#        logger.debug("Built mirrors list: %s" % (provided_mirrors))






#print get_mirrors("baby", "8")
#print get_links("fairy", "235")
#print get_result_list([["series", "scnsrcMe", "izombie", "12"]])
