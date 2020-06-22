#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gingkg
@contact: sby2015666@163.com
@software: PyCharm
@file: humancomputer_interact.py
@time: 2020/6/9
@last updated date: 2020/6/14
@desc: human computer interact
"""

from library import Library
from book import Book
import pickle
import sys
import os
import argparse

LIB_SET_CACHE_PATH = "lib/" + "lib_set_cache.pkl"


class HumanComputerInteract:
    def __init__(self):
        self.lib_set = set()
        self.lib = None
        self.load_cache()
        print("*******************************************************")
        print("* 欢迎使用仙得法歌图书管理系统！")
        print("* 开始创建和管理自己的图书馆吧！(*^_^*) ！")
        print("* ps:系统有待完善，添加书籍时，请一定保证书名和ISBN的唯一性")
        print("*******************************************************\n")
        self.print_lib_set()

    def run(self):
        print("你可以选择新建一个图书馆或者打开\\移除一个已存在的图书馆："
              "\n# 输入1:新建\n# 输入2:打开\n# 输入3:重开\n# 输入4:移除\n# 其它:退出系统")
        a = input(">>>").strip()
        if a == "1":
            # 创建图书馆
            self.creat_lib()
            while True:
                self.print_options()
                self.lib_operation()
        elif a == "2":
            # 打开图书馆
            self.open_lib()
            while True:
                self.print_options()
                self.lib_operation()
        elif a == "3":
            self.save_lib()
            self.__init__()
            self.run()
        elif a == "4":
            self.remove_lib()
            self.run()
        else:
            # self.save_lib()
            self.exit()

    def creat_lib(self):
        lib_name = input("请输入新建的图书馆的名字：").strip()
        flag = None
        while True:
            if lib_name in self.lib_set:
                print(lib_name + "已存在!")
                print("是否打开"+lib_name+":\n# yes:打开\n# no:返回\n# 其他:退出系统")
                flag = input(">>>").strip()
                if flag == "yes":
                    break
                elif flag == "no":
                    break
                else:
                    self.exit()
            else:
                break
        if flag == "yes":
            self.lib = Library(lib_name)
            print("成功打开" + lib_name + "!")
            while True:
                self.print_options()
                self.lib_operation()
        elif flag == "no":
            self.run()
        else:
            lib_location = input("请输入"+lib_name+"的地址：").strip()
            default_return_book_position = input("请输入"+lib_name+"的默认还书地点：").strip()
            max_borrow_time_limit = int(input("请输入"+lib_name+"的书籍最大借阅期限(天)：").strip())
            self.lib = Library(lib_name, lib_location, default_return_book_position, max_borrow_time_limit)
            self.lib_set.add(lib_name)
            print("成功创建"+lib_name+"!")

    def open_lib(self):
        lib_name = input("请输入你想打开的图书馆的名字：").strip()
        flag = None
        while True:
            if lib_name not in self.lib_set:
                print(lib_name + "不存在!")
                print("是否继续打开图书馆:\n# yes:继续\n# no:返回\n# 其他:退出系统")
                flag = input(">>>").strip()
                if flag == "yes":
                    lib_name = input("请输入你想打开的图书馆的名字：").strip()
                elif flag == "no":
                    break
                else:
                    self.exit()
            else:
                break
        if flag == "no":
            self.run()
        else:
            self.lib = Library(lib_name)
            print("成功打开" + lib_name + "!")

    def save_lib(self):
        print("是否保存本次操作:\n# yes:保存\n# no:不保存\n# 其他:退出系统")
        flag = input(">>>").strip()
        if flag == "yes":
            self.lib.save_cache()
            print("成功保存本次操作!")
        elif flag == "no":
            pass
        else:
            self.exit()

    def exit(self):
        try:
            self.save_cache()
            sys.exit(0)
        finally:
            print("已保存记录!")
            print("已成功退出系统！")
            print("欢迎下次使用仙得法歌图书管理系统！")

    def load_cache(self):
        if not os.path.exists(LIB_SET_CACHE_PATH):
            f = open(LIB_SET_CACHE_PATH, 'wb')
            lib_set = set()
            pickle.dump(lib_set, f)
            f.close()
        f = open(LIB_SET_CACHE_PATH, 'rb')
        try:
            self.lib_set = pickle.load(f)
        except ValueError:
            self.reset_cache()
        f.close()

    def save_cache(self):
        f = open(LIB_SET_CACHE_PATH, 'wb')
        pickle.dump(self.lib_set, f)
        f.close()

    def reset_cache(self):
        f = open(LIB_SET_CACHE_PATH, 'wb')
        lib_set = set()
        pickle.dump(lib_set, f)
        f.close()
        self.load_cache()

    def remove_lib(self):
        lib_name = input("请输入你想要移除的图书馆：").strip()

        if lib_name in self.lib_set:
            file = "lib/" + lib_name + "_cache.pkl"
            if os.path.exists(file):
                os.remove(file)
            file = "lib/" + lib_name + "_barcode_no.pkl"
            if os.path.exists(file):
                os.remove(file)
            self.lib_set.discard(lib_name)
            print("成功移除"+lib_name+"!")
        else:
            print(lib_name + "不存在!")

    def print_lib_set(self):
        print("***********************************************")
        print("已存在的图书馆：")
        print("-----------------------------------------------")
        for lib_name in self.lib_set:
            lib = Library(lib_name)
            lib.print_library_info()
        print("***********************************************")

    def print_options(self):
        print("选项：\n"
              "# 1:添加书籍\n"
              "# 2:精确匹配查询书籍\n"
              "# 3:模糊匹配查询书籍\n"
              "# 4:删除书籍\n"
              "# 5:借阅书籍\n"
              "# 6:归还书籍\n"
              "# 7:查询借阅记录\n"
              "# 8:借阅分布\n"
              "# 9:馆藏目录\n"
              "# 10:当前借阅\n"
              "# 11:借还日志\n"
              "# 12:重开\n"
              "# ?:关于"+self.lib.name+"\n"
              "# 其它:退出系统")

    def lib_operation(self):
        b = input(">>>").strip()
        if b == "1":
            self.add_book()
            while True:
                flag = input("是否继续添加书籍：\n# yes:继续\n# no:返回\n# 其他:退出系统\n>>>").strip()
                if flag == "yes":
                    self.add_book()
                elif flag == "no":
                    break
                else:
                    self.save_lib()
                    self.exit()
        elif b == "2":
            self.exact_query_system()
            while True:
                flag = input("是否继续查询书籍：\n# yes:继续\n# no:返回\n# 其他:退出系统\n>>>").strip()
                if flag == "yes":
                    self.exact_query_system()
                elif flag == "no":
                    break
                else:
                    self.save_lib()
                    self.exit()
        elif b == "3":
            self.fuzzy_query_system()
            while True:
                flag = input("是否继续查询书籍：\n# yes:继续\n# no:返回\n# 其他:退出系统\n>>>").strip()
                if flag == "yes":
                    self.fuzzy_query_system()
                elif flag == "no":
                    break
                else:
                    self.save_lib()
                    self.exit()
        elif b == "4":
            self.exact_remove_system()
            while True:
                flag = input("是否继续删除书籍：\n# yes:继续\n# no:返回\n# 其他:退出系统\n>>>").strip()
                if flag == "yes":
                    self.exact_remove_system()
                elif flag == "no":
                    break
                else:
                    self.save_lib()
                    self.exit()
        elif b == "5":
            self.loan_system()
            while True:
                flag = input("是否继续借阅书籍：\n# yes:继续\n# no:返回\n# 其他:退出系统\n>>>").strip()
                if flag == "yes":
                    self.loan_system()
                elif flag == "no":
                    break
                else:
                    self.save_lib()
                    self.exit()
        elif b == "6":
            self.return_system()
            while True:
                flag = input("是否继续归还书籍：\n# yes:继续\n# no:返回\n# 其他:退出系统\n>>>").strip()
                if flag == "yes":
                    self.loan_system()
                elif flag == "no":
                    break
                else:
                    self.save_lib()
                    self.exit()
        elif b == "7":
            self.query_loan_record()
            while True:
                flag = input("是否继续查询借阅记录：\n# yes:继续\n# no:返回\n# 其他:退出系统\n>>>").strip()
                if flag == "yes":
                    self.query_loan_record()
                elif flag == "no":
                    break
                else:
                    self.save_lib()
                    self.exit()
        elif b == "8":
            self.lib.borrow_statistics()
        elif b == "9":
            self.lib.print_collection_index()
        elif b == "10":
            self.lib.print_borrow_system()
        elif b == "11":
            self.lib.print_borrow_return_log()
        elif b == "12":
            self.save_lib()
            self.__init__()
            self.run()
        elif b == "?" or b == "？":
            self.lib.print_library_info()
        else:
            self.save_lib()
            self.exit()

    def add_book(self):
        book_title = input("书籍名称：").strip()
        book_author = input("作者：").strip()
        book_isbn = input("ISBN：").strip()
        book_price = float(input("定价：").strip())
        book_translator = input("译者【没有使用enter跳过】：").strip()
        book_campus_location = input("馆藏地点：").strip()
        book_call_no = input("索书号：").strip()
        book_number = int(input("册数：").strip())
        book = Book(book_title, book_author, book_isbn, book_price,
                    translator=book_translator if book_translator else None)
        self.lib.add_book(book, book_campus_location, book_call_no, book_number)

    def exact_query_system(self):
        way = input("请输入精确匹配查询方式【可选:title/ISBN】：").strip()
        while True:
            if way not in {"title", "ISBN"}:
                print("error:输入不符合要求，请重新输入！")
                way = input("请输入精确匹配查询方式【可选:title/ISBN】：").strip()
            else:
                break
        if way == "title":
            keywords = [x for x in (input("请输入需要查询的书籍名【可输入多个，以空格分隔】\n>>>").strip()).split()]
        if way == "ISBN":
            keywords = [x for x in (input("请输入需要查询的书籍的ISBN【可输入多个，以空格分隔】\n>>>").strip()).split()]
        self.lib.exact_match_query_book(way, keywords)

    def fuzzy_query_system(self):
        way = input("请输入模糊匹配查询方式【可选:title/ISBN】：").strip()
        while True:
            if way not in {"title", "ISBN"}:
                print("error:输入不符合要求，请重新输入！")
                way = input("请输入精确匹配查询方式【可选:title/ISBN】：").strip()
            else:
                break
        if way == "title":
            keywords = [x for x in (input("请输入需要查询的书籍名关键词【可输入多个，以空格分隔】\n>>>").strip()).split()]
        if way == "ISBN":
            keywords = [x for x in (input("请输入需要查询的书籍的ISBN关键数字【可输入多个，以空格分隔】\n>>>").strip()).split()]
        self.lib.fuzzy_query_book(way, keywords)

    def exact_remove_system(self):
        way = input("请输入删除方式【可选:title/ISBN】：").strip()
        while True:
            if way not in {"title", "ISBN"}:
                print("error:输入不符合要求，请重新输入！")
                way = input("请输入删除方式【可选:title/ISBN】：").strip()
            else:
                break
        if way == "title":
            keywords = [x for x in input("请输入需要删除的书籍名【可输入多个，以空格分隔】\n>>>").strip().split()]
        if way == "ISBN":
            keywords = [x for x in input("请输入需要删除的书籍的ISBN【可输入多个，以空格分隔】\n>>>").strip().split()]
        self.lib.exact_match_remove_book(way, keywords)

    def loan_system(self):
        person = input("请输入借阅人的姓名：").strip()
        keywords = [x for x in input("请输入需要借阅的书籍名【可输入多个，以空格分隔】\n>>>").strip().split()]
        self.lib.borrow_manage(keywords, person)

    def return_system(self):
        barcodes = [x for x in input("请输入需要归还的书籍条码号【可输入多个，以空格分隔】\n>>>").strip().split()]
        self.lib.return_manage(barcodes)

    def query_loan_record(self):
        way = input("请输入查询借阅记录的方式【可选:borrower/title/date】：").strip()
        while True:
            if way not in {"borrower","title","date"}:
                print("error:输入不符合要求，请重新输入！")
                way = input("请输入查询借阅记录的方式【可选:borrower/title/date】：").strip()
            else:
                break
        if way == "borrower":
            keyword = input("请输入需要查询借阅记录的借阅人：\n>>>").strip()
        if way == "title":
            keyword = input("请输入需要查询借阅记录的书籍名：\n>>>").strip()
        if way == "date":
            keyword = input("请输入需要查询借阅记录的日期：\n>>>").strip()
        self.lib.borrow_query(way, keyword)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin", type=str, default="gingkg", help='admin name, only name, not file path')
    parser.add_argument("--password", type=str, default="1896", help='admin password')
    args = parser.parse_args()

    admin_cache = []
    admin_cache.append({'admin': 'gingkg', 'password': '1896'})
    admin_cache.append({'admin': '沈宝印', 'password': '6666'})

    flag = False
    for x in admin_cache:
        if x['admin'] == args.admin and x['password'] == args.password:
            flag = True
            print("登陆成功！")
            break
        else:
            sys.exit("用户名或密码错误！")

    if flag:
        medusa = HumanComputerInteract()
        medusa.run()
