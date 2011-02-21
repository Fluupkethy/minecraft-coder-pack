import sys
import time
import shutil
import pprint
import os
import re
import glob
import shutil
import urllib
import md5
sys.path.append('..')
sys.path.append('../parsers')
sys.path.append('../obfuscathon_v2')
sys.path.append('../renamer_v3')

import parsers
import def_project
import annotate_gl_constants

from optparse import OptionParser

def get_class_list(filename):
    ff = open(filename, 'r')
    
    class_list = []
    
    while True:
        buffer = ff.readline()
        
        if not buffer:
            break  
        
        class_name = os.path.splitext(buffer.strip())[0]
        if os.sep != '/': class_name = class_name.replace(os.sep, '/')

        class_name = list(class_name.rpartition('/'))
        if len(class_name[0]) == 0:
            class_name[1] = '/'
            class_name[0] = 'net/minecraft/src'
            if class_name[2] in ['Minecraft', 'MinecraftApplet']: class_name[0] = 'net/minecraft/client'
            if class_name[2] in ['MinecraftServer']: class_name[0] = 'net/minecraft/server'

        class_name = ''.join(class_name)

        class_list.append(class_name)
    
    return class_list

def main(options, args):
    conf   = options.conf
    obf    = options.obf
    indir  = options.indir
    outdir = options.outdir
    
#    if not conf or not obf or not indir or not outdir:
#        conf   = 'client_obfuscation.txt'
#        obf    = 'minecraft_rev.saffx'
#        indir  = 'bin/minecraft'
#        outdir = 'out'
    
    class_list   = get_class_list(conf)
    parsed_match = parsers.parse_saffx(obf)
    parsed_match['Option'] = parsed_match['options']
    parsed_match['Class']     = {}
    parsed_match['Method']    = {}
    parsed_match['Field']     = {}
    parsed_match['Signature'] = {}
    signat_table              = {}
    
    for value in parsed_match['classes']:
        parsed_match['Class'][value['src_name']] = value['trg_name']
    for value in parsed_match['methods']:
        parsed_match['Method'][value['src_name']] = value['trg_name']
    for value in parsed_match['methods']:
        parsed_match['Signature'][value['src_name']] = value['src_sig']        
    for value in parsed_match['fields']:
        parsed_match['Field'][value['src_name']] = value['trg_name']


    
    print ('+ Reading classes in %s.'%indir)
    current_project = def_project.ProjectDef(indir)
    for classname in class_list:
        print ('+ Normalizing mapping tables for %s.'%classname)
        match_table = current_project.normalize_mapping_table(classname, parsed_match)
        print ('+ Remapping %s.'%classname)
        current_project.remap_all(classname, match_table)
    
    for classname in class_list:
        current_project.apply_changes (classname)
        current_project.remap_packages(classname, match_table)
        current_project.apply_changes (classname)

        current_project.write_class(classname, outdir)
    
if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--conf", dest="conf", help="List of classes to reobfuscate.")
    parser.add_option("-d", dest="obf",            help="Obfuscation table.")
    parser.add_option("-i", dest="indir",          help="Root of the directory to search for the class files.")
    parser.add_option("-o", dest="outdir",         help="Target directory for reobfuscated classes.")
    (options, args) = parser.parse_args()      
    
    main(options, args)
