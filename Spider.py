# -*- coding: utf-8 -*-

__author__ = 'flyinggoblin'

from re import findall

import requests
from bs4 import BeautifulSoup

COLLECTION_SCI = 0
COLLECTION_SSCI = 1
COLLECTION_AHCI = 2
COLLECTION_ISTP = 3
COLLECTION_ISSHP = 4
COLLECTION_ESCI = 5
COLLECTION_CCR = 6
COLLECTION_IC = 7

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
        self.__root = 'http://www.webofknowledge.com/'
        self.__search_root = 'https://apps.webofknowledge.com/WOS_GeneralSearch.do'
        self.__sid = self.get_session_id()
        self.__start_year = 1999
        self.__end_year = 2016
        self.__collection_enable_list = [False] * len(COLLECTION_LIST)

    @property
    def __hearder(self):
        hearder = dict()
        hearder['Origin'] = self.__root
        hearder['Referer'] = 'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?SID='\
                             + self.__sid \
                             + '&product=WOS&search_mode=GeneralSearch'
        hearder['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"\
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
        form_data['value(select1)'] = 'TS'
        s = requests.Session()
        r = s.post(self.__search_root, data=form_data, headers=self.__hearder)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup)
        result_article = soup.find_all('input', value="DocumentType_ARTICLE")
        if result_article:
            article_num = 0
        else:
            article_num = int(findall(r"\d+", result_article[0].text.replace(',', ''))[0])
        result_review = soup.find_all('input', value="DocumentType_REVIEW")
        if result_review:
            review_num = 0
        else:
            review_num = int(findall(r"\d+", result_review[0].text.replace(',', ''))[0])
        a_and_r = article_num + review_num
        report_link = soup.find('a', alt="View Citation Report")
        true_link = "https://apps.webofknowledge.com" + report_link['href']
        r2 = s.get(true_link)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        refer = soup2.find_all('span', id="CR_HEADER_3")
        refer_num = int(findall(r"\d+", refer[0].text)[0])
        flag = 0
        error = 'no error'
        return a_and_r, refer_num, flag, error

    def search_paper(self, paper_name):
        try:
            a_and_r, refer_num, flag, error = self.__do_search_paper(paper_name)
        except Exception as e:
            # 出现错误，再次try，以提高结果成功率
            try:
                a_and_r, refer_num, flag, error = self.__do_search_paper(paper_name)
            except Exception as e:
                print(e)
                a_and_r = 0
                refer_num = 0
                flag = 1
                error = str(e)
        return a_and_r, refer_num, flag, error

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

