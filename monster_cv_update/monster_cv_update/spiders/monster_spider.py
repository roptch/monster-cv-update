# -*- coding: utf-8 -*-

import HTMLParser
import scrapy
from scrapy import log
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings

class MonsterSpider(scrapy.Spider):
    name = 'monster'
    allowed_domains = ['monster.fr']
    settings = get_project_settings()

    def start_requests(self):
        return [scrapy.Request("https://login.monster.fr/Login/SignIn",
                               callback=self.login)]

    def login(self, response):
        return [scrapy.FormRequest(
            "https://login.monster.fr/Login/SignIn",
            formdata={
                'EmailAddress': self.settings.get('MONSTER_USERNAME'),
                'Password': self.settings.get('MONSTER_PASSWORD'),
                'AreCookiesEnabled': 'True'},
            callback=self.logged_in
        )]

    def logged_in(self, response):
        return [scrapy.Request(
            'http://mon.monster.fr/Resume/Settings/%s'
                % self.settings.get('MONSTER_CV_HASH'),
            callback=self.update_cv
        )]

    def update_cv(self, response):
        form_data = {}

        # Extracting <input> tags name/value
        text_tags = Selector(response=response).xpath('//form[@id="form0"]//input[(@type="text" or @type="hidden" or (@type="checkbox" and @checked) or (@type="radio" and @checked)) and @name and @value]').extract()
        for text_tag in text_tags:
            name = Selector(text=text_tag).xpath('//input/@name').extract()[0]
            value = Selector(text=text_tag).xpath('//input/@value').extract()[0]
            if name not in form_data:
                form_data[name] = value

        # Extracting <select> tags name/value
        select_tags = Selector(response=response).xpath('//form[@id="form0"]//select[@name]').extract()
        for select_tag in select_tags:
            name = Selector(text=select_tag).xpath('//select/@name').extract()[0]
            option_tags = Selector(text=select_tag).xpath('//select//option[@selected and @value]/@value').extract()
            if len(option_tags) > 0:
                value = option_tags[0]
            else:
                value = Selector(text=select_tag).xpath('//select//option[@value]/@value').extract()[0]
            if name not in form_data:
                form_data[name] = value

        form_data['Command'] = 'update'

        # Creating the request to reinject the form data
        req = scrapy.FormRequest(
            'http://mon.monster.fr/Resume/Settings/%s'
                % self.settings.get('MONSTER_CV_HASH'),
            formdata=form_data,
            callback=self.check_update
        )
        return [req]

    def check_update(self, response):
        if 'erreur' in response.body:
            self.log('Fail :\\')
        else:
            self.log('Update success!')
