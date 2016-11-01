# -*- coding: utf-8 -*-

__author__ = 'flyinggoblin'

from re import findall

import requests
from bs4 import BeautifulSoup

EDITIONS_SCI = 1
EDITIONS_SSCI = 2
EDITIONS_AHCI = 3
EDITIONS_ISTP = 4
EDITIONS_ISSHP = 5
EDITIONS_ESCI = 6
EDITIONS_CCR = 7
EDITIONS_IC = 8

EDITIONS_LIST = [EDITIONS_SCI, EDITIONS_SSCI, EDITIONS_AHCI, EDITIONS_ISTP, EDITIONS_ISSHP, EDITIONS_ESCI, EDITIONS_CCR, EDITIONS_IC]

class Spider(object):
    def __init__(self, sid, root_url):
        self.__sid = sid
        self.__root_url = root_url
        self.__start_year = 1999
        self.__end_year = 2016
        self.__hearder = {
            'Origin': 'https://apps.webofknowledge.com',
            'Referer': 'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?SID='
                       + str(sid)
                       + '&product=WOS&search_mode=GeneralSearch&errorQid=6',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          + " Chrome/50.0.2661.94 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.__editions_enable_list = [True, True, True, True, True, True, True, True]

    @property
    def __form_data(self):
        base_form = {
            'fieldCount': 1,
            'action': 'search',
            'product': 'WOS',
            'search_mode': 'GeneralSearch',
            'SID': self.__sid,
            'max_field_count': 25,
            'formUpdated': 'true',
            'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A',
            'period': 'Range Selection',
            'range':'ALL',
            'ss_lemmatization': 'On',
            'ss_spellchecking': 'Suggest',
            'limitStatus': 'expanded',
            'startYear': self.__start_year,
            'endYear': self.__end_year,
            'update_back2search_link_param': 'yes',
            'ssStatus': 'display:none',
            'ss_showsuggestions': 'ON',
            'ss_numDefaultGeneralSearchFields':1
            # 不一定必要的东西们
             ,'max_field_notice': '',
            'input_invalid_notice': '',
            'exp_notice': '',
            'input_invalid_notice_limits': '',
            'sa_params': 'WOS | | '+self.__sid+'|https://apps.webofknowledge.com:443|'
        }
        # 会议信息
        base_form['editions'] = ['SCI','SSCI']
        # for editions_flag in self.__editions_enable_list:
        #     if editions_flag:
        #         base_form['editions'] = ['SCI','SSCI']


        # value(input1):A Distributed Computational Cognitive Model for Object Recognition
        # value(select1):TS
        #
        # value(hidInput1):
        # SinceLastVisit_UTC:
        # SinceLastVisit_DATE:
        # ss_query_language:

        return base_form

    def __do_search_paper(self, paper_name):
        form_data = self.__form_data
        form_data['value(input1)'] = paper_name
        form_data['value(select1)'] = 'TS'
        s = requests.Session()
        r = s.post(self.__root_url, data=form_data, headers=self.__hearder)
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
