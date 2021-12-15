#!/usr/bin/env python
#coding=utf-8

import re
import codecs
import os

from basicmethods import *
import langmodel

USE_PICKLE = True
USE_DATABASE = False

#
# write to vocabulary/vocab_df
# (1) serialization to pickle file
# vocabulary = {} # term freq. in file group !!
# (2) update to database
# interface given by web app:
# - def insert(tablename, k, v)
# - def update(tablename, k, v)
# - def query(tablename, k) #fail: 0
#
vocabulary = {} # term freq. in file group !!
vocab_df = {} # doc freq. in file group

if USE_PICKLE:
    import pickle
    
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

def build_vocab_from_lines(lines):
    local_vocab = {}
    for line in lines:
        line = line.rstrip()
        sentences = re.split(ur'。|？|！', line)
        # sentences = line.split('。')
        for sc in sentences:
            # print n, '\t', to_unicode(sc) 
            # n += 1

            # get term freq.
            for word in langmodel.bigram_cn(sc):
                if word in local_vocab:
                    local_vocab[word] += 1
                else:
                    local_vocab[word] = 1

    if USE_PICKLE:
        for word in local_vocab:
            if word in vocabulary:
                vocabulary[word] += local_vocab[word]
            else:
                vocabulary[word] = local_vocab[word]
        return True
    elif USE_DATABASE:
        for word in local_vocab:
            v = query("vocabulary", word)
            if v > 0:
                update("vocabulary", word, v+local_vocab[word])
            else:
                insert("vocabulary", word, local_vocab[word])
        return True
    else:
        print "error: must configure whether use pickle or database"
        return False

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

def build_df_from_lines(lines):
    file_vocab = {} # term freq. in this file
    local_vocab_df = {}

    for line in lines:
        line = line.rstrip()
        sentences = re.split(ur'。|？|！', line)
        # sentences = line.split('。')
        for sc in sentences:
            # print n, '\t', to_unicode(sc) 
            # n += 1

            # get term freq. in this file
            for word in langmodel.bigram_cn(sc):
                if word in file_vocab:
                    file_vocab[word] += 1
                else:
                    file_vocab[word] = 1

    # get doc freq.
    for word in file_vocab:
        if word in local_vocab_df:
            local_vocab_df[word] += 1
        else:
            local_vocab_df[word] = 1


    if USE_PICKLE:
        for word in local_vocab_df:
            if word in vocab_df:
                vocab_df[word] += local_vocab_df[word]
            else:
                vocab_df[word] = local_vocab_df[word]
        return True
    elif USE_DATABASE:
        for word in local_vocab_df:
            v = query("vocab_df", word)
            if v > 0:
                update("vocab_df", word, v+local_vocab_df[word])
            else:
                insert("vocab_df", word, local_vocab_df[word])
        return True
    else:
        print "error: must configure whether use pickle or database"
        return False

def fwrite_dict(outfilename, dictobj):
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
    if USE_PICKLE:
        with open('vocabulary.pickle', 'wb') as f:
            pickle.dump(vocabulary, f) 

        with open('vocab_df.pickle', 'wb') as f:
            pickle.dump(vocab_df, f) 

    # sort the vocab and output
    fwrite_dict('vocabulary.txt', vocabulary)

    # sort the vocab of df and output
    fwrite_dict('vocab_df.txt', vocab_df)
