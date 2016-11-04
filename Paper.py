# -*- coding: utf-8 -*-

__author__ = 'flyinggoblin'


class Paper(object):
    def __init__(self, title, authors, journal, year, cited_times, cited_url=''):
        self.title = title
        self.authors = authors
        self.journal = journal
        self.year = year
        self.cited_times = cited_times
        self.cited_url = cited_url

    def __str__(self):
        return 'Paper name: %s; Authors: %s; Journal: %s; Year: %d; Cited times: %d' \
               % (self.title, self.authors, self.journal, self.year, self.cited_times)

    def is_self_cite(self, cite_paper):
        # 这里简单比较了，因为目前都是web of science 爬下来的作者
        # 以后可能加入更严谨的比较方式
        cite_authors = [''.join(filter(str.isalnum, a)).lower() for a in cite_paper.authors]
        for author in self.authors:
            if ''.join(filter(str.isalnum, author)).lower() in cite_authors:
                return True
        return False
