#!/usr/bin/env python
#coding=utf-8

#
# generate ranked sentences from 
#

import re
import codecs
import os
import math

from basicmethods import *
import langmodel

TOTAL_FILE_NUM = 405
USE_PICKLE = True
USE_DATABASE = False

#
# read from vocabulary/vocab_df
# (1) deserialization from pickle file
# vocabulary = {} # term freq. in file group !!
# (2) get from database
# interface given by web app:
# - def insert(k, v)
# - def update(k, v)
# - def query(k) #fail: 0
#
if USE_PICKLE:
    import pickle
    with open('vocab_df.pickle', 'rb') as f:
        vocab_df = pickle.load(f) 

def get_df(word):
    if USE_PICKLE:
        return vocab_df[word]
    elif USE_DATABASE:
        return query(word)
    else:
        print "error: must configure whether use pickle or database"
        return -1

##def convert_cn(s):
##    return s.encode('gb18030')  # gb2312 cannot work

def scale_func(x):
    # return float(x+1)/(x)
    # return 1
    return 1.0/math.sqrt(x)
    # return 1.0/x

def tfidf_norm_for_sentence(sentence):
    score = 0
    for word in langmodel.bigram_cn(sentence):
        # get df value
        df = get_df(word)
        if df > 0:
            score += -math.log(float(df)/TOTAL_FILE_NUM)
        else:
            print "error: df less than 0"
            score = 0

    if len(sentence) > 0:
        return float(score)*scale_func(len(sentence))
    else:
        return 0

def fwrite_dict(outfilename, dictobj):
    outputdir = 'article_rankscale'
    outfilepath = os.path.join(outputdir, outfilename) 
    outfile = open(outfilepath, 'w')
    for w in sorted(dictobj.items(), key=lambda x:x[1], reverse=True):
        # print w[0], w[1]
        outfile.write(to_unicode(w[0]))
        outfile.write('\n')
        outfile.write('tfidf = '+str(w[1]))
        outfile.write('\n\n')
    outfile.close()
        
def fgetlines(filepath):
    f = codecs.open(filepath, 'r', 'utf-8')
    # n = 1

    # file structure:
    
    # <url>
    #
    # <title>
    #
    # <content>: multi-lines
    # ...
    
    # skip url line
    url = f.readline()
    # print line

    # skip blank line
    f.readline()

    # get title
    title = f.readline()
    # print to_unicode(line)

    # get content lines:
    content = []

    line = f.readline()
    while line:
        content.append(line)
        line = f.readline()
        
    return content
    
def fsummary(filepath):
    f = codecs.open(filepath, 'r', 'utf-8')
    # n = 1

    # file structure:
    
    # <url>
    #
    # <title>
    #
    # <content>: multi-lines
    # ...
    
    # skip url line
    url = f.readline()
    # print url

    # skip blank line
    f.readline()

    # get title
    title = f.readline()
    # print to_unicode(line)

    #
    # start from content:
    #
    
    sentcs_tfidf = {}
    
    # for line in f.readlines(): # get exception when use this line of code
    line = f.readline()
    while line:
        line = line.rstrip()
    	sentences = re.split(ur'。|？|！', line)
        # sentences = line.split('。')

    	for sc in sentences:
            # print n, '\t', to_unicode(sc) 
            # n += 1

            # for each sc, add every word's idf
            sentcs_tfidf[sc] = tfidf_norm_for_sentence(sc)
        line = f.readline()

    f.close()

    return sentcs_tfidf

def get_summary_from_lines(lines):
    #
    # start from content lines:
    #
    
    sentcs_tfidf = {}

    for line in lines:        
        line = line.rstrip()
    	sentences = re.split(ur'。|？|！', line)

    	for sc in sentences:
            # print n, '\t', to_unicode(sc) 
            # n += 1
            print ""
            print to_unicode(sc)
            # for each sc, add every word's idf
            sentcs_tfidf[sc] = tfidf_norm_for_sentence(sc)

    # sort the sentcs_tfidf and output sentcs
    outputsum = []
    for w in sorted(sentcs_tfidf.items(), key=lambda x:x[1], reverse=True):
        # print w[0], w[1]
        outputsum.append(to_unicode(w[0]))
##        print 'tfidf = '+str(w[1])

    return outputsum

if __name__ == "__main__": 
    # list all file paths in directory 'article'
    dataDir = 'article'
    pathlist = ls_dir(dataDir)
    for path in pathlist:
        print "summary from file:", path
        sentences_tfidf = fsummary(path)
        
        # sort the sentcs_tfidf and output sentences
        filename = os.path.basename(path)
        sumfilename = filename.replace('.', '_rankscale.')
        fwrite_dict(sumfilename, sentences_tfidf)
    
##    sentences_tfidf = fsummary('1.txt')
##    # sort the sentcs_tfidf and output sentences
##    filename = os.path.basename(path)
##    sumfilename = filename.replace('.', '_rankscale.')
##    fwrite_dict(sumfilename, sentences_tfidf)
        
##    lines = fgetlines('1.txt')
##    summary = get_summary_from_lines(lines)
##    for line in summary:
##        print ""
##        print to_unicode(line)

