import requests, json, time


# TODO: essayer avec un bloc try pour la requete
class pyloadClient(object):
    """

    """
    def __init__(self, server_ip, username, password):
        self.server_ip = server_ip
        self.username = username
        self.password = password

        url  = "http://" + self.server_ip + ":8000/api/login"
        #print url

        payload={'username':self.username,'password':self.password}
        with requests.session() as self.session: 
            self.session.post(url, data=payload)

    def check_current_downloads_for_mirror(self, mirror_name):
        pass
        #r = self.session.post('http://172.17.0.57:8000/api/statusDownloads')
        #print r
        #print r.text

    def choose_link(self, links):
        """
        Choose the best link in the list (links)
        :param links
        :type links = list
        :return link
        """
        self.links = links

        for item in links:
            #print item
            if "uplea" in item:
                return item
            elif "1fichier" in item:
                return item
            elif "filefactory" in item:
                return item


    # TODO: Variabalise things and return value at the end
    def push_link(self, title, link):
        """

        """
        self.title = title
        self.link = link

        payload={'name': title, 'links':[self.link]}
        payloadJSON = {k: json.dumps(v) for k, v in payload.items()}

        url = "http://" + self.server_ip + ":8000/api/addPackage"

        r = self.session.post(url, data=payloadJSON)
        #r = s.post('http://172.17.0.57:8000/api/checkOnlineStatus', data=payloadJSON)
        #print r.text
        pid = r.text

        flag = True
        while flag == True:
            payload={'pid': pid}
            payloadJSON = {k: json.dumps(v) for k, v in payload.items()}

            url = "http://" + self.server_ip + ":8000/api/getPackageData"

            r = self.session.post(url, data=payloadJSON)
            print r
            #print r.text
            resp = r.json()
            #print resp
            status = resp["links"][0]["statusmsg"]
            #print status
            if status == "failed" or status == "offline" or status == "skipped":
                print "ERROR the links is dead"
                return "error"
                flag = False
                break
            elif status == "downloading" or status == "waiting" or status == "queued":
                print "SUCCESS Download is queued"
                return "success"
                flag = False
                break
            else:
                print "Waiting - reason: %s" % (status)
                time.sleep(2)





#linklist = ['http://uplea.com/dl/057843A511390A8', 'http://www.uptobox.com/84vwjp6bnxkd']
#push_to_pyload()

#client = pyloadClient("172.17.0.57", "user", "neutre")
#client.push_link("test", "http://uplea.com/dl/057843A511390A8")
#while True:
#    client.check_current_downloads_for_mirror(uplea)
#    time.sleep(20)
