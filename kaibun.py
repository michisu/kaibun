# -*- coding: utf-8 -*-
import sys
import MeCab
import ipadic


class CircularLetter(object):

    def __init__(self, ipadic_dir='~/ipadic-2.7.0', mecab_option=''):
        self.tagger = MeCab.Tagger(mecab_option)
        self.trie = ipadic.IpadicTrie(ipadic_dir)

    def reading(self, line):
        tokens = []
        node = self.tagger.parseToNode(line)
        while node:
            if node.surface != '':
                ft = node.feature.decode('utf-8').split(',')
                if len(ft) < 8:
                    tokens.append(node.surface.decode('utf-8'))
                else:
                    tokens.append(ft[7])
            node = node.next
        return ''.join(tokens)

    def reversed_reading(self, line):
        return ''.join(reversed(self.reading(line)))

    def is_circular(self, line):
        reading = self.reading(line)
        reversed_reading = ''.join(reversed(reading))
        return reading == reversed_reading

    def reversed(self, line):
        tokens = []
        last_pos = 0
        line = self.reversed_reading(line)
        for i in xrange(len(line)):
            if i < last_pos: continue
            key, values = self.trie.longest_prefix_item(line[i:], (None, None))
            if key and values:
                tokens.append(values[0])
                last_pos += len(key)
            else:
                tokens.append(line[i])
                last_pos += 1
        return ''.join(tokens)


def main():
    circular = CircularLetter(sys.argv[1])
    try:
        line = raw_input('> ')
        while line:
            line = line.strip()
            print 'is_circular?:', circular.is_circular(line)
            print 'circular:', circular.reversed(line)
            line = raw_input('> ')
    except EOFError:
        pass

if __name__ == '__main__':
    main()
