# -*- coding: utf-8 -*-

import sys
reload(sys) 
sys.setdefaultencoding('utf8')

def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
       if not isinstance(obj, unicode):
       	  obj = unicode(obj, encoding)
    return obj

if __name__ == "__main__": 
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

    sys.stdin.readline()
