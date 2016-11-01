
from Spider import Spider, COLLECTION_SCI
from Paper import Paper

import requests
import bs4

if __name__=="__main__":
    FIT3_524_spider = Spider()
    FIT3_524_spider.enable_collection(COLLECTION_SCI)
    paper, error = FIT3_524_spider.search_paper('A Distributed Computational Cognitive Model for Object Recognition')
    print(paper)
    print(error)
