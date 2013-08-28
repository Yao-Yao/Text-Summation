# -*- coding: utf-8 -*-
##import codecs
from basicmethods import *

##import sys
##reload(sys) 
##sys.setdefaultencoding('utf8')

##def convert_cn(s):
##    return s.encode('gb18030')  # gb2312 cannot work

def unigram_en(sc):
    words = []
    for w in sc.split():
        words.append(w)
    return words

def unigram_cn(sc):
    words = []
    for w in sc:
        words.append(w)
    return words

def bigram_en(sc):
    begin = '<B>'
    end = '<E>'
    words = []
    word = [begin, begin]

    for w in sc.split():
        word[0] = word[1]
        word[1] = w
        words.append(tuple(word))

    word[0] = word[1]
    word[1] = end
    words.append(tuple(word))

    return words

def bigram_cn(sc):
    begin = '<B>'
    end = '<E>'
    words = []
    word = [begin, begin]

    for w in sc:
        word[0] = word[1]
        word[1] = w
        words.append(tuple(word))

    word[0] = word[1]
    word[1] = end
    words.append(tuple(word))

    return words

if __name__ == "__main__": 
    sc = 'i love you'
    print sc
    words = unigram_en(sc)
    print words
    for w in words:
        print w

    words = bigram_en(sc)
    print words
    for w in words:
        print w
        
    sc = to_unicode('我爱你')
    print sc
    words = unigram_cn(sc)
    print words
    for w in words:
        print w
        
    print sc
    words = bigram_cn(sc)
    print words
    for w in words:
        print w
        
    print "\n****** press any key to exit ******"
    sys.stdin.readline()
