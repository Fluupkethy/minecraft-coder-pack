import os
import re
import md5
import sys
import glob
import time
import shutil
import pprint

from optparse import OptionParser

sys.path.append('..')
sys.path.append('../parsers')

import parsers
import annotate_gl_constants as GLConstants

def create_dic_class (parsed_rgs):
    return_dic = {}
    for entry in parsed_rgs['class_map']:
        notch_data = entry['src_name'].split('/')
        return_dic[entry['trg_name']] = {}                
        return_dic[entry['trg_name']]['notch']      = notch_data[-1]
        return_dic[entry['trg_name']]['searge']     = entry['trg_name']
        return_dic[entry['trg_name']]['full']       = entry['trg_name']
        return_dic[entry['trg_name']]['class']      = entry['trg_name']
        return_dic[entry['trg_name']]['full_final'] = entry['trg_name']
        return_dic[entry['trg_name']]['notch_pkg']  = '/'.join(notch_data[:-1])
        return_dic[entry['trg_name']]['modified']   = False 

    return return_dic

def create_dic_member(parsed_rgs, parsed_csv, class_dict, target, type, config):
    return_dic = {}

    rev_class_dict = {}
    for key,value in class_dict.items():
        rev_class_dict[value['notch']] = key

    for entry in parsed_rgs[type]:
        
        notch_data = entry['src_name'].split('/')
        
        s_root = entry['trg_name']
        if entry['trg_name'].find('func') != -1 or entry['trg_name'].find('field') != -1:
            s_root = '_'.join(entry['trg_name'].split('_')[0:2])
        else:
            s_root = notch_data[-2] + '_' + entry['trg_name']
        
        
        
        return_dic[s_root] = {}
        return_dic[s_root]['notch']       = notch_data[-1]
        return_dic[s_root]['searge']      = entry['trg_name']
        return_dic[s_root]['s_root']      = s_root
        return_dic[s_root]['full']        = None
        return_dic[s_root]['full_final']  = None
        return_dic[s_root]['notch_sig']   = None
        return_dic[s_root]['csv']         = None
        return_dic[s_root]['index']       = s_root.split('_')[-1]
        return_dic[s_root]['known']       = False
        return_dic[s_root]['notch_class'] = notch_data[-2]
        return_dic[s_root]['notch_pkg']   = '/'.join(notch_data[:-2])
        return_dic[s_root]['class']       = None
        return_dic[s_root]['descript']    = None
        return_dic[s_root]['package']     = config['package_name']
        
        #Bot related keys
        return_dic[s_root]['old_mod']     = False   #This modification has already been commited and is considered permanent
        return_dic[s_root]['new_mod']     = False   #This is a new modification to be commited on next update
        return_dic[s_root]['modified']    = False   #The entry has been modified
        return_dic[s_root]['nick_mod']    = None    #The name of the guy who did the last set on this entry
        return_dic[s_root]['time_mod']    = None    #The time of the modification
        return_dic[s_root]['forced']      = False   #If this entry has been forced modified
        return_dic[s_root]['annotation']  = ''      #Some infos which may be usefull later one
        
        try:
            return_dic[s_root]['class']       = rev_class_dict[notch_data[-2]]
        except:
            return_dic[s_root]['class']       = return_dic[s_root]['notch_class']
        
        if type == 'method_map':
            return_dic[s_root]['notch_sig']   = entry['src_sig']
        
    #We create a dict lookup based on the csv
    member_lookup = {}
    descri_lookup = {}
    for entry in parsed_csv:
        s_root = entry['searge_%s'%target]
        if entry['searge_%s'%target].find('func') != -1 or entry['searge_%s'%target].find('field') != -1:
            s_root = '_'.join(entry['searge_%s'%target].split('_')[0:2])        
        member_lookup[s_root] = entry['full']
        if 'description' in entry:
            descri_lookup[s_root] = entry['description']
        else:
            descri_lookup[s_root] = '*'

    #Now, we go through the return_dict, and associate the corresponding full name to the corresponding key
    #If we don't have a fullname, we 'star' it for later parsing
    known_name_repr   = config['known_name'].split('+')
    unknown_name_repr = config['unknown_name'].split('+')
    for part in known_name_repr:
        if part not in ['notch', 'searge', 's_root', 'csv', 'index']:
            raise KeyError("Unknown qualifier for representation. Choose in ['notch', 'searge', 's_root', 'csv', 'index'] separated by '+'")
    for part in unknown_name_repr:
        if part not in ['notch', 'searge', 's_root', 'csv', 'index']:
            raise KeyError("Unknown qualifier for representation. Choose in ['notch', 'searge', 's_root', 'csv', 'index'] separated by '+'")

    for key in return_dic.keys():
        try:
            return_dic[key]['csv']   = member_lookup[return_dic[key]['s_root']]
            return_dic[key]['known'] = True
        except KeyError:
            return_dic[key]['csv'] = return_dic[key]['s_root']

    for key in return_dic.keys():
        try:
            return_dic[key]['descript']   = descri_lookup[return_dic[key]['s_root']]
        except KeyError:
            return_dic[key]['descript']   = '*'
    
    for key in return_dic.keys():
        if return_dic[key]['known']:
            return_dic[key]['full']       = member_lookup[return_dic[key]['s_root']]
            return_dic[key]['full_final'] = '_'.join([return_dic[key][i] for i in known_name_repr])

        else:
            if return_dic[key]['searge'].find('func') != -1 or return_dic[key]['searge'].find('field') != -1:
                return_dic[key]['full']       = return_dic[key]['s_root']
                return_dic[key]['full_final'] = '_'.join([return_dic[key][i] for i in unknown_name_repr])
            else:
                return_dic[key]['full']       = return_dic[key]['searge']
                return_dic[key]['full_final'] = return_dic[key]['searge']

