# -*- coding:utf-8 -*-
import random


class Accounts(object):

    def __init__(self, filename):
        self.filename = filename
        self.f_level = {}
        self.s_level = {}
        self.__load_from_file()

    def __load_from_file(self):
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                data = line.strip('\n').split('\t')
                if len(data) != 4:
                    print line
                    continue
                self.f_level.setdefault(data[0], []).append((data[2], data[3]))
                self.f_level.setdefault(data[1], []).append((data[2], data[3]))

    def get_random_account_by_f_class(self, f_class):
        data = self.f_level.get(f_class, [])
        if not data:
            return None
        return random.choice(data)

    def get_random_account_by_s_class(self, s_class):
        data = self.s_level.get(s_class, [])
        if not data:
            return None
        return random.choice(data)

    def get_random_account(self, f_class, s_class):
        data = self.get_random_account_by_s_class(s_class.encode('utf-8'))
        if data:
            return data
        return self.get_random_account_by_f_class(f_class.encode('utf-8'))

def main():
    account_mgr = Accounts('accounts.txt')
    #print account_mgr.get_random_account_by_f_class('vct//电影')
    #print account_mgr.get_random_account_by_f_class('vsct//体育/篮球')
    print account_mgr.get_random_account_by_f_class('vct//娱乐')

if __name__ == '__main__':
    main()
