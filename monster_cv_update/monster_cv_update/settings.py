# -*- coding: utf-8 -*-

# Scrapy settings for monster_cv_update project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'monster_cv_update'

SPIDER_MODULES = ['monster_cv_update.spiders']
NEWSPIDER_MODULE = 'monster_cv_update.spiders'

MONSTER_USERNAME = '' # Fill your monster username here
MONSTER_PASSWORD = '' # Fill your monster password here

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'monster_cv_update (+http://www.yourdomain.com)'
