# -*- coding: utf-8 -*-

__author__ = 'flyinggoblin'

class Paper(object):
    def __init__(self, title, authers, journal, year, cited_times, cited_url=''):
        self.title = title
        self.authers = authers
        self.journal = journal
        self.year = year
        self.cited_times = cited_times
        self.cited_url = cited_url

    def __str__(self):
        return 'Paper name: %s; Authers: %s; Journal: %s; Year: %d; Cited times: %d' \
               % (self.title, self.authers, self.journal, self.year, self.cited_times)