# Commented this part. It will make sure to have full final names with the notch extended, even if it is one of the enum.
# Not sure if it should be done or not.
#            if return_dic[key]['searge'].find('func') != -1 or return_dic[key]['searge'].find('field') != -1:
#                return_dic[key]['full']       = return_dic[key]['searge']
#                return_dic[key]['full_final'] = return_dic[key]['searge']
#            else:
#                return_dic[key]['full']       = return_dic[key]['searge']
#                return_dic[key]['full_final'] = return_dic[key]['searge'] + '_' + return_dic[key]['notch']
            
    return return_dic

def solve_collisions (member_dic):
    unique_names = set()
    
    #We protect the class names by adding them before hand
    for key in member_dic['class'].keys():
        if member_dic['class'][key]['full_final'] not in unique_names :
            unique_names.add(member_dic['class'][key]['full_final'])
        else:
            raise KeyError("Duplicated class name : %s"%member_dic['class'][key]['full_final'])

    for group in ['method', 'field']:
        for key in member_dic[group].keys():
            index = 0
            start_name = member_dic[group][key]['full_final']
            curr_name  = member_dic[group][key]['full_final']
            while curr_name in unique_names :
                curr_name = start_name + '_%02d'%index
                index += 1
            unique_names.add(curr_name)
            member_dic[group][key]['full_final'] = curr_name
        

def parse_all_files  (config_file):
    renamer_options = { 'class_csv'       : None,
                        'field_csv'       : None,
                        'method_csv'      : None,
                        'server_rgs'      : None,
                        'client_rgs'      : None,
                        'server_rgs_out'  : None,
                        'client_rgs_out'  : None,
                        'server_src'      : None,
                        'client_src'      : None,
                        'package_name'    : None,
                        'unknown_name'    : None,
                        'known_name'      : None,
                        'md5_file_client' : None,
                        'md5_file_server' : None,
                        }

    config     = parsers.parse_config(config_file, renamer_options)
    
    class_csv  = parsers.parse_csv(config['class_csv'],  3, ',', ['full',      'trashbin', 'notch_c',  'trashbin',  'notch_s', 'description'])
    method_csv = parsers.parse_csv(config['method_csv'], 4, ',', ['trashbin',  'searge_c', 'trashbin', 'searge_s',  'full', 'description'])    
    field_csv  = parsers.parse_csv(config['field_csv'],  3, ',', ['trashbin',  'trashbin', 'searge_c', 'trashbin',  'trashbin', 'searge_s', 'full', 'description'])    
    
    client_rgs = parsers.parse_rgs(config['client_rgs']) #contains a list of notch_name to searge_name for the client
    server_rgs = parsers.parse_rgs(config['server_rgs']) #contains a list of notch_name to searge_name for the server

    #We want 3 dicts per soft. One for classes, methods and fields. Each dict is going to take the searge_name as the key, as it is the only
    #unique identifier we are sure of for now. Each dict will have at least 3 entries, notch_name, searge_name and full_name.
    #Classes will have an identical searge_name and full_name, as they are identical. Methods will also contain the notch_signature and maybe the searge_signature.
    #Packages can also be a value somewhere for the reobfuscation step.

    #Let's start with the class dictionary. For this one, we just need the rgs file.
    class_dict_c = create_dic_class(client_rgs)
    class_dict_s = create_dic_class(server_rgs)

    #Now the fields, as they are easy to process. Need both the csv and the rgs. Third argument is to get the right column
    field_dict_c = create_dic_member(client_rgs, field_csv, class_dict_c, 'c', 'field_map', config)
    field_dict_s = create_dic_member(server_rgs, field_csv, class_dict_s, 's', 'field_map', config)

    #And finally the methods. Same as before.
    method_dict_c = create_dic_member(client_rgs, method_csv, class_dict_c, 'c', 'method_map', config)
    method_dict_s = create_dic_member(server_rgs, method_csv, class_dict_s, 's', 'method_map', config)

    client_dic = {'class':class_dict_c, 'method':method_dict_c, 'field':field_dict_c}
    server_dic = {'class':class_dict_s, 'method':method_dict_s, 'field':field_dict_s}

    #solve_collisions(client_dic)
    #solve_collisions(server_dic)

    return client_dic, server_dic, config

