import scrapy
from scrapy.utils.project import get_project_settings

class MonsterSpider(scrapy.Spider):
    name = 'monster'
    allowed_domains = ['monster.fr']
    settings = get_project_settings()

    def start_requests(self):
        return [scrapy.Request("https://login.monster.fr/Login/SignIn",
                               callback=self.login)]

    def login(self, response):
        return [scrapy.FormRequest.from_response(
            response,
            "https://login.monster.fr/Login/SignIn",
            formdata={'EmailAddress': self.settings.get('MONSTER_USERNAME'), 'Password': self.settings.get('MONSTER_PASSWORD'),
                        'AreCookiesEnabled': 'True'},
            callback=self.logged_in
        )]

    def logged_in(self, response):
        pass
