#!/usr/bin/env python
#coding=utf-8

import re
import codecs
import os
import pickle
import math

from basicmethods import *
import langmodel

# deserialization
with open('vocab_df.pickle', 'rb') as f:
    vocab_df = pickle.load(f) 
# vocabulary = {} # term freq. in file group !!

TOTAL_FILE_NUM = 405

##def convert_cn(s):
##    return s.encode('gb18030')  # gb2312 cannot work

def scale_func(x):
    # return float(x+1)/(x)
    # return 1
    return 1.0/math.sqrt(x)
    # return 1.0/x

def calculate_tfidf_norm_for_sc(sc, vocab_df):
    score = 0
    for word in langmodel.bigram_cn(sc):
        score += -math.log(float(vocab_df[word])/TOTAL_FILE_NUM)

    if len(sc) > 0:
        return float(score)*scale_func(len(sc))
    else:
        return 0

def print_tfidf(dictobj, outfilename):
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

def summary_from_file(filepath):
    f = codecs.open(filepath, 'r', 'utf-8')
    # n = 1

    # skip first two lines, i.e. url
    line = f.readline()
    # print line
    line = f.readline()
    line = f.readline()
    # print to_unicode(line)

    sentcs_tfidf = {}
    # for line in f.readlines():
    while line:
        line = line.rstrip()
    	sentences = re.split(ur'。|？|！', line)
        # sentences = line.split('。')

    	for sc in sentences:
            # print n, '\t', to_unicode(sc) 
            # n += 1

            # for each sc, add every word's idf
            sentcs_tfidf[sc] = calculate_tfidf_norm_for_sc(sc, vocab_df)
        line = f.readline()
    f.close()

    # sort the sentcs_tfidf and output sentcs
    filename = os.path.basename(filepath)
    sumfilename = filename.replace('.', '_rankscale.')
    print_tfidf(sentcs_tfidf, sumfilename)

#def insert(k, v)
#def update(k, v)
#def query(k) #fail: None

#fail: u_content[:140] + ... 
def get_summary(u_title, u_content):
    pass

if __name__ == "__main__": 
    # list all file paths in directory 'article'
    dataDir = 'article'
    pathlist = ls_dir(dataDir)
    for path in pathlist:
        print path
        summary_from_file(path)
    # summary_from_file('1.txt')
    
    print to_unicode("\n****** 按任意键退出! ******")
    sys.stdin.readline()
