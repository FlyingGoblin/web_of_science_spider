# -*- coding: utf-8 -*-

__author__ = 'flyinggoblin'

class Paper(object):
    def __init__(self, name, authers, journal, cited_times, cited_url=''):
        self.name = name
        self.authers = authers
        self.journal = journal
        self.cited_times = cited_times
        self.cited_url = cited_url

    def __str__(self):
        return 'Paper name: %s; Authers: %s; Journal: %s; Cited times: %d' \
               % (self.name, self.authers, self.journal, self.cited_times)

