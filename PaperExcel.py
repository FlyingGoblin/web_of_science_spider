# -*- coding: utf-8 -*
import xlrd
import xlwt

from Paper import Paper
from My_enum import enum

__author__ = 'flyinggoblin'

TABLE_TITLE = enum('TITLE',
                   'JOURNAL',
                   'AUTHORS',
                   'YEAR',
                   'CITE_NUMBER',
                   'OTHER_CITE_NUMBER',
                   'CITE_TITLE',
                   'CITE_JOURNAL',
                   'CITE_AUTHOR',
                   'CITE_YEAR',
                   'IS_SCI',
                   'IS_OTHER_CITE')

TABLE_TITLE_CN = {
    TABLE_TITLE.TITLE: u'题目',
    TABLE_TITLE.JOURNAL: u'收录',
    TABLE_TITLE.AUTHORS: u'作者',
    TABLE_TITLE.YEAR: u'时间(年)',
    TABLE_TITLE.CITE_NUMBER: u'引用',
    TABLE_TITLE.OTHER_CITE_NUMBER: u'他引',
    TABLE_TITLE.CITE_TITLE: u'引用文章',
    TABLE_TITLE.CITE_JOURNAL: u'引用文章期刊',
    TABLE_TITLE.CITE_AUTHOR: u'引用作者',
    TABLE_TITLE.CITE_YEAR: u'引用时间(年)',
    TABLE_TITLE.IS_SCI: u'是否SCI引用',
    TABLE_TITLE.IS_OTHER_CITE: u'是否他引',
}


class PaperExcel(object):
    def __init__(self, excel_path):
        self.__excel_path = excel_path
        self.__excel = xlwt.Workbook()
        self.__table = self.__excel.add_sheet('sheet 1')
        self.__current_row = 1
        self.__write_table_title()

    def __write_table_title(self):
        for col in TABLE_TITLE_CN:
            self.__table.write(0, col, TABLE_TITLE_CN[col])

    def write_paper_cite(self, paper, cites):
        row_start_paper = row_paper = self.__current_row
        # 论文本身
        self.__table.write(row_paper, 0, paper.title)
        self.__table.write(row_paper, 1, paper.journal)
        for author in paper.authors:
            self.__table.write(row_paper, 2, author)
            row_paper += 1
        # 引用信息
        row_cite = self.__current_row
        self.__table.write(row_cite, 3, paper.year)
        self.__table.write(row_cite, 4, len(cites))
        other_cite_count = 0
        row_cite_end = row_cite
        for cite in cites:
            row_cite = row_start_cite = row_cite_end
            self.__table.write(row_cite, 6, cite.title)
            self.__table.write(row_cite, 7, cite.journal)
            for author in cite.authors:
                self.__table.write(row_cite, 8, author)
                row_cite += 1
            row_cite_end = row_cite
            row_cite = row_start_cite
            self.__table.write(row_cite, 9, cite.year)
            self.__table.write(row_cite, 10, 1)
            if paper.is_self_cite(cite):
                self.__table.write(row_cite, 11, 0)
            else:
                self.__table.write(row_cite, 11, 1)
                other_cite_count += 1
        self.__current_row = max(row_paper, row_cite_end)
        self.__table.write(row_start_paper, 5, other_cite_count)
        self.__excel.save(self.__excel_path)

    @classmethod
    def read_title_list(cls, excel_path):
        title_data = xlrd.open_workbook(excel_path)
        table = title_data.sheets()[0]
        return table.col_values(0)
