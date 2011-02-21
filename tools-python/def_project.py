import pprint
import glob
import sys
import os
import copy

from def_class import *

class ProjectDef():
    
    def __init__(self, _rootdir):
        
        self.rootdir   = _rootdir       #Root directory of the project.
        self.filelist  = []             #List of class files in the project directory
        self.classlist = {}
        self.inherit_full_trees = {}
        self.inherit_trees      = {}
        self.interfaces         = []

        self.gen_filelist ()
        self.gen_classlist()

    def gen_filelist   (self):
        """Generates the list of class files in the current root directory, recursively."""
        self.filelist = []
        for path, dirlist, filelist in os.walk(self.rootdir):
            self.filelist.extend(glob.glob(os.path.join(path,'*.class')))

    def gen_classlist  (self):
        """Parses all the class files and generates a hash table with classname:classobj."""        
        self.classlist = {}
        for classfile in self.filelist:
            classobj = ClassDef(classfile)
            self.classlist[classobj.get_classname()] = classobj

    def get_superclass (self, name):
        """Returns the super class of the class with the given name."""
        if self.classlist[name].get_supername() not in self.classlist:   return None
        if self.classlist[name].get_supername().split('/')[0] == 'java': return None
        return self.classlist[self.classlist[name].get_supername()]

    def get_childclass (self, name):
        """Returns an array of classes inheriting from the class with the given name."""
        childlist = []
        for classentry in self.classlist.values():
            if classentry.get_supername() == name:
                childlist.append(classentry)
        return childlist

    def get_interfclass(self, name):
        """Returns an array of all the interfaces for the given class."""
        return [self.classlist[i] for i in self.classlist[name].get_intername() if i in self.classlist]

    def get_package(self, name):
        """Look for class in the class list and return the leading package. Careful to have different names in each package!"""
        for classname in self.classlist.keys():
            if classname.split('/')[-1] == name:
                return '/'.join(classname.split('/')[:-1])

    def get_allinterfaces(self):
        """Returns an array of all the interfaces in the current project."""
        if self.interfaces:
            return self.interfaces
        
        interfaces_list = []
        for classobj in self.classlist.values():
            interfaces_list.extend(classobj.get_intername())
        
        interfaces_list = set(interfaces_list)
        
        self.interfaces = interfaces_list
        return interfaces_list
        

    def get_impleminterfclass(self, name):
        """Returns an array of all the classes implementing a given interface."""
        implementlist = []
        for classentry in self.classlist.values():
            if name in classentry.get_intername():
                implementlist.append(classentry)
        return implementlist

    def get_implementinginterface(self, name):
        """Returns an array of all the classes implementing a given interface."""
        implementlist = []
        for classentry in self.classlist.values():
            if name in classentry.get_intername():
                implementlist.append(classentry.get_classname())
        return implementlist
        
    def get_classesref (self, name):
        """Returns all the class references in the given class."""
        return self.classlist[name].get_classref()

    def get_methodsref (self, name):
        """Returns all the methods references in the given class."""
        return self.classlist[name].get_methodsref()

    def get_fieldsref  (self, name):
        """Returns all the fields references in the given class."""
        return self.classlist[name].get_fieldsref()

    def get_methods    (self, name):
        """Returns all the methods in the given class."""
        return self.classlist[name].get_methods()

    def get_fields     (self, name):
        """Returns all the fields in the given class."""
        return self.classlist[name].get_fields()

    def get_methods_fullname    (self, name):
        """Returns all the methods in the given class."""
        return self.classlist[name].get_methods_fullname()

    def get_fields_fullname     (self, name):
        """Returns all the fields in the given class."""
        return self.classlist[name].get_fields_fullname()

    def get_methods_desc    (self, name):
        """Returns all the methods in the given class."""
        return self.classlist[name].get_methods_desc()

    def get_constructors    (self, name):
        """Returns all the methods in the given class."""
        return self.classlist[name].get_constructors()

    def get_fields_desc     (self, name):
        """Returns all the fields in the given class."""
        return self.classlist[name].get_fields_desc()

    def get_field_desc(self, classname, name):
        desc = None
        while not desc and self.get_superclass(classname):
            desc = self.classlist[classname].get_field_desc(classname, name)
            classname = self.get_superclass(classname).get_classname()
        return desc

    def get_method_desc(self, classname, name):
        desc = None
        while not desc and self.get_superclass(classname):
            desc = self.classlist[classname].get_method_desc(classname, name)
            classname = self.get_superclass(classname).get_classname()
        return desc        

    def get_method_desc_inclass(self, classobj, classname, name):
        return classobj.get_method_desc(classname, name)

    def get_field_desc_inclass(self, classobj, classname, name):
        return classobj.get_field_desc(classname, name)

    def get_ancestors       (self, name):
        ancestor_class_list = []
        
        ancestor_class_list = [name]
        ancestor = self.get_superclass(name)
        while ancestor:
            ancestor_class_list.append(ancestor.get_classname())
            ancestor = self.get_superclass(ancestor.get_classname()) 
            
        return ancestor_class_list

    def get_children        (self, name):
        children_class_list = []
        
        def recur_get_child(classobj, classlist):
            for child in self.get_childclass(classobj.get_classname()):
                classlist.append(child.get_classname())
                recur_get_child(child, classlist)
                
        recur_get_child(self.classlist[name], children_class_list)   
        
        return children_class_list

    def get_brothers        (self, name):
        brothers = []
        if self.get_superclass(name):
            ancestor = self.get_superclass(name).get_classname()
            brothers = self.get_children(ancestor)
        return brothers

    def get_cousins         (self, name):
        interfaces = [i.get_classname() for i in self.get_interfclass(name)]
        cousins = []
        for i in interfaces:
            cousins.extend(self.get_implementinginterface(i))
        return cousins

    def get_uncles (self,name):
        ancestors = self.get_ancestors(name)
        interfaces = []
        for i in ancestors:
            interfaces.extend(self.get_interfaces(i))
        uncles = []
        for i in interfaces:
            uncles.extend(self.get_implementinginterface(i))
        return uncles

    def get_interfaces         (self, name):
        return [i.get_classname() for i in self.get_interfclass(name)]

    def get_inherit_tree    (self, name):
        """Returns an array containing both the parents, interfaces and children names of a given class."""
        
        if name in self.inherit_trees:
            return self.inherit_trees[name]
        
        ancestor_class_list = []
        
        ancestor_class_list = [name]
        ancestor = self.get_superclass(name)
        while ancestor:
            ancestor_class_list.append(ancestor.get_classname())
            ancestor = self.get_superclass(ancestor.get_classname()) 

        inter_class_list = []
        for classname in ancestor_class_list:
            inter_class_list.append(classname)
            for interface in self.get_interfclass(classname):
                inter_class_list.append(interface.get_classname())

        
        def recur_get_child(classobj, classlist):
            for child in self.get_childclass(classobj.get_classname()):
                classlist.append(child.get_classname())
                recur_get_child(child, classlist)
                
        recur_get_child(self.classlist[name], inter_class_list)

        inter_class_list = set(inter_class_list)
        
        #for entry in inter_class_list:
        self.inherit_trees[name] = inter_class_list
        
        return inter_class_list

    def get_full_inherit_tree    (self, name):
        """Returns an array containing both the parents, interfaces and children names of a given class."""
        
        if name in self.inherit_full_trees:
            return self.inherit_full_trees[name]
        
        ancestor_class_list = []
        
        ancestor_class_list = [name]
        ancestor = self.get_superclass(name)
        while ancestor:
            ancestor_class_list.append(ancestor.get_classname())
            ancestor = self.get_superclass(ancestor.get_classname())        
        
        def recur_get_child(classobj, classlist):
            for child in self.get_childclass(classobj.get_classname()):
                classlist.append(child.get_classname())
                recur_get_child(child, classlist)
        
        child_class_list = []
        for ances_class in ancestor_class_list:
            child_class_list.append(ances_class)
            recur_get_child(self.classlist[ances_class], child_class_list)

        inter_class_list = []
        for classname in child_class_list:
            inter_class_list.append(classname)
            for interface in self.get_interfclass(classname):
                inter_class_list.append(interface.get_classname())

        implem_class_list = []
        for classname in inter_class_list:
            implem_class_list.append(classname)
            for interface in self.get_impleminterfclass(classname):
                implem_class_list.append(interface.get_classname())        

        implem_class_list = set(implem_class_list)
        
        for entry in implem_class_list:
            self.inherit_full_trees[entry] = implem_class_list
        
        return implem_class_list

    def apply_changes(self, name):
        self.classlist[name].apply_changes()

    def find_classes_implementing(self, member_type, name):
        """Returns an array of all the classes implementing a certain method/field.
        The method/field is given by its full name, including package and class (ie: /net/minecraft/src/Block/func_xxxx)."""
        class_name  = '/'.join(name.split('/')[:-1])
        member_name = name.split('/')[-1]
        
        if not class_name in self.classlist:
            return []
            #raise Warning('Invalid class. Not found !')
        
        #if not member_name in self.classlist[class_name].get_members(member_type):
        #    return []
            #raise Warning('Invalid %s %s for class %s. Not found !'%(member_type, member_name, class_name))

        #inherit_list = self.get_full_inherit_tree(class_name)
        inherit_list = self.get_inherit_tree(class_name)
        class_list   = []
        
       
        for classname in inherit_list:
            if member_name in self.classlist[classname].get_members(member_type):
                class_list.append(classname)

        return class_list

    def normalize_mapping_table  (self, classname, mappingtable):
        """Take a class to be renamed and a mapping table. It looks at all the entries in the class, and compare them to the
        mapping table. It creates a mapping table with the proper matchings"""
        
        #First we get the list of method, class and field references from the class
        if classname not in self.classlist:
            sys.stderr.write('ERROR : Class file for %s not found. Please check your compilation logs for errors.\n'%classname)
            sys.exit(0)
        
        ref = {}
        ref['Class']  = self.get_classesref(classname)
        ref['Method'] = self.get_methodsref(classname)
        ref['Field']  = self.get_fieldsref (classname)
        ref['Method'].extend(self.get_methods_fullname(classname))
        ref['Field'] .extend(self.get_fields_fullname(classname))
        
        #self.classlist[classname].print_fieldsref()
        #self.classlist[classname].print_methodsref()
        
        ref['Class']  = set(ref['Class'])
        ref['Method'] = set(ref['Method'])
        ref['Field']  = set(ref['Field'])
        
        member_array = []
        map_table = {}
        map_table['Class']  = {}
        map_table['Method'] = {}
        map_table['Field']  = {}
        
        if 'Class' in mappingtable:
            map_table['Class'] = mappingtable['Class']
        
        if 'Option' in mappingtable:
            map_table['Option'] = mappingtable['Option']

        map_table['Package'] = {}
        for entry in map_table['Option']:
            if entry['command'] == 'strip_package':
                map_table['Package'][entry['argument']] = ''        
        
        #Now we go through all the method references and check if we have a match in the hashtable
        members_keys = ['Method', 'Field']
        for member_key in members_keys:
            for member in ref[member_key]:
                
                
                member_name  = member.split('/')[-1]
                member_class = '/'.join(member.split('/')[:-1])
                member_sig   = None
                if member_key == 'Method':
                    member_sig = self.get_method_desc_inclass(self.classlist[classname], member_class, member_name)

                if member_sig:
                    #We obfuscate the signature for comparison
                    sig_regex = r'L([\w/]+);'
                    results = re.findall(sig_regex, member_sig)
                    for result in results:
                        try:
                            pack_result = '/'.join(result.split('/')[:-1])
                            member_sig = member_sig.replace('L%s;'%result, 'L%s/%s;'%(pack_result, mappingtable['Class'][result]))
                        except:
                            pass

                    for orig, dest in map_table['Package'].items():
                        if dest == '':
                            orig += '/'
                            
                        member_sig = member_sig.replace(orig, dest)
                
                #This is to protect all the methods & fields from outside the game.
                #If we have a class which is not in the map, we don't even consider renaming anything in it.
                if member_class not in self.classlist: continue
                
                #We don't care about creators, as they are renamed at the class renaming stage
                #Also some other protection on enums
                if member_name in ['<init>', '<clinit>', '_mthclass$']: continue
                
                #If the member is directly in the map, we just add it and continue
                if member in mappingtable[member_key]:
                    map_table[member_key][member] = mappingtable[member_key][member]
                    continue
                
                #We create a set of potential candidates
                candidate_list = [i for i in mappingtable[member_key].keys() if i.split('/')[-1] == member.split('/')[-1]]

                #For the methods, we check the signature
                if member_key == 'Method':
                    candidate_list = [i for i in candidate_list if mappingtable['Signature'][i] == member_sig]

                if len([i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_children(member_class)]) == 1:
                    candidate_list = [i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_children(member_class)]

                if len([i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_ancestors(member_class)]) == 1:
                    candidate_list = [i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_ancestors(member_class)]

                if len([i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_brothers(member_class)]) == 1:
                    candidate_list = [i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_brothers(member_class)]

                if len([i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_interfaces(member_class)]) == 1:
                    candidate_list = [i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_interfaces(member_class)]

                if len([i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_implementinginterface(member_class)]) == 1:
                    candidate_list = [i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_implementinginterface(member_class)]

                if len([i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_cousins(member_class)]) == 1:
                    candidate_list = [i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_cousins(member_class)]                    

                if len([i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_uncles(member_class)]) == 1:
                    candidate_list = [i for i in candidate_list if '/'.join(i.split('/')[:-1]) in self.get_uncles(member_class)]     

                #We only have one possibility
                if len(candidate_list) == 1:
                    map_table[member_key][member] = mappingtable[member_key][candidate_list[0]]
                    continue

                print "\t+ Found %d potential candidates for %s %s"%(len(candidate_list), member, member_sig)
                for i in candidate_list:
                    print "\t\t",i
                
                #If the member is not in the table, it means we don't have a good match
