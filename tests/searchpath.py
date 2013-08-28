import os
import sys

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
    dataDir = '../article'
    pathlist = ls_dir(dataDir)
    for path in pathlist:
    	print path
    	
    print "\n****** press any key to exit ******"
    sys.stdin.readline()
