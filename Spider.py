# -*- coding: utf-8 -*-

__author__ = 'flyinggoblin'

from re import findall

import requests
from bs4 import BeautifulSoup


class Spider(object):
    def __init__(self, sid, paper_name, start_year, end_year):
        self.hearders = {
            'Origin': 'https://apps.webofknowledge.com',
            'Referer': 'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=R1ZsJrXOFAcTqsL6uqh&preferencesSaved=',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.form_data = {
            'fieldCount': 2,
            'action': 'search',
            'product': 'WOS',
            'search_mode': 'GeneralSearch',
            'SID': sid,
            'max_field_count': 25,
            'formUpdated': 'true',
            'value(input1)': paper_name,
            'value(select1)': 'SO',
            'value(hidInput1)': '',
            'value(bool_1_2)': 'AND',
            'value(input2)': str(start_year) + '-' + str(end_year),
            'value(select2)': 'PY',
            'value(hidInput2)': '',
            'limitStatus': 'collapsed',
            'ss_lemmatization': 'On',
            'ss_spellchecking': 'Suggest',
            'SinceLastVisit_UTC': '',
            'period': 'Range Selection',
            'range': 'ALL',
            'startYear': '1900',
            'endYear': '2016',
            'update_back2search_link_param': 'yes',
            'ssStatus': 'display:none',
            'ss_showsuggestions': 'ON',
            'ss_query_language': 'auto',
            'ss_numDefaultGeneralSearchFields': 1,
            'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A'
        }
        self.form_data2 = {
            'product': 'WOS',
            'prev_search_mode': 'CombineSearches',
            'search_mode': 'CombineSearches',
            'SID': sid,
            'action': 'remove',
            'goToPageLoc': 'SearchHistoryTableBanner',
            'currUrl': 'https://apps.webofknowledge.com/WOS_CombineSearches_input.do?SID=' + sid + '&product=WOS&search_mode=CombineSearches',
            'x': 48,
            'y': 9,
            'dSet': 1
        }


    def craw(self, root_url):
        try:
            s = requests.Session()
            r = s.post(root_url, data=self.form_data, headers=self.hearders)
            soup = BeautifulSoup(r.text, 'html.parser')
            result_article = soup.find_all('input', value="DocumentType_ARTICLE")
            if result_article == []:
                article_num = 0
            else:
                article_num = int(findall(r"\d+", result_article[0].text.replace(',', ''))[0])
            result_review = soup.find_all('input', value="DocumentType_REVIEW")
            if result_review == []:
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
        except Exception as e:
            # 出现错误，再次try，以提高结果成功率
            try:
                s = requests.Session()
                r = s.post(root_url, data=self.form_data, headers=self.hearders)
                soup = BeautifulSoup(r.text, 'html.parser')
                result_article = soup.find_all('input', value="DocumentType_ARTICLE")
                if result_article == []:
                    article_num = 0
                else:
                    article_num = int(findall(r"\d+", result_article[0].text.replace(',', ''))[0])
                result_review = soup.find_all('input', value="DocumentType_REVIEW")
                if result_review == []:
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

            except Exception as e:
                print(e)
                a_and_r = 0
                refer_num = 0
                flag = 1
                error = str(e)
        return a_and_r, refer_num, flag, error