#                if member not in map_table[member_key]:
#                    sys.stderr.write("WARNING : Cannot find a proper entry for %s %s. Will not be reobfuscated.\n"%(member_key, member))
                #=========OLD VERSION===========
                
                #Now, we have the case where the member is not in the mappingtable and is from a known class
                #We check if it is defined somewhere else in his own heritance tree
#                member_family_array = [u'%s/%s'%(i,member_name) for i in self.get_inherit_tree(member_class)]
#                for sibling in member_family_array:
#                    if sibling in mappingtable[member_key]:
#                        map_table[member_key][member] = mappingtable[member_key][sibling]
#                        break
                
#                if member in map_table[member_key]: continue
                
                #We also check if the member is implemented somewhere else, as it would be the case for references.
#                member_imp_array = ([u'%s/%s'%(i,member_name) for i in self.find_classes_implementing(member_key, member)])
#                for implement in member_imp_array:
#                    if implement in mappingtable[member_key]:
#                        map_table[member_key][member] = mappingtable[member_key][implement]
#                        break
                
#                if member in map_table[member_key]: continue
                
                #And the classes implementing a given interface
#                class_itr_array = []
#                for interface in self.get_allinterfaces():
#                    class_itr_array.extend(self.get_impleminterfclass(interface))
#                member_itr_array = ([u'%s/%s'%(i.get_classname(),member_name) for i in class_itr_array])
#                for implement in member_itr_array:
#                    if implement in mappingtable[member_key]:
#                        map_table[member_key][member] = mappingtable[member_key][implement]
#                        break              
                
