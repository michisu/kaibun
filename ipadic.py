# -*- coding: utf-8 -*-
import os
import re
from pytrie import StringTrie


pattern = re.compile((u'\(品詞 \((?P<pos>.*)\)\) '
    u'\(\(見出し語 \((?P<basic>.*) (\d+)\)\) '
    u'\(読み (?P<reading>.*)\) \(発音 (?P<pron>.*)\) \)'))


class IpadicTrie(StringTrie):

    def __init__(self, dirname=None):
        super(IpadicTrie, self).__init__(self)
        if dirname: self.initialize(dirname)

    def initialize(self, dirname):
        for filename in os.listdir(dirname):
            if filename.endswith('.dic'):
                filepath = os.path.join(dirname, filename)
                print 'reading', filepath
                self.add_dic(filepath)

    def add_dic(self, filepath, encoding='euc-jp'):
        for line in file(filepath):
            line = line.strip().decode(encoding)
            m = pattern.match(line)
            reading = m.group('reading')
            basic = m.group('basic')
            if reading not in self:
                self[reading] = []
            self[reading].append(basic)


def main():
    import sys
    trie = IpadicTrie(sys.argv[1])


if __name__ == '__main__':
    main()
