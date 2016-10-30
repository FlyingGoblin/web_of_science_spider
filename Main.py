
from Spider import Spider
from re import findall

import requests
import bs4

if __name__=="__main__":
    root_url = 'https://apps.webofknowledge.com/WOS_GeneralSearch.do'
    # sid='W1OZtZW2eSwnTmvSLev'

    root = 'http://www.webofknowledge.com/'
    s = requests.get(root)
    sid = findall(r'SID=\w+&', s.url)[0].replace('SID=', '').replace('&', '')
    obj_spider = Spider(sid, 'A Distributed Computational Cognitive Model for Object Recognition', 1993, 2016)
    ar, ref, fl, er = obj_spider.craw(root_url)
    print(ar)
    print(ref)
    print(fl)
    print(er)
