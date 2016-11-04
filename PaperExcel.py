# -*- coding: utf-8 -*-
import xlrd
import xlwt

from Paper import Paper

__author__ = 'flyinggoblin'


class PaperExcel(object):
    def __init__(self, excel_path):
        self.__excel_path = excel_path
        self.__excel = xlwt.Workbook()
        self.__table = self.__excel.add_sheet('sheet 1')
        self.__current_row = 1
        self.__table.write(0, 0, u'题目')
        self.__table.write(0, 1, u'收录')
        self.__table.write(0, 2, u'作者')
        self.__table.write(0, 3, u'时间(年)')
        self.__table.write(0, 4, u'引用')
        self.__table.write(0, 5, u'他引')
        self.__table.write(0, 6, u'引用文章')
        self.__table.write(0, 7, u'引用文章期刊')
        self.__table.write(0, 8, u'引用作者')
        self.__table.write(0, 9, u'引用时间(年)')
        self.__table.write(0, 10, u'是否SCI引用')
        self.__table.write(0, 11, u'是否他引')

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
