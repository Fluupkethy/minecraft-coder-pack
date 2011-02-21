import os
from optparse import OptionParser

def main(options, args):
    for path, dirlist, filelist in os.walk(options.dir):
        if args[0] in filelist:
            print path

if __name__ == '__main__':
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dir", dest="dir", default='C:\\Program files\\', help="Root directory for search. Default to C:\\Program files\\")      
    (options, args) = parser.parse_args()      
        
    main(options, args)
