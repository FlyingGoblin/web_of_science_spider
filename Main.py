# -*- coding: utf-8 -*-
from Spider import Spider, COLLECTION_SCI
from PaperExcel import PaperExcel


if __name__ == "__main__":
    error_file_path = './error.txt'
    cite_url_file_path = './cite_url.txt'
    paper_title_list = PaperExcel.read_title_list('./test.xlsx')
    paper_excel_writer = PaperExcel('./result.xlsx')
    FIT3_524_spider = Spider()
    FIT3_524_spider.enable_collection(COLLECTION_SCI)
    error_file = open(error_file_path, 'w')
    cite_url_file = open(cite_url_file_path, 'w')
    for paper_title in paper_title_list:
        paper, error = FIT3_524_spider.search_paper(paper_title)
        if not error == 'no error':
            error_file.write('%s: %s\n' % (paper.title, error))  # 记录错误列表
            print(error)
            continue
        print('Successfully get paper:')
        print(paper)
        cite_papers, cite_url, error = FIT3_524_spider.search_cite_papers(paper, COLLECTION_SCI)
        cite_url_file.write('%s: %s\n' % (paper.title, cite_url))
        if not error == 'no error':
            error_file.write('%s: %s\n' % (paper.title, error))  #  记录错误列表
            print(error)
            continue
        print('Cited paper count: %d' % len(cite_papers))
        paper_excel_writer.write_paper_cite(paper, cite_papers)
    error_file.close()
    cite_url_file.close()