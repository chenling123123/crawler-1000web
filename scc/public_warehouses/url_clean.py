from urllib.parse import urljoin

class url_join():
    def joinurl(self,start_url,url):
        last_url=urljoin(start_url,url)
        return last_url
