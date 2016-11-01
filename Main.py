
from Spider import Spider
from re import findall

import requests
import bs4

if __name__=="__main__":
    root_url = 'https://apps.webofknowledge.com/WOS_GeneralSearch.do'
    # sid='W1OZtZW2eSwnTmvSLev'

    root = 'http://www.webofknowledge.com/'
    s = requests.get(root)
    print(s.url)
    sid = findall(r'SID=\w+&', s.url)[0].replace('SID=', '').replace('&', '')
    obj_spider = Spider(sid, root_url)
    ar, ref, fl, er = obj_spider.search_paper('A Distributed Computational Cognitive Model for Object Recognition')
    print(ar)
    print(ref)
    print(fl)
    print(er)
