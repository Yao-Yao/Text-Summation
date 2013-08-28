# -*- coding: utf-8 -*-

import os
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
       if not isinstance(obj, unicode):
       	  obj = unicode(obj, encoding)
    return obj

# list all file paths in directory
def ls_dir(data_dir):
	pathlist = []
	for lists in os.listdir(data_dir): 
	    path = os.path.join(data_dir, lists) 
	    if os.path.isfile(path): 
	    	#print os.path.basename(path)
	    	pathlist.append(path)
	return pathlist
    
if __name__ == "__main__": 
    # search all files in directory 'article'
    dataDir = 'article'
    pathlist = ls_dir(dataDir)
    for path in pathlist:
    	print path

    a = '友谊地久天长'
    print 'a = ', a
    print 'len(a) = ', len(a)
    b = 'haha'
    print 'b = ', b
    print 'len(b) = ', len(b)
    
    ua = to_unicode(a)
    print 'ua = ', ua
    print 'len(ua) = ', len(ua)
    ub = to_unicode(b)
    print 'ub = ', ub
    print 'len(ub) = ', len(ub)
    
    print "\n****** press any key to exit ******"
    sys.stdin.readline()
