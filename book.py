#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gingkg
@contact: sby2015666@163.com
@software: PyCharm
@file: book.py
@time: 2020/6/7
@desc: book class
"""


class Book:
    def __init__(self, title="龙枪编年史.第一部.秋暮之巨龙",
                 author="(美)Margaret Weis,(美)Tracey Hickman",
                 isbn="7-80160-118-1",
                 price=28.00,
                 number=None,
                 campus_location=None,
                 call_no=None,
                 return_book_position=None,
                 translator=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.number = number
        self.campus_location = campus_location
        self.return_book_position = return_book_position
        self.translator = translator
        self.call_no = call_no  # 索书号
        self.barcode_and_state_list = []  # 条码号和状态
        # for i in range(self.number):
        #     self.barcode_and_state_list.append({'barcode':get_barcode_no.get_barcode_no(),'state':"可借"})

    def get_book_info(self):
        info = {'title': self.title,
                'author': self.author,
                'ISBN': self.isbn,
                'price': self.price,
                'number': self.number,
                'campus_location': self.campus_location,
                'return_book_position': self.return_book_position,
                'call_no': self.call_no,
                'barcode_and_state_list': self.barcode_and_state_list,
                'translator': self.translator
                }
        return info

    def print_book_info(self):
        print('---------------------------------------------------------------------------------------')
        print("书名："+self.title)
        if self.translator is None:
            print("作者："+self.author)
        else:
            print("作者："+self.author+"原著 "+self.translator+"译")
        if self.call_no is not None:
            print("索书号："+self.call_no)
        if self.number is not None:
            print("册数：" + str(self.number))
            print("--------------------------------------------")
            print("条码号          | 状态")
            print("--------------------------------------------")
            for i in range(self.number):
                print(self.barcode_and_state_list[i]['barcode']+"         | "+self.barcode_and_state_list[i]['state'])
            print("--------------------------------------------")
        print("ISBN："+self.isbn)
        print("定价：CNY"+str(self.price))
        if self.campus_location is not None:
            print("馆藏地："+self.campus_location)
        if self.return_book_position is not None:
            print("还书地点："+self.return_book_position)
        print('---------------------------------------------------------------------------------------')


if __name__ == "__main__":
    book1 = Book(translator="朱学恒")
    book1_info = book1.get_book_info()
    book1.print_book_info()
