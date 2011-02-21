#!/usr/bin/python

#Code by ProfMobius, Oct 2010
#You are welcome to do whatever you want with it, as long as you keep the credits.
#Have fun !

import csv
import pprint
import re
import os
import urllib
import glob
import shutil
from optparse import OptionParser

def get_csv(options, args):

    path = options.dir

    class_filename = os.path.join(path, 'classes.csv')
    field_filename = os.path.join(path, 'fields.csv')
    func_filename  = os.path.join(path, 'methods.csv')

    print '== Updating csv files. =='

    print '+ Deleting old csv files.'
    if os.path.exists(class_filename):
        os.remove(class_filename)

    if os.path.exists(field_filename):
        os.remove(field_filename)

    if os.path.exists(func_filename):
        os.remove(func_filename)

    print '+ Downloading new csv files.'
    url_class  = 'http://mcp.ocean-labs.de/files/renamer_csv/classes.csv'
    url_field  = 'http://mcp.ocean-labs.de/files/renamer_csv/fields.csv'
    url_method = 'http://mcp.ocean-labs.de/files/renamer_csv/methods.csv'

    urllib.urlretrieve(url_class,  filename=class_filename)
    urllib.urlretrieve(url_field,  filename=field_filename)
    urllib.urlretrieve(url_method, filename=func_filename)

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dest", dest="dir", default='', help="Indicate which directory to output the csv to. Default is current directory.")
    (options, args) = parser.parse_args()

    get_csv(options, args)
