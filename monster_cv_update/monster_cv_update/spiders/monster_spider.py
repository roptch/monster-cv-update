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
        text_tags = Selector(response=response).xpath('//form[@id="form0"]//input[@type="text" and @name and @value]').extract()
        for text_tag in text_tags:
            name = Selector(text=text_tag).xpath('//input/@name').extract()[0]
            value = Selector(text=text_tag).xpath('//input/@value').extract()[0]
            form_data[name] = value
        select_tags = Selector(response=response).xpath('//form[@id="form0"]//select[@name]').extract()
        for select_tag in select_tags:
            name = Selector(text=select_tag).xpath('//select/@name').extract()[0]
            option_tags = Selector(text=select_tag).xpath('//select//option[@selected and @value]/@value').extract()
            if len(option_tags) > 0:
                value = option_tags[0]
            else:
                value = Selector(text=select_tag).xpath('//select//option[@value]/@value').extract()[0]
            print '%s: %s' % (name, value)

        req = scrapy.FormRequest(
            'http://mon.monster.fr/Resume/Settings/%s'
                % self.settings.get('MONSTER_CV_HASH'),
            formdata=form_data,
            callback=self.check_update
        )
        self.log(req.headers, loglevel=log.WARNING)

        return [req]

    def check_update(self, response):
        self.log('Done.', loglevel=log.INFO)
