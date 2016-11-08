# -*- coding: utf-8 -*-
from re import findall

import requests
from bs4 import BeautifulSoup
from Paper import Paper

__author__ = 'flyinggoblin'

COLLECTION_SCI = 0
COLLECTION_SSCI = 1
COLLECTION_AHCI = 2
COLLECTION_ISTP = 3
COLLECTION_ISSHP = 4
COLLECTION_ESCI = 5
COLLECTION_CCR = 6  # 化学
COLLECTION_IC = 7  # 化学

COLLECTION_LIST = [COLLECTION_SCI, COLLECTION_SSCI, COLLECTION_AHCI, COLLECTION_ISTP, COLLECTION_ISSHP, COLLECTION_ESCI, COLLECTION_CCR, COLLECTION_IC]

COLLECTION_CN = {
    COLLECTION_SCI: 'SCI',
    COLLECTION_SSCI: 'SSCI',
    COLLECTION_AHCI: 'AHCI',
    COLLECTION_ISTP: 'ISTP',
    COLLECTION_ISSHP: 'ISSHP',
    COLLECTION_ESCI: 'ESCI',
    COLLECTION_CCR: 'CCR',
    COLLECTION_IC: 'IC'
}


class Spider(object):
    def __init__(self):
        self.__root = 'http://apps.webofknowledge.com'
        self.__search_root = 'https://apps.webofknowledge.com/WOS_GeneralSearch.do'
        self.__sid = self.get_session_id()
        self.__start_year = 1900
        self.__end_year = 2016
        self.__collection_enable_list = [False] * len(COLLECTION_LIST)

    @property
    def __hearder(self):
        hearder = dict()
        hearder['Origin'] = self.__root
        hearder['Referer'] = 'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?SID='\
                             + self.__sid \
                             + '&product=WOS&search_mode=GeneralSearch'
        hearder['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                                + " Chrome/50.0.2661.94 Safari/537.36"
        hearder['Content-Type'] = 'application/x-www-form-urlencoded'
        return hearder

    @property
    def __form_data(self):
        base_form = dict()
        base_form['fieldCount'] = 1
        base_form['action'] = 'search'
        base_form['product'] = 'WOS'
        base_form['search_mode'] = 'GeneralSearch'
        base_form['SID'] = self.__sid
        base_form['max_field_count'] = 25
        base_form['formUpdated'] = 'true'
        base_form['rs_sort_by'] = 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A'
        base_form['period'] = 'Range Selection'
        base_form['range'] = 'ALL'
        base_form['startYear'] = self.__start_year
        base_form['endYear'] = self.__end_year
        # base_form['ss_lemmatization'] = 'On'
        # base_form['ss_spellchecking'] = 'Suggest'
        # base_form['limitStatus'] = 'expanded'
        # base_form['update_back2search_link_param'] = 'yes'
        # base_form['ssStatus'] = 'display:none'
        # base_form['ss_showsuggestions'] = 'ON'
        # base_form['ss_numDefaultGeneralSearchFields'] = 1

        # 会议信息
        base_form['editions'] = []
        for index in range(len(self.__collection_enable_list)):
            collection_flag = self.__collection_enable_list[index]
            if collection_flag:
                base_form['editions'].append(COLLECTION_CN[index])
        return base_form

    def __do_search_paper(self, paper_name):
        if not any(self.__collection_enable_list):
            print('enable at least one collection first!')
            error = 'no collection'
            return error
        form_data = self.__form_data
        form_data['value(input1)'] = paper_name
        form_data['value(select1)'] = 'TI'
        s = requests.Session()
        r = s.post(self.__search_root, data=form_data, headers=self.__hearder)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup)
        paper = None
        # 在搜索结果第一页中找title相等的论文,第一页没有匹配的就算找不到
        for all_paper_info in soup.select('div.search-results-item'):
            # title
            title = all_paper_info.select('a.smallV110 value')[0].get_text().replace(' ', '|||')
            title = title.strip()
            title = title.replace('|||', ' ')
            if not ''.join(filter(str.isalnum, title)).lower() == ''.join(filter(str.isalnum, paper_name)).lower():
                continue
            else:
                if paper:
                    error = 'more than one paper founded'
                    return paper, error
            # Times Cited
            cited_times_str = findall(r'\d', all_paper_info.select('div.search-results-data-cite')[0].get_text())[0]
            cited_times = int(cited_times_str)
            if cited_times > 0:
                cited_url = self.__root + all_paper_info.select('div.search-results-data-cite a')[0]['href']
            else:
                cited_url = ''

            paper_url = self.__root + all_paper_info.select('a.smallV110')[0]['href']
            r = s.get(paper_url)
            paper_soup = BeautifulSoup(r.text, 'html.parser')
            # journal
            journal = paper_soup.select('p.sourceTitle value')[0].get_text()
            authors = year = ids = None
            for possible_field in paper_soup.select('p.FR_field'):
                possible_str = possible_field.get_text()
                if not authors and possible_str.find('By:') >= 0 or possible_str.find(u'作者:') >= 0:
                    authors = findall('(?<=\\()(.+?)(?=\\))', possible_str)
                if not year and possible_str.find('Published:') >= 0 or possible_str.find(u'出版年:') >= 0:
                    year_str = findall(r'\d+', possible_str)[-1]
                    year = int(year_str)
                if not ids and possible_str.find('IDS Number:') >= 0 or possible_str.find(u'IDS 号:') >= 0:
                    ids = findall(r'\w+', possible_str)[-1]
            paper = Paper(title, authors, journal, year, ids, cited_times, cited_url)
        if paper:
            error = 'no error'
        else:
            error = 'no such paper'
        return paper, error

    def search_paper(self, paper_name):
        try:
            paper, error = self.__do_search_paper(paper_name)
        except Exception:
            # 出现错误，再次try，以提高结果成功率
            try:
                paper, error = self.__do_search_paper(paper_name)
            except Exception as e:
                paper = None
                error = e
                print(e)
        return paper, error

    def get_session_id(self):
        s = requests.get(self.__root)
        sid = findall(r'SID=\w+&', s.url)[0].replace('SID=', '').replace('&', '')
        return sid

    def enable_collection(self, collection):
        if collection in COLLECTION_LIST:
            self.__collection_enable_list[collection] = True
        else:
            print('no such collection')

    def disable_collection(self, collection):
        if collection in COLLECTION_LIST:
            self.__collection_enable_list[collection] = False
        else:
            print('no such collection')

    def __do_search_cite_papers(self, paper, collection):
        cite_papers = []
        cite_url = paper.cited_url
        # 获得引用页面
        s = requests.Session()
        r = s.get(cite_url)
        cite_soup = BeautifulSoup(r.text, 'html.parser')
        if collection is not None:
            span = cite_soup.select('span#CAScorecard_count_WOS' + COLLECTION_CN[collection])[0]
            if int(span.get_text()) is 0:
                return cite_papers, cite_url
            else:
                cite_url = self.__root + '/' + span.a['href'].replace(';jsessionid=' + r.cookies['JSESSIONID'], '')
                r = s.get(cite_url)
                cite_soup = BeautifulSoup(r.text, 'html.parser')
        # 获得引用论文信息
        while True:  # 翻页直到最后一页
            papers_info = cite_soup.select('div.search-results-item')
            for paper_info in papers_info:
                title = paper_info.select('a.smallV110 value')[0].get_text().replace(' ', '|||')
                title = title.strip()
                title = title.replace('|||', ' ')
                # Times Cited
                cited_times_str = findall(r'\d', paper_info.select('div.search-results-data-cite')[0].get_text())[0]
                cited_times = int(cited_times_str)
                if cited_times > 0:
                    cited_url = self.__root + paper_info.select('div.search-results-data-cite a')[0]['href']
                else:
                    cited_url = ''

                paper_url = self.__root + paper_info.select('a.smallV110')[0]['href']
                r = s.get(paper_url)
                paper_soup = BeautifulSoup(r.text, 'html.parser')
                # journal
                journal = paper_soup.select('p.sourceTitle value')[0].get_text()
                # authors, years & IDS
                authors = year = ids = None
                for possible_field in paper_soup.select('p.FR_field'):
                    possible_str = possible_field.get_text()
                    if not authors and possible_str.find('By:') >= 0 or possible_str.find(u'作者:') >= 0:
                        authors = findall('(?<=\\()(.+?)(?=\\))', possible_str)
                    if not year and possible_str.find('Published:') >= 0 or possible_str.find(u'出版年:') >= 0:
                        year_str = findall(r'\d+', possible_str)[-1]
                        year = int(year_str)
                    if not ids and possible_str.find('IDS Number:') >= 0 or possible_str.find(u'IDS 号:') >= 0:
                        ids = findall(r'\w+', possible_str)[-1]
                paper = Paper(title, authors, journal, year, ids, cited_times, cited_url)
                print(paper)
                cite_papers.append(paper)
            # 翻页直到最后一页
            total_page = int(cite_soup.select('span[id="pageCount.top"]')[0].get_text())
            current_page = int(cite_soup.select('input.goToPageNumber-input')[0]['value'])
            print('%d of % d' % (current_page, total_page))
            if current_page < total_page:
                r = s.get(cite_soup.select('a.paginationNext')[0]['href'])
                cite_soup = BeautifulSoup(r.text, 'html.parser')
            else:
                break
        return cite_papers, cite_url

    def search_cite_papers(self, paper, collection=None):  # 目前一次只支持查一种会议类型和全数据库
        cite_papers = None
        if paper is None:
            print('invalid paper')
            cite_url = None
            error = 'invalid paper'
        elif paper.cited_times is 0:
            print('no cite')
            cite_url = paper.cited_url
            cite_papers = []
            error = 'no error'
        else:
            try:
                cite_papers, cite_url = self.__do_search_cite_papers(paper, collection)
                error = 'no error'
            except Exception:
                # 出现错误，再次try，以提高结果成功率
                try:
                    cite_papers, cite_url = self.__do_search_cite_papers(paper, collection)
                    error = 'no error'
                except Exception as e:
                    error = e
                    cite_url = paper.cited_url
                    print(e)
        return cite_papers, cite_url, error