def walk_sources     (dir, conv_dict, md5file, skipopengl=False):
    
    for path, dirlist, filelist in os.walk(dir):
        remap_sources(path, conv_dict, md5file, skipopengl)
        
def remap_sources    (dir, conv_dict, md5file, skipopengl=False):
    
    print '+ Renaming in %s.'%(dir)

    type_hash         = {'method':'func', 'field':'field'}
    regexp_searge     = r'%s_[0-9]+_[a-zA-Z]+_?'
    regexp_full_final = r'%s_[0-9]+_[a-zA-Z]+_?'
    final_hash        = {'method':{}, 'field':{}}
    for group in ['method', 'field']:
        for key in conv_dict[group].keys():
            final_hash[group][conv_dict[group][key]['full_final']] = conv_dict[group][key]
    
    number_results_bef = 0.
    number_results_aft = 0.

   
    for src_file in glob.glob(os.path.join(dir,'*.java')):
        
        fi = open(src_file, 'r')
        fo = open(src_file + '.tmp', 'w')
        
        buffer = fi.read()
       
        for group in ['method', 'field']:
            results = re.findall(regexp_searge%type_hash[group], buffer)
            number_results_bef += len(results)
            for result in results:
                try:
                    buffer = buffer.replace(result, conv_dict[group]['_'.join(result.split('_')[0:2])]['full_final'])
                except KeyError:
                    pass
            results = re.findall(regexp_searge%type_hash[group], buffer)
            number_results_aft += len(results)
#            for entry in conv_dict[group].values():
#                if entry['searge'].find('field') != -1 or entry['searge'].find('func') != -1:
#                    if entry['searge'] != entry['full_final']:
#                        buffer = buffer.replace(entry['searge'], entry['full_final'])
        
        md5_digest = md5.new(buffer).hexdigest()
        md5file.write ('%s\t%s\n'%(src_file, md5_digest))
        
        fo.write(buffer)
        
        fi.close()
        fo.close()

        shutil.move(src_file + '.tmp', src_file)

        #Call the OpenGL Cst renamer on this file unless we skip renaming (name_update)
        if not skipopengl:
            GLConstants.annotate_file(src_file)
        

#    print "Number of fields/methods before renaming : %d"%number_results_bef
#    print "Number of fields/methods after  renaming : %d"%number_results_aft

def write_reobf      (dir, pkg_name, conv_dict, config):
    
    fo = open(dir, 'wb')
    
    fo.write('[OPTIONS]\n')
    fo.write('strip_package %s\n'%pkg_name)
    fo.write('\n')    
    
    type_match = {'class':'[CLASSES]', 'field':'[FIELDS]', 'method':'[METHODS]'}
    
    for group in ['class', 'field', 'method']:
        fo.write('%s\n'%type_match[group])
        for entry in conv_dict[group].values():
            if entry['notch_pkg']:
                pkg = entry['notch_pkg']
            else:
                pkg = config['package_name']
            if group == 'method':
                fo.write('%s/%s/%s %s %s\n'%(pkg, entry['class'], entry['full_final'], entry['notch_sig'], entry['notch']))
            elif group == 'field':
                fo.write('%s/%s/%s %s\n'%(pkg, entry['class'], entry['full_final'], entry['notch']))
            else:
                fo.write('%s/%s %s\n'%(pkg, entry['full_final'], entry['notch']))
        
        fo.write('\n')
        
    fo.close()

def main(options, args):
    client_dic, server_dic, config = parse_all_files(options.conf)

#    pprint.pprint( client_dic['method'])
#    pprint.pprint( server_dic['method'])
#    pprint.pprint( client_dic['field'])
#    pprint.pprint( server_dic['field'])

    if options.recursive:
        rename_sources = walk_sources
    else:
        rename_sources = remap_sources

    
    fmd5_client = open(config['md5_file_client'], 'w')
    fmd5_server = open(config['md5_file_server'], 'w')
    rename_sources(config['client_src'], client_dic, fmd5_client, options.skipopengl)
    rename_sources(config['server_src'], server_dic, fmd5_server)
    fmd5_client.close()
    fmd5_server.close()

    write_reobf(config['client_rgs_out'], config['package_name'], client_dic, config)
    write_reobf(config['server_rgs_out'], config['package_name'], server_dic, config)

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--conf", dest="conf",      default='renamer.conf', help="Configuration file for the renamer. Default to renamer.conf.")  
    parser.add_option("-R",           dest="recursive",  action="store_true",   help="Control if the sources renaming should be recursive or not. Default to no.")   
    parser.add_option("--skipopengl",  dest="skipopengl", action="store_true",   help="Control if the opengl annoter should be skip. Default to false.")       
    (options, args) = parser.parse_args()      
    
    main(options, args)