#                if member in map_table[member_key]: continue
                
                #Finally, the most dangerous case, a full tree search, up down and sideway. We HAVE to stop as soon as we are found one
#                member_family_array = [u'%s/%s'%(i,member_name) for i in self.get_full_inherit_tree(member_class)]
#                for sibling in member_family_array:
#                    if sibling in mappingtable[member_key]:
#                        map_table[member_key][member] = mappingtable[member_key][sibling]
#                        break
                
#                if member in map_table[member_key]: continue
                
                #If the member is not in the table, it means we don't have a good match
#                if member not in map_table[member_key]:
#                    print "WARNING : Cannot find a proper entry for %s %s. Will not be reobfuscated."%(member_key, member)
                
        return map_table

    def remap_all                (self, classname, mappingtable):
        self.classlist[classname].remap_methods (mappingtable['Method'], mappingtable['Class'])
        self.classlist[classname].remap_fields  (mappingtable['Field'],  mappingtable['Class'])
        self.classlist[classname].remap_classes (mappingtable['Class'])

    def remap_packages (self, classname, mappingtable):
        self.classlist[classname].remap_packages(mappingtable['Package'])

    def write_class(self, classname, directory):
        class_path = self.classlist[classname].get_classname()
        if os.sep != '/': class_path = class_path.replace('/', os.sep)
        self.classlist[classname].write_class(os.path.join(directory, class_path + '.class'))

    def print_dbformat(self, classname):
        a = self.classlist[classname].get_classname()
        b = self.classlist[classname].get_supername()
        c = self.classlist[classname].get_intername()
        
        if b.split('/')[0] == 'java':
            b = 'null'
        
        buffer = '%s %s'%(a,str(b))
        for i in c:
            buffer += ' +%s'%i
    
        print buffer
