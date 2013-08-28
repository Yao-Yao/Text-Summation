#!/usr/bin/env python
#coding=utf-8

import re
import codecs
import os
import pickle

from basicmethods import *
import langmodel

vocabulary = {} # term freq. in file group !!
vocab_df = {} # doc freq. in file group

##def convert_cn(s):
##    return s.encode('gb18030')  # gb2312 cannot work

def build_vocab_from_file(filepath):
    f = codecs.open(filepath, 'r', 'utf-8')
    # n = 1

    # skip first two lines, i.e. url
    line = f.readline()
    # print line
    line = f.readline()
    line = f.readline()
    # print to_unicode(line)

    # for line in f.readlines():
    while line:
        line = line.rstrip()
    	sentences = re.split(ur'。|？|！', line)
        # sentences = line.split('。')
    	for sc in sentences:
            # print n, '\t', to_unicode(sc) 
            # n += 1

            # get term freq.
            for word in langmodel.bigram_cn(sc):
                if word in vocabulary:
                    vocabulary[word] += 1
                else:
                    vocabulary[word] = 1
        line = f.readline()
    f.close()

def build_df_from_file(filepath):
    f = codecs.open(filepath, 'r', 'utf-8')
    # n = 1
    file_vocab = {} # term freq. in the file

    # skip first two lines, i.e. url
    line = f.readline()
    # print line
    line = f.readline()
    line = f.readline()
    # print to_unicode(line)

    # for line in f.readlines():
    while line:
        line = line.rstrip()
        sentences = re.split(ur'。|？|！', line)
        # sentences = line.split('。')
        for sc in sentences:
            # print n, '\t', to_unicode(sc) 
            # n += 1

            # get term freq.
            for word in langmodel.bigram_cn(sc):
                if word in file_vocab:
                    file_vocab[word] += 1
                else:
                    file_vocab[word] = 1
        line = f.readline()
    f.close()

    # get doc freq.
    for word in file_vocab:
        if word in vocab_df:
            vocab_df[word] += 1
        else:
            vocab_df[word] = 1

def print_dict(dictobj, outfilename):
    outfile = open(outfilename, 'w')
    for w in sorted(dictobj.items(), key=lambda x:x[1], reverse=True):
        # print w[0], w[1]
        outfile.write(to_unicode(w[0][0]))
        outfile.write(to_unicode(w[0][1]))
        outfile.write('\t')
        outfile.write(str(w[1]))
        outfile.write('\n')
    outfile.close()


if __name__ == "__main__": 
    # list all file paths in directory 'article'
    dataDir = 'article'
    pathlist = ls_dir(dataDir)

    # build vocab and vocab of df
    for path in pathlist:
        print path
        build_vocab_from_file(path)
        build_df_from_file(path)
    
    # serialization
    with open('vocabulary.pickle', 'wb') as f:
        pickle.dump(vocabulary, f) 

    with open('vocab_df.pickle', 'wb') as f:
        pickle.dump(vocab_df, f) 

    # sort the vocab and output
    print_dict(vocabulary, 'vocabulary.txt')

    # sort the vocab of df and output
    print_dict(vocab_df, 'vocab_df.txt')

    print to_unicode("\n****** 按任意键退出! ******")
    sys.stdin.readline()
