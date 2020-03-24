
class EduWebsites:
    def __init__(self):
        self.url_name_dict = {}
        self.name_url_dict = {}
        with open('../resources/valid_edu_websites.csv') as url_list_file:
            self.urls = [url.strip() for url in url_list_file.read().split(',')]
        for url in self.urls:
            name = url.split('/')[2].split('.')[0]
            self.url_name_dict[url] = name
            self.name_url_dict[name] = url

    def get_name(self, url):
        return self.url_name_dict[url]

    def get_url(self, name):
        return self.name_url_dict[name]


eduWebsites = EduWebsites()