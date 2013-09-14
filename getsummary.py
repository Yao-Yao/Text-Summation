#!/usr/bin/env python
#coding=utf-8
import StringIO

from basicmethods import *
import rankscale
import buildvocab

# - def insert(tablename, k, v)
# - def update(tablename, k, v)
# - def query(tablename, k) #fail: 0

#
# this function will be invoke by web app
#
# def get_summary(u_title, u_content) # fail: []
#
def get_summary(u_title, u_content):
    fbuffer = StringIO.StringIO(u_content)

    # get lines:
    lines = []

    line = fbuffer.readline()
    while line:
        lines.append(line)
        line = fbuffer.readline()
        
    # update vocabulary and vocab_df
    if not build_vocab_from_lines(lines):
        print "error: build vocabulary failed"
    if not build_df_from_lines(lines):
        print "error: build vocab of df failed"

    # return sentence list by descent order
    summary = rankscale.get_summary_from_lines(lines)
    if len(summary) > 0:
        return summary
    else:
        # summarizing process failed
        return summary # u_content[:140]

if __name__ == "__main__":
    content = rankscale.fgetlines('1.txt')

    summary = rankscale.get_summary_from_lines(content)
    for line in summary:
        print ""
        print to_unicode(line)
