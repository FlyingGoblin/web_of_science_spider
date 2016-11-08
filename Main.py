# -*- coding: utf-8 -*-
from Spider import Spider, COLLECTION_SCI
from LiuYongjinExcel import LiuYongjinExcel


if __name__ == "__main__":
    error_file_path = './error.txt'
    cite_url_file_path = './cite_url.xlsx'
    paper_list = LiuYongjinExcel.read_title_list_form_per_result('./PaperRecord_2016-10-25-cy.xlsx')
    paper_excel_writer = LiuYongjinExcel('./result.xlsx')
    FIT3_524_spider = Spider()
    FIT3_524_spider.enable_collection(COLLECTION_SCI)
    error_file = open(error_file_path, 'w')
    for paper_title, author_tag in paper_list:
        paper, error = FIT3_524_spider.search_paper(paper_title)
        if not error == 'no error':
            error_file.write('%s: %s\n' % (paper_title, error))  # 记录错误列表
            print(error)
            continue
        print('Successfully get paper:')
        print(paper)
        cite_papers, cite_url, error = FIT3_524_spider.search_cite_papers(paper, COLLECTION_SCI)
        if not error == 'no error':
            error_file.write('%s: %s\n' % (paper.title, error))  # 记录错误列表
            print(error)
            continue
        LiuYongjinExcel.write_cite_url(cite_url_file_path, paper, cite_url)
        print('Cited paper count: %d' % len(cite_papers))
        paper_excel_writer.write_paper_cite(paper, cite_papers, author_tag)
    error_file.close()