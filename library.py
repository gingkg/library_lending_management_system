#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gingkg
@contact: sby2015666@163.com
@software: PyCharm
@file: library.py
@time: 2020/6/7
@last updated date: 2020/6/14
@desc: library class
"""

import os
import pickle
from book import Book
from datetime import datetime
from datetime import timedelta
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pyplot import MultipleLocator
import copy
import re
import time

IMAGE_SAVE_PATH = 'pictures/'


class Library:
    def __init__(self, name="西北工业大学(友谊校区)图书馆",
                 location="陕西省西安市莲湖区西北工业大学",
                 return_book_position="友谊校区一楼还书处",
                 max_borrow_time_limit=30):
        self.name = name
        self.location = location
        self.return_book_position = return_book_position
        self.number_of_collection = 0
        self.number_of_type = 0
        self.max_borrow_time_limit = max_borrow_time_limit
        self.collection = {'title': [], 'author': [], 'isbn': [], 'book': []}  # 馆藏信息
        self.borrow_system = {'title': [], 'isbn': [], 'barcode': [], 'borrower': [],
                              'out_time': [], 'date_to_return': []}  # 只记录当前被借阅的书籍
        self.borrow_return_log = {'title': [], 'isbn': [], 'barcode': [], 'borrower': [],
                                  'out_time': [], 'return_time': []}  # 详细记录所有借阅信息，当还书的时候才会被记录
        self.borrower_set = set()
        self.load_cache()

    # 添加书籍
    def add_book(self, book=Book(),
                 campus_location="西馆书库四层南 社科图书库",
                 call_no="I712.4/W015-3/(1)",
                 number=3):
        print("正在向"+self.name+"添加《"+book.title+"》......")
        # 先查重
        try:
            index = self.collection['isbn'].index(book.isbn)
        except ValueError:
            book.number = number
            book.campus_location = campus_location
            book.return_book_position = self.return_book_position+"/"+campus_location
            book.call_no = call_no
            for i in range(number):
                book.barcode_and_state_list.append({'barcode': self.get_barcode_no(), 'state': "可借"})
            self.number_of_collection = self.number_of_collection + number
            self.number_of_type = self.number_of_type + 1
            self.collection['title'].append(book.title)
            self.collection['author'].append(book.author)
            self.collection['isbn'].append(book.isbn)
            self.collection['book'].append(book)
        else:
            print("《"+book.title+"》已存在于"+self.name)
            book.number = book.number + number
            for i in range(number):
                self.collection['book'][index].barcode_and_state_list\
                    .append({'barcode': self.get_barcode_no(), 'state': "可借"})
            self.number_of_collection = self.number_of_collection + number
        print(str(number)+"本《" + book.title + "》添加成功!")

    # 获取该图书馆的全局唯一识别码
    def get_barcode_no(self):
        file = "lib/"+self.name+"_barcode_no.pkl"
        if not os.path.exists(file):
            f = open(file, 'wb')
            barcode_dict = {'str': '0000000', 'int': 0}
            pickle.dump(barcode_dict, f)
            f.close()
        f = open(file, 'rb')
        barcode_dict = pickle.load(f)
        f.close()
        f = open(file, 'wb')
        barcode_dict['int'] = barcode_dict['int'] + 1
        barcode_dict['str'] = "{:0>7d}".format(barcode_dict['int'])
        pickle.dump(barcode_dict, f)
        f.close()
        return barcode_dict['str']

    # 加载信息
    def load_cache(self):
        file = "lib/" + self.name + "_cache.pkl"
        if not os.path.exists(file):
            f = open(file, 'wb')
            collection = {'title': [], 'author': [], 'isbn': [], 'book': []}
            borrow_system = {'title': [], 'isbn': [], 'barcode': [], 'borrower': [], 'out_time': [],
                             'date_to_return': []}
            borrow_return_log = {'title': [], 'isbn': [], 'barcode': [], 'borrower': [], 'out_time': [],
                                 'return_time': []}
            borrower_set = set()
            pickle.dump((collection, borrow_system, borrow_return_log, borrower_set,
                         self.name,self.location,self.return_book_position,self.number_of_collection,
                         self.number_of_type,self.max_borrow_time_limit), f)
            f.close()
        f = open(file, 'rb')
        try:
            self.collection, self.borrow_system, self.borrow_return_log, self.borrower_set, \
            self.name, self.location, self.return_book_position, self.number_of_collection,\
            self.number_of_type, self.max_borrow_time_limit = pickle.load(f)
        except ValueError:
            self.reset_cache()
        f.close()

    def save_cache(self):
        file = "lib/" + self.name + "_cache.pkl"
        f = open(file, 'wb')
        pickle.dump((self.collection, self.borrow_system, self.borrow_return_log, self.borrower_set,
                     self.name, self.location, self.return_book_position, self.number_of_collection,
                     self.number_of_type, self.max_borrow_time_limit), f)
        f.close()

    def reset_cache(self):
        file = "lib/" + self.name + "_cache.pkl"
        f = open(file, 'wb')
        collection = {'title': [], 'author': [], 'isbn': [], 'book': []}
        borrow_system = {'title': [], 'isbn': [], 'barcode': [], 'borrower': [], 'out_time': [],
                         'date_to_return': []}
        borrow_return_log = {'title': [], 'isbn': [], 'barcode': [], 'borrower': [], 'out_time': [],
                             'return_time': []}
        borrower_set = set()
        pickle.dump((collection, borrow_system, borrow_return_log, borrower_set,
                     self.name,self.location,self.return_book_position,self.number_of_collection,
                     self.number_of_type,self.max_borrow_time_limit), f)
        f.close()
        self.load_cache()

    # 输出馆藏目录
    def print_collection_index(self):
        print("**********************************************************************************")
        print("    "+self.name+"馆藏目录(index,皮一下我很开心)：")
        print("----------------------------------------------------------------------------------")

        for i, book in enumerate(self.collection['book']):
            if book.translator is None:
                print("{}、《{}》- {}著 - ISBN:{} - 索书号:{} - 馆藏复本：{}".format(i+1, book.title, book.author,
                                                                         book.isbn, book.call_no, book.number))
            else:
                print("{}、《{}》- {}著 {}译 - ISBN:{} - 索书号:{} - 馆藏复本：{}".format(i, book.title, book.author,
                                                                            book.translator, book.isbn, book.call_no,
                                                                            book.number))
        print("**********************************************************************************")

    def print_library_info(self):
        print("--------------------------------------------------------")
        print("馆名："+self.name)
        print("地址："+self.location)
        print("还书地点："+self.return_book_position)
        print("最大借阅期限："+str(self.max_borrow_time_limit)+"天")
        print("馆藏数量："+str(self.number_of_collection)+"本")
        print("--------------------------------------------------------")

    # 精确匹配查询
    def exact_match_query_book(self, way="title", keywords=['射雕英雄传.叁']):
        print('正在查询......')
        print('查询结果：')
        print('***********************************************************************************************')
        if "title" == way:
            for keyword in keywords:
                indexs = [i for i,x in enumerate(self.collection['title']) if x == keyword]
                if indexs:
                    for index in indexs:
                        self.collection['book'][index].print_book_info()
                else:
                    print("对不起，" + self.name + "没有收藏《" + keyword + "》！请尝试模糊查询！(我还没实装，哈哈)")
                print('***********************************************************************************************')
        if "ISBN" == way:
            for keyword in keywords:
                try:
                    index = self.collection['isbn'].index(keyword)
                except ValueError:
                    print("对不起，"+self.name+"没有收藏ISBN号为\""+keyword+"\"的书籍！请尝试模糊查询！")
                else:
                    self.collection['book'][index].print_book_info()
                print('***********************************************************************************************')

    # 模糊查询
    def fuzzy_query_book(self, way="title", keywords=['射雕','龙枪']):
        flag_set = set()
        print('正在查询......')
        print('查询结果：')
        print('***********************************************************************************************')
        if "title" == way:
            for keyword in keywords:
                for i, x in enumerate(self.collection['title']):
                    if re.search(keyword,x,re.I) is not None:
                        flag_set.add(i)
            if flag_set:
                for index in flag_set:
                    self.collection['book'][index].print_book_info()
            else:
                print("对不起，没有任何匹配书籍！")
            print('***********************************************************************************************')
        if "ISBN" == way:
            for keyword in keywords:
                for i, x in enumerate(self.collection['isbn']):
                    if re.search(keyword,x,re.I) is not None:
                        flag_set.add(i)
            if flag_set:
                for index in flag_set:
                    self.collection['book'][index].print_book_info()
            else:
                print("对不起，没有任何匹配书籍！")
            print('***********************************************************************************************')

    # 删除书籍
    def exact_match_remove_book(self, way="title", keywords=['射雕英雄传.叁']):
        print('开始删除......')
        print('---------------------------------------------------------------------------------------')
        if "title" == way:
            for keyword in keywords:
                indexs = [i for i, x in enumerate(self.collection['title']) if x == keyword]
                if indexs:
                    for index in indexs:
                        try:
                            self.borrow_system['isbn'].index(self.collection['book'][index].isbn)
                        except ValueError:
                            self.number_of_collection = \
                                self.number_of_collection - self.collection['book'][index].number
                            self.number_of_type = self.number_of_type - 1
                            print("准备删除的书籍信息：")
                            self.collection['book'][index].print_book_info()
                            del self.collection['title'][index]
                            del self.collection['author'][index]
                            del self.collection['isbn'][index]
                            del self.collection['book'][index]
                            print("成功删除《" + keyword + "》!")
                        else:
                            print("《" + keyword + "》有部分书籍处于借出状态，目前不可删除!")
                else:
                    print(self.name + "没有收藏《" + keyword + "》!")

                # try:
                #     index = self.collection['title'].index(keyword)
                # except ValueError:
                #     print(self.name + "没有收藏《" + keyword + "》!")
                # else:
                #     # 查一下要删除的书籍是否借出
                #     try:
                #         self.borrow_system['title'].index(keyword)
                #     except ValueError:
                #         print("准备删除的书籍信息：")
                #         self.collection['book'][index].print_book_info()
                #         del self.collection['title'][index]
                #         del self.collection['author'][index]
                #         del self.collection['isbn'][index]
                #         del self.collection['book'][index]
                #         print("成功删除《" + keyword + "》!")
                #     else:
                #         print("《" + keyword + "》有部分书籍处于借出状态，目前不可删除!")
                print('---------------------------------------------------------------------------------------')
        if "ISBN" == way:
            for keyword in keywords:
                try:
                    index = self.collection['isbn'].index(keyword)
                except ValueError:
                    print(self.name + "没有收藏ISBN号为\"" + keyword + "\"的书籍！")
                else:
                    try:
                        self.borrow_system['isbn'].index(keyword)
                    except ValueError:
                        self.number_of_collection = \
                            self.number_of_collection - self.collection['book'][index].number
                        self.number_of_type = self.number_of_type - 1
                        print("准备删除的书籍信息：")
                        self.collection['book'][index].print_book_info()
                        del self.collection['title'][index]
                        del self.collection['author'][index]
                        del self.collection['isbn'][index]
                        del self.collection['book'][index]
                        print("成功删除《" + keyword + "》!")
                    else:
                        print("ISBN号为\"" + keyword + "\"的书籍有部分处于借出状态，目前不可删除!")
                print('---------------------------------------------------------------------------------------')
        print('删除完毕！')
        print('---------------------------------------------------------------------------------------')

    def get_time(self):
        now = datetime.now()
        days = timedelta(days=self.max_borrow_time_limit)
        return_time = now + days
        return now.strftime('%Y/%m/%d'), return_time.strftime('%Y/%m/%d')

    def borrow_manage(self, titles=['射雕英雄传.叁'], borrower='沈宝印'):
        # 先查询系统里是否存在书籍
        print('---------------------------------------------------------------------------------------')
        for keyword in titles:
            # 一个小彩蛋，操作有风险，可能会删除全部数据
            if keyword == "创世纪之书":
                if not(borrower == "天地有雪" or borrower == "罗森"):
                    print("\033[31mPermissionDenied:您正在访问禁止阅读书籍，但您没有创世神权限!\033[0m")
                    print("\033[31m系统将于3秒后开始无差别攻击......\033[0m")
                    print("\033[31m倒计时开始:\033[0m")
                    print("\033[31m3\033[0m")
                    time.sleep(1)
                    print("\033[31m2\033[0m")
                    time.sleep(1)
                    print("\033[31m1\033[0m")
                    time.sleep(1)
                    print("\033[31m0\033[0m")
                    print("\033[31m开始无差别攻击\033[0m")
                    print("\033[31m启动三级自卫程序......\033[0m")
                    print("\033[31m大威天龙，大罗法咒，般若诸佛，遍照三千。\033[0m\n")
                    time.sleep(1)
                    # r = random.random()
                    r = 0.981
                    if r > 0.1:
                        print("\033[31m启动二级自卫程序......\033[0m")
                        print("\033[31m武中无相开始模拟\033[0m")
                        print("\033[31m系统机能50%增援\033[0m")
                        print("\033[31m核融拳3倍增压\033[0m")
                        print("\033[31m核融拳·飞翼零式\033[0m\n")
                    time.sleep(1)
                    if r > 0.4:
                        print("\033[31m启动一级自卫程序......\033[0m")
                        print("\033[31m武中无相全面开启\033[0m")
                        print("\033[31m系统机能100%增援\033[0m")
                        print("\033[31m核融拳5倍增压\033[0m")
                        print("\033[31m核融拳·导弹式\033[0m\n")
                    time.sleep(1)
                    if r > 0.7:
                        print("\033[31m启动终极级自卫程序......\033[0m")
                        print("\033[31m武中无相极限模拟\033[0m")
                        print("\033[31m系统机能全面解封\033[0m")
                        print("\033[31m启动末日系统:天崩\033[0m\n")
                    time.sleep(1)
                    if r > 0.98:
                        print("\033[31m未能成功清理入侵者，系统将于3秒后开始自毁......\033[0m\n")
                        print("\033[31m倒计时开始:")
                        print("\033[31m3\033[0m")
                        time.sleep(1)
                        print("\033[31m2\033[0m")
                        time.sleep(1)
                        print("\033[31m1\033[0m")
                        time.sleep(1)
                        print("\033[31m0\033[0m")
                        print("\033[31m开始自毁\033[0m")
                        f_path = "lib/lib_set_cache.pkl"
                        if os.path.exists(f_path):
                            self.doc_burner("lib_set_cache.pkl")
                            f = open(f_path, 'rb')
                            lib_set = pickle.load(f)
                            f.close()
                            f = open(f_path, 'wb')
                            lib_set.discard(self.name)
                            pickle.dump(lib_set, f)
                            f.close()
                        f = "lib/"+self.name+"_cache.pkl"
                        if os.path.exists(f):
                            self.doc_burner(self.name+"_cache.pkl")
                            os.remove(f)
                        f = "lib/"+self.name+"_barcode_no.pkl"
                        if os.path.exists(f):
                            self.doc_burner(self.name+"_barcode_no.pkl")
                            os.remove(f)
                        print("\033[31m成功自毁！\033[0m")
                        exit(0)
                    else:
                        print("\033[31m成功清理不明入侵者，退出系统，本次操作不会被保存!\033[0m")
                    exit(0)
            try:
                index = self.collection['title'].index(keyword)
            except ValueError:
                print("对不起，" + self.name + "没有收藏《" + keyword + "》！请尝试荐购！")
            else:
                # 查询是否存在可借书籍
                print(borrower+"准备借阅的书籍信息：")
                self.collection['book'][index].print_book_info()
                flag = False
                for i,dic in enumerate(self.collection['book'][index].barcode_and_state_list):
                    if dic['state'] == "可借":
                        flag = True
                        self.borrower_set.add(borrower)
                        self.borrow_system['title'].append(keyword)
                        self.borrow_system['isbn'].append(self.collection['book'][index].isbn)
                        self.borrow_system['barcode'].append(self.collection['book'][index].
                                                             barcode_and_state_list[i]['barcode'])
                        self.borrow_system['borrower'].append(borrower)
                        self.borrow_system['out_time'].append(self.get_time()[0])
                        self.borrow_system['date_to_return'].append(self.get_time()[1])
                        self.collection['book'][index].barcode_and_state_list[i]['state'] = \
                            "借出,应还时间:"+self.get_time()[1]
                        break
                if flag:
                    print("借书成功！")
                else:
                    print("抱歉，所有《"+keyword+"》均已外借！")
            print('---------------------------------------------------------------------------------------')

    def doc_burner(self,doc_name="text.txt"):
        print("\033[31m正在销毁"+doc_name+"......\033[0m")
        for i in range(101):
            time.sleep(0.1)
            print('\033[31m\r|' + '▇' * (i // 2) + '|' + str(i) + '%\033[0m', end='')
        print("")

    def print_borrow_system(self):
        print("****************************************************************************************************")
        print(self.name+"当前借阅信息：")
        print("----------------------------------------------------------------------------------------------------")
        for title,isbn,barcode,borrower,out_time,date_to_return in \
                zip(self.borrow_system['title'],self.borrow_system['isbn'], self.borrow_system['barcode'],
                    self.borrow_system['borrower'], self.borrow_system['out_time'],
                    self.borrow_system['date_to_return']):
            print("书名："+title, end='|')
            print("ISBN："+isbn, end='|')
            print("条码号："+barcode, end='|')
            print("借阅人："+borrower, end='|')
            print("借出时间："+out_time, end='|')
            print("借阅期限："+str(self.max_borrow_time_limit)+"天", end='|')
            print("应还时间："+date_to_return)
        print("****************************************************************************************************")

    def return_manage(self, barcodes=["0000292"]):
        print("**********************************************************************************************")
        print("正在还书......")
        print("----------------------------------------------------------------------------------------------")
        for barcode in barcodes:
            try:
                # 寻找位于借阅系统中的位置
                index = self.borrow_system['barcode'].index(barcode)
            except ValueError:
                print("书籍已归还！")
            else:
                # 寻找位于图书馆的位置
                index_lib = self.collection['isbn'].index(self.borrow_system['isbn'][index])
                print("准备归还书籍的信息：")
                print("借阅人：" + self.borrow_system['borrower'][index], end='|')
                print("条码号：" + self.borrow_system['barcode'][index], end='|')
                print("借出时间：" + self.borrow_system['out_time'][index], end='|')
                print("还书时间：" + self.get_time()[0])
                self.collection['book'][index_lib].print_book_info()
                for dic in self.collection['book'][index_lib].barcode_and_state_list:
                    if dic['barcode'] == barcode:
                        dic['state'] = "可借"
                        break
                # 添加还书日志信息
                self.borrow_return_log['title'].append(self.borrow_system['title'][index])
                self.borrow_return_log['isbn'].append(self.borrow_system['isbn'][index])
                self.borrow_return_log['barcode'].append(self.borrow_system['barcode'][index])
                self.borrow_return_log['borrower'].append(self.borrow_system['borrower'][index])
                self.borrow_return_log['out_time'].append(self.borrow_system['out_time'][index])
                self.borrow_return_log['return_time'].append(self.get_time()[0])
                del self.borrow_system['title'][index],self.borrow_system['isbn'][index],\
                    self.borrow_system['barcode'][index],self.borrow_system['borrower'][index],\
                    self.borrow_system['out_time'][index],self.borrow_system['date_to_return'][index]
                print("还书成功!")
                print("----------------------------------------------------------------------------------------------")
        print("**********************************************************************************************")

    def print_borrow_return_log(self):
        print("****************************************************************************************************")
        print(self.name+"借还日志：")
        print("----------------------------------------------------------------------------------------------------")
        for title, isbn, barcode, borrower, out_time, return_time in \
                zip(self.borrow_return_log['title'], self.borrow_return_log['isbn'], self.borrow_return_log['barcode'],
                    self.borrow_return_log['borrower'], self.borrow_return_log['out_time'],
                    self.borrow_return_log['return_time']):
            print("书名：" + title, end='|')
            print("ISBN：" + isbn, end='|')
            print("条码号：" + barcode, end='|')
            print("借阅人：" + borrower, end='|')
            print("借出时间：" + out_time, end='|')
            print("还书时间：" + return_time)
        print("****************************************************************************************************")

    def borrow_query(self,way="borrower", keyword="沈宝印"):
        print("*****************************************************************************************************")
        if "borrower" == way:
            print(keyword + "借阅的书籍：")
            print(
                "-----------------------------------------------------------------------------------------------------")
            for title, isbn, barcode, borrower, out_time, date_to_return in \
                    zip(self.borrow_system['title'], self.borrow_system['isbn'], self.borrow_system['barcode'],
                        self.borrow_system['borrower'], self.borrow_system['out_time'],
                        self.borrow_system['date_to_return']):
                if borrower == keyword:
                    print("借阅人：" + borrower, end='|')
                    print("借阅书籍：" + title, end='|')
                    print("ISBN：" + isbn, end='|')
                    print("条码号：" + barcode, end='|')
                    print("借出时间：" + out_time, end='|')
                    print("借阅期限：" + str(self.max_borrow_time_limit) + "天", end='|')
                    print("应还时间：" + date_to_return)
            for title, isbn, barcode, borrower, out_time, return_time in \
                    zip(self.borrow_return_log['title'], self.borrow_return_log['isbn'],
                        self.borrow_return_log['barcode'],
                        self.borrow_return_log['borrower'], self.borrow_return_log['out_time'],
                        self.borrow_return_log['return_time']):
                if borrower == keyword:
                    print("借阅人：" + borrower, end='|')
                    print("借阅书籍：" + title, end='|')
                    print("ISBN：" + isbn, end='|')
                    print("条码号：" + barcode, end='|')
                    print("借出时间：" + out_time, end='|')
                    print("还书时间：" + return_time)
        if "title" == way:
            print("《"+keyword+"》被借阅情况：")
            print(
                "-----------------------------------------------------------------------------------------------------")
            for title, isbn, barcode, borrower, out_time, date_to_return in \
                    zip(self.borrow_system['title'], self.borrow_system['isbn'], self.borrow_system['barcode'],
                        self.borrow_system['borrower'], self.borrow_system['out_time'],
                        self.borrow_system['date_to_return']):
                if title == keyword:
                    print("借阅书籍：" + title, end='|')
                    print("借阅人：" + borrower, end='|')
                    print("ISBN：" + isbn, end='|')
                    print("条码号：" + barcode, end='|')
                    print("借出时间：" + out_time, end='|')
                    print("借阅期限：" + str(self.max_borrow_time_limit) + "天", end='|')
                    print("应还时间：" + date_to_return)
            for title, isbn, barcode, borrower, out_time, return_time in \
                    zip(self.borrow_return_log['title'], self.borrow_return_log['isbn'],
                        self.borrow_return_log['barcode'],
                        self.borrow_return_log['borrower'], self.borrow_return_log['out_time'],
                        self.borrow_return_log['return_time']):
                if title == keyword:
                    print("借阅书籍：" + title, end='|')
                    print("借阅人：" + borrower, end='|')
                    print("ISBN：" + isbn, end='|')
                    print("条码号：" + barcode, end='|')
                    print("借出时间：" + out_time, end='|')
                    print("还书时间：" + return_time)
        if "date" == way:
            print(keyword+"的借阅情况：")
            print(
                "-----------------------------------------------------------------------------------------------------")
            for title, isbn, barcode, borrower, out_time, date_to_return in \
                    zip(self.borrow_system['title'], self.borrow_system['isbn'], self.borrow_system['barcode'],
                        self.borrow_system['borrower'], self.borrow_system['out_time'],
                        self.borrow_system['date_to_return']):
                if out_time == keyword:
                    print("借出时间：" + out_time, end='|')
                    print("借阅书籍：" + title, end='|')
                    print("借阅人：" + borrower, end='|')
                    print("ISBN：" + isbn, end='|')
                    print("条码号：" + barcode, end='|')
                    print("借阅期限：" + str(self.max_borrow_time_limit) + "天", end='|')
                    print("应还时间：" + date_to_return)
            for title, isbn, barcode, borrower, out_time, return_time in \
                    zip(self.borrow_return_log['title'], self.borrow_return_log['isbn'],
                        self.borrow_return_log['barcode'],
                        self.borrow_return_log['borrower'], self.borrow_return_log['out_time'],
                        self.borrow_return_log['return_time']):
                if out_time == keyword:
                    print("借出时间：" + out_time, end='|')
                    print("借阅书籍：" + title, end='|')
                    print("借阅人：" + borrower, end='|')
                    print("ISBN：" + isbn, end='|')
                    print("条码号：" + barcode, end='|')
                    print("还书时间：" + return_time)
        print("*****************************************************************************************************")

    def sort_desc_index(self, titles=['多源信息融合理论及应用',"射雕英雄传.叁"], arr=[1,2]):
        num = []
        tit = []
        arr = np.array(arr)
        st = list(np.argsort(-arr))
        st = st[0:10]
        arr = list(arr)
        for i in st:
            num.append(arr[i])
            tit.append(titles[i])
        return tit, num

    def borrow_statistics(self):
        # 绘图设置
        plt.close('all')  # 关闭所有绘图
        matplotlib.rcParams['axes.unicode_minus'] = False  # 绘图可以出现负号
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 后面中括号中为指定字体名称。
        # 先统计每一本书被借了多少次
        titles = self.collection['title']
        borrow_num = []
        for isbn in self.collection['isbn']:
            count = 0
            for value in self.borrow_system['isbn']:
                if isbn == value:
                    count = count + 1
            for value in self.borrow_return_log['isbn']:
                if isbn == value:
                    count = count + 1
            borrow_num.append(count)
        titles, borrow_num = self.sort_desc_index(titles, borrow_num)
        titles = titles[::-1]
        titles_temp = copy.deepcopy(titles)
        # 修改title，防止书名过长
        for i,title in enumerate(titles_temp):
            if len(title) > 9:
                titles[i] = title[0:int(len(title)/2)] + "\n" + title[int(len(title)/2):]
        borrow_num = borrow_num[::-1]
        # 绘图
        plt.figure(1)
        color = ['#00ace6', '#00bfff', '#1ac6ff', '#33ccff', '#4dd2ff',
                 '#66d9ff', '#80dfff', '#99e6ff', '#b3ecff', '#ccf2ff']
        color = color[::-1]
        plt.barh(range(len(borrow_num)), borrow_num, height=0.35, color=color, tick_label=titles)
        plt.tick_params(labelsize=12)
        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        plt.title('书籍借阅次数榜单榜单前10', fontsize=24)
        plt.ylabel('书籍', fontsize=14)
        plt.xlabel('借阅次数', fontsize=14)
        for a, b in zip(range(len(borrow_num)), borrow_num):
            plt.text(b + 0.05, a-0.1, '%d' % b, ha='center', va='bottom', fontsize=12)
        plt.get_current_fig_manager().window.showMaximized() # 最大化窗口
        # plt.tight_layout()
        plt.savefig(IMAGE_SAVE_PATH+self.name+'top_10_by_title.png',bbox_inches='tight')
        # 再统计每个人被借了多少本书
        borrowers = list(self.borrower_set)
        borrow_num = []
        for borrower in borrowers:
            count = 0
            for value in self.borrow_system['borrower']:
                if borrower == value:
                    count = count + 1
            for value in self.borrow_return_log['borrower']:
                if borrower == value:
                    count = count + 1
            borrow_num.append(count)
        borrowers, borrow_num = self.sort_desc_index(borrowers, borrow_num)
        plt.figure(2)
        color = ['#ffe6b3', '#ffdd99', '#ffd480', '#ffcc66', '#ffc34d',
                 '#ffbb33', '#ffb31a', '#ffaa00', '#e69900', '#cc8800']
        color = color[::-1]
        plt.bar(range(len(borrow_num)), borrow_num, width=0.2, color=color, tick_label=borrowers)
        plt.tick_params(labelsize=12)
        ax = plt.gca()
        ax.yaxis.set_major_locator(MultipleLocator(1))
        plt.title('书籍借阅次数榜单榜单前10', fontsize=24)
        plt.xlabel('姓名', fontsize=14)
        plt.ylabel('借阅次数', fontsize=14)
        for a, b in zip(range(len(borrow_num)), borrow_num):
            plt.text(a, b + 0.05,  '%d' % b, ha='center', va='bottom', fontsize=12)
        plt.savefig(IMAGE_SAVE_PATH+self.name+'top_10_by_borrower.png',bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    guada = Library()
    guada.reset_cache()
    book1 = Book(translator="朱学恒")
    book2 = Book('射雕英雄传.叁','金庸','978-7-5462-1334-7',27.00)
    book3 = Book('笑傲江湖.壹','金庸','978-7-5462-1340-8',27.00)
    book4 = Book('多源信息融合理论及应用','潘泉 ... [等]','978-7-302-30127-1',69.00)
    book5 = Book('博弈论入门','葛泽慧 ... [等]','978-7-302-50490-0',55.00)
    book6 = Book('小李飞刀:外一篇.4.天涯·明月·刀','古龙','978-7-80765-762-0',29.50)
    book7 = Book('龙族.II.悼亡者之瞳','江南','978-7-5492-0430-4',29.80)
    book8 = Book('目标跟踪基本原理','(澳) Subhash Challa ... [等]','978-7-118-10092-1',86.00,translator='周共健')
    book9 = Book('菊与刀','(美) 鲁思·本尼迪克特','978-7-214-23419-3',36.80,translator='叶宁')
    book10 = Book('线性代数·第四版','西北工业大学应用数学系线性代数教学组','978-7-5612-4070-0',20.00)
    book11 = Book('1984','(英) 乔治·奥威尔','978-7-5680-1418-2',55.00,translator='韩阳, 王喆')


    guada.add_book(book1)
    guada.add_book(book2, '东馆南四层 社科图书阅览室','I247/J691-51/(3)', 5)
    guada.add_book(book3,'东馆南四层 社科图书阅览室','I247/J691-53/(1)',2)
    guada.add_book(book4,'东馆南四层 社科图书阅览室','G202/1302',2)
    guada.add_book(book5,'东馆南三层 科技图书阅览室','O225/1808',4)
    guada.add_book(book6,'东馆南四层 社科图书阅览室','I247/G611-38/(4:1)',3)
    guada.add_book(book7,'东馆南四层 社科图书阅览室','I247/J365-4/(2)',2)
    guada.add_book(book7, '东馆南四层 社科图书阅览室', 'I247/J365-4/(2)', 2)
    guada.add_book(book8, '东馆北三层 科技典藏图书阅览室 ', 'TN953/1509',3)
    guada.add_book(book9, '东馆南四层 社科图书阅览室', 'G131.3/1907', 4)
    guada.add_book(book10, '东馆南三层 科技图书阅览室', 'O151.2/1408-6=4', 1)
    guada.add_book(book11, '东馆南四层 社科图书阅览室', 'I561.4/A009-18', 2)

    book1.print_book_info()
    book2.print_book_info()
    book3.print_book_info()
    book4.print_book_info()

    guada.print_collection_index()

    way = "title"
    keywords = ["射雕英雄传.叁","笑傲江湖.壹"]
    guada.exact_match_query_book(way,keywords)

    # # 删除书籍
    # guada.exact_match_remove_book(way,keywords)

    # guada.print_collection_index()

    # 借书
    guada.borrow_manage(['多源信息融合理论及应用',"射雕英雄传.叁",'龙族.II.悼亡者之瞳','博弈论入门','小李飞刀:外一篇.4.天涯·明月·刀', '线性代数·第四版'])
    guada.borrow_manage(['笑傲江湖.壹','1984','射雕英雄传.叁','目标跟踪基本原理','龙枪编年史.第一部.秋暮之巨龙'],"天地有雪")
    guada.borrow_manage(['博弈论入门','射雕英雄传.叁','小李飞刀:外一篇.4.天涯·明月·刀','1984','菊与刀','龙族.II.悼亡者之瞳'],"西门朱玉")
    guada.borrow_manage(['博弈论入门', '射雕英雄传.叁', '小李飞刀:外一篇.4.天涯·明月·刀', '1984', '菊与刀', '龙族.II.悼亡者之瞳'], "冰尘")

    guada.print_borrow_system()

    # 还书
    if len(guada.borrow_system['barcode']) > 5:
        guada.return_manage(random.sample(guada.borrow_system['barcode'],4))

    # guada.return_manage(['0002373'])

    guada.print_borrow_system()

    guada.print_borrow_return_log()

    # 借阅查询
    way = "borrower"
    keyword = "西门朱玉"
    guada.borrow_query(way, keyword)
    way = "title"
    keyword = "射雕英雄传.叁"
    guada.borrow_query(way, keyword)
    way = "date"
    keyword = "2020/06/08"
    guada.borrow_query(way, keyword)

    # 输出统计图
    guada.borrow_statistics()

    # 每次操作到最后，一定要保存信息，否则就白操作了
    guada.save_cache()

    # import webbrowser
    #
    # url = 'D:\phpStudy\phpstudy_pro\WWW\Web开发\study002\风姿物语百度百科.html'
    # webbrowser.open(url)
