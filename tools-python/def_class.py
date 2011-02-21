import StringIO 
from   construct   import *
import def_cstpool as CTPoolLib
import def_member  as MemberLib
import re
import os
import copy
import pprint

class ClassDef():

    def __init__(self, _filename):
        self.filename  = _filename
        self.stream    = None
    
        self.post_cp_buffer = None
        #Parsed elements
        self.header        = None
        self.cpool_count   = None
        self.cpool         = None
        self.inheritance   = None
        self.fields_count  = None
        self.fields        = None
        self.methods_count = None
        self.methods       = None
        self.attrbs_count  = None
        self.attrbs        = None        
        
        #Analysed elements
        self.classname   = None
        self.supername   = None
        self.intername   = None
        self.utf8entries = None

        self.open_file()
        self.parse_file()
        self.correct_utf8_multicalls()
        #self.check_utf8_multicalls()

    def __repr__(self):
        return "<ClassDef instance | %s>"%self.get_classname()

    def get_classname (self):
        """Returns the class name."""
        if not self.classname: raise Warning("Class %s not properly parsed or initialiased."%self.filename)
        return self.cpool[self.inheritance.this_class - 1].get_name()
        #return self.classname

    def get_supername (self):
        """Returns the super class name."""
        return self.supername

    def get_intername (self):
        """Returns the interface names."""
        return self.intername

    def get_classref  (self):
        return ['%s'%(i.get_name()) for i in self.cpool if i.Tag == 7]

    def get_methodsref(self):
        return ['%s/%s'%(i.get_class(),i.get_name()) for i in self.cpool if i.Tag in [10,11]]

    def get_fieldsref (self):
        return ['%s/%s'%(i.get_class(),i.get_name()) for i in self.cpool if i.Tag == 9]

    def get_methodsref_inst(self):
        return [i for i in self.cpool if i.Tag in [10,11]]

    def get_fieldsref_inst (self):
        return [i for i in self.cpool if i.Tag == 9]

    def get_members   (self, m_type):
        if m_type == 'Field':  return self.get_fields()
        if m_type == 'Method': return self.get_methods()

    def get_members_fullname   (self, m_type):
        if m_type == 'Field':  return self.get_fields_fullname()
        if m_type == 'Method': return self.get_methods_fullname()
    
    def get_fields    (self):
        return [i.get_name() for i in self.fields]

    def get_methods   (self):
        return [i.get_name() for i in self.methods]

    def get_fields_fullname    (self):
        return ['%s/%s'%(self.get_classname(),i.get_name()) for i in self.fields]

    def get_methods_fullname   (self):
        return ['%s/%s'%(self.get_classname(),i.get_name()) for i in self.methods]

    def get_fields_desc    (self):
        return ['%s/%s %s'%(self.get_classname(),i.get_name(), i.get_desc()) for i in self.fields]

    def get_methods_desc   (self):
        return ['%s/%s %s'%(self.get_classname(),i.get_name(), i.get_desc()) for i in self.methods]

    def get_field_desc     (self, classname, name):
        fieldsrefs = self.get_fieldsref_inst()
        for i in fieldsrefs:
            if i.get_name() == name and i.get_class() == classname:
                return i.get_desc()
        for i in self.fields:
            if i.get_name() == name and self.get_classname() == classname:
                return i.get_desc()
        return None            

    def get_method_desc    (self, classname, name):
        methodrefs = self.get_methodsref_inst()
        for i in methodrefs:
            if i.get_name() == name and i.get_class() == classname:
                return i.get_desc()        
        for i in self.methods:
            if i.get_name() == name and self.get_classname() == classname:
                return i.get_desc()
        return None            

    def print_fieldsref(self):
        fieldsrefs = self.get_fieldsref_inst()
        for i in fieldsrefs: print "%s %s %s"%(i.get_class(), i.get_name(), i.get_desc())

    def print_methodsref(self):
        methodrefs = self.get_methodsref_inst()
        for i in methodrefs: print "%s %s %s"%(i.get_class(), i.get_name(), i.get_desc())

    def get_constructors   (self):
        return ['%s/%s %s'%(self.get_classname(),i.get_name(), i.get_desc()) for i in self.methods if i.get_name() in ['<init>', '<clinit>']]

    def gen_calltable      (self):
        calltable = {}

        for cpentry in self.cpool:
            if cpentry.Tag in [8,9,10,11]:
                nameindex = cpentry.get_nameindex()
                if not nameindex in calltable: calltable[nameindex] = []
                calltable[nameindex].append(cpentry.index)

        for method in self.methods:
            nameindex = method.get_nameindex()
            if not nameindex in calltable: calltable[nameindex] = []
            calltable[nameindex].append(method.index)

        for field in self.fields:
            nameindex = field.get_nameindex()
            if not nameindex in calltable: calltable[nameindex] = []
            calltable[nameindex].append(field.index)

#       pprint.pprint( calltable)

        return calltable

    def correct_utf8_multicalls (self):
        
        calltable = self.gen_calltable()
        for key, call_list in calltable.items():
            
            #Protection for constructors.
            if self.cpool[key-1].get_name() in ['<init>', '<clinit>']: continue

            #If the list is one element long, just skip
            if len(call_list) == 1: continue
            
            while len(call_list) > 0:
                caller_index = call_list.pop()
                
                #We don't want to rename the implemented methods and other
                if caller_index > 2000:  continue
                
                caller    = self.cpool[caller_index-1]
                
                #If we have a string
                if caller.Tag == 8:
                    current_cpooli = len(self.cpool)+1
                    #print key, caller.index, '=>', current_cpooli, caller.get_name()
                    self.cpool.append(CTPoolLib.InfoUTF8(StringIO.StringIO('\x00\x01\x00'), current_cpooli))
                    self.cpool[current_cpooli-1].link_cpool(self.cpool)
                    self.cpool[current_cpooli-1].set_name(self.cpool[key-1].get_name())
                    self.cpool[current_cpooli-1].apply_changes()
                    caller.set_nameindex(current_cpooli)            
                
                #If we have an external method/field call
                elif caller.get_class() != self.get_classname():
                    
                    #We have to create a new Name&Type entry
                    nametype_cpooli = len(self.cpool)+1
                    self.cpool.append(CTPoolLib.InfoNameType(StringIO.StringIO('\x00\x00\x00\x00'), nametype_cpooli))
                    
                    #And a new UTF8Entry
                    utf8_cpooli = len(self.cpool)+1
                    self.cpool.append(CTPoolLib.InfoUTF8(StringIO.StringIO('\x00\x01\x00'),         utf8_cpooli))
                    
                    self.cpool[nametype_cpooli-1].link_cpool(self.cpool)
                    self.cpool[utf8_cpooli-1].link_cpool(self.cpool)
                    
                    #We copy the old text over the new cstpool utf8 entry
                    self.cpool[utf8_cpooli-1].set_name(self.cpool[key-1].get_name())
                    self.cpool[utf8_cpooli-1].apply_changes()

                    #We make the new name & type field point to the new utf8 entry
                    self.cpool[nametype_cpooli-1].data.NameIndex = utf8_cpooli
                    self.cpool[nametype_cpooli-1].data.DescIndex = self.cpool[caller.data.NameTypeIndex -1].data.DescIndex
                    
                    caller.data.NameTypeIndex = nametype_cpooli
                    


        self.cpool_count = len(self.cpool)+1
        #print self.cpool_count
        
    def check_utf8_multicalls (self):
        calltable = self.gen_calltable()
        for key, entry in calltable.items():
            if self.cpool[key - 1].Tag == 1 and len(entry) > 1:
                return True
        return False
                    

    def apply_changes(self):
        for utf8 in [i for i in self.cpool if i.Tag == 1]:
            utf8.apply_changes()

    def remap_descrip   (self, member, class_map):
        sig_regex = r'L([\w/]+);'
        desc    = member.get_desc()
        olddesc = member.get_desc()
        results = re.findall(sig_regex, desc)
        for result in results:
            try:
                pack_result = '/'.join(result.split('/')[:-1])
                desc = desc.replace('L%s;'%result, 'L%s/%s;'%(pack_result, class_map[result]))
            except:
                pass
        if desc != olddesc:
            member.set_desc(desc)        

    def remap_methods   (self, method_map, class_map):
        methodrefs = [i for i in self.cpool if i.Tag in [10,11]]
        
        #We replace the methods references
        for methodref in methodrefs:
            #method_name = '%s/%s %s'%(methodref.get_class(),methodref.get_name(),methodref.get_desc())method_name = '%s/%s %s'%(methodref.get_class(),methodref.get_name(),methodref.get_desc())
            method_name = '%s/%s'%(methodref.get_class(),methodref.get_name())
            if method_name in method_map: 
                methodref.set_name(method_map[method_name])
                #self.remap_descrip(methodref, class_map)
        
        #We replace the methods implementations
        for method in self.methods:
            #method_name = '%s/%s %s'%(self.get_classname(),method.get_name(),methodref.get_desc())
            method_name = '%s/%s'%(self.get_classname(),method.get_name())
            if method_name in method_map: 
                method.set_name(method_map[method_name])            
                #self.remap_descrip(method, class_map)

    def remap_fields    (self, field_map,  class_map):
        fieldrefs = [i for i in self.cpool if i.Tag == 9]        
        
        #We replace the methods references
        for fieldref in fieldrefs:
            field_name = '%s/%s'%(fieldref.get_class(),fieldref.get_name())
            if field_name in field_map: 
                fieldref.set_name(field_map[field_name])
                #self.remap_descrip(fieldref, class_map)
        
        #We replace the methods implementations
        for field in self.fields:
            field_name = '%s/%s'%(self.get_classname(),field.get_name())
            if field_name in field_map: 
                field.set_name(field_map[field_name])
                #self.remap_descrip(field, class_map)                

    def remap_classes   (self, class_map):
        classrefs = [i for i in self.cpool if i.Tag == 7]
        
        for classref in classrefs:
            if classref.get_name() in class_map:
                pkg_name   = '/'.join(classref.get_name().split('/')[:-1])
                class_name = classref.get_name().split('/')[-1]
                classref.set_name('%s/%s'%(pkg_name,class_map[classref.get_name()]))
                
        for entry in [i for i in self.cpool if i.Tag == 1]:
            self.remap_descrip(entry, class_map)    
        

    def remap_packages  (self, package_map):
        methodrefs = [i for i in self.cpool if i.Tag in [10,11]]
        fieldrefs  = [i for i in self.cpool if i.Tag == 9] 
        classrefs  = [i for i in self.cpool if i.Tag == 7]
        
        for orig, dest in package_map.items():
            if dest == '':
                orig += '/'
            for entry in methodrefs:
                entry.set_desc(entry.get_desc().replace(orig, dest))
            for entry in fieldrefs:
                entry.set_desc(entry.get_desc().replace(orig, dest))
            for entry in classrefs:
                entry.set_name(entry.get_name().replace(orig, dest))

            for entry in self.methods:
                entry.set_desc(entry.get_desc().replace(orig, dest))
            for entry in self.fields:
                entry.set_desc(entry.get_desc().replace(orig, dest))

            for entry in [i for i in self.cpool if i.Tag == 1]:
                entry.set_desc(entry.get_desc().replace(orig, dest))

    def open_file     (self):
        """Open the class file and generate the stream for later parsing"""
        ffin   = open(self.filename, 'rb')
        buffer = ffin.read()
        ffin.close()
        self.stream = StringIO.StringIO(buffer)
    
    def parse_file    (self):
        """Parses the header and the constant pool. Generates the cpool array"""
        self.header      = self.Struct_Header .parse_stream(self.stream)
        
        #Parse the constant pool
        self.cpool       = []
        self.cpool_count = self.Struct_CPCount.parse_stream(self.stream)
        cp_index = 0
        while cp_index < self.cpool_count-1:
            tag = self.Struct_CPTag.parse_stream(self.stream)
            self.cpool.append(CTPoolLib.InfoType[tag](self.stream, cp_index+1))
            if tag == 5 or tag == 6:
                self.cpool.append(CTPoolLib.InfoDummy(self.stream, cp_index+1))
                # self.constant_pool[-1]
                cp_index += 1

            cp_index += 1

        for entry in self.cpool:
            entry.link_cpool(self.cpool)

        self.utf8entries = [i for i in self.cpool if i.Tag == 1]    #List of all the utf8 entries

        post_cp_anchor = self.stream.tell()

        #Parse inheritance data
        self.inheritance = self.Struct_Inherit.parse_stream(self.stream)
        self.classname   = self.cpool[self.inheritance.this_class  - 1].get_name()
        self.supername   = self.cpool[self.inheritance.super_class - 1].get_name()

        self.intername   = []
        for entry in self.inheritance.interfaces:
            self.intername.append(self.cpool[entry.ClassIndex - 1].get_name())
 
        #Parse fields
        indexfield         = 10001
        self.fields_count  = self.Struct_FieldsCount. parse_stream(self.stream)
        self.fields = []
        for ifield in range( self.fields_count):
            self.fields.append(MemberLib.FieldDef(self.stream, self.cpool, indexfield))
            indexfield += 1
            
        #Parse methods
        indexmethod        = 20001
        self.methods_count = self.Struct_MethodsCount.parse_stream(self.stream)
        self.methods = []
        for imethod in range( self.methods_count):
            self.methods.append(MemberLib.MethodDef(self.stream, self.cpool, indexmethod))        
            indexmethod += 1
            
        #Parse attributes
        indexattrb         = 30001
        self.attrbs_count  = self.Struct_AttrbsCount. parse_stream(self.stream)
        self.attrbs = []
        for iattrb in range( self.attrbs_count):
            self.attrbs.append(MemberLib.AttribDef(self.stream, self.cpool, indexattrb))         
            indexattrb += 1

        self.stream.seek(post_cp_anchor)
        self.post_cp_buffer = self.stream.read()

    def write_class(self, filename):
        try: os.makedirs(os.path.dirname(filename))
        except OSError: pass
            
        print "Writing out %s."%filename
        ffout = open(filename, 'wb')
        
        self.Struct_Header.build_stream(self.header, ffout)
        self.Struct_CPCount.build_stream(self.cpool_count, ffout)
        for entry in self.cpool:
            entry.write_stream(ffout)
        ffout.write(self.post_cp_buffer)
        
        ffout.close()

    Struct_Header       = Struct ("ConstantPoolHeader", UBInt32("magic"), UBInt16("minor_version"), UBInt16("major_version"))
    Struct_CPCount      = UBInt16("constant_pool_count")
    Struct_CPTag        = UBInt8 ("tag")
    Struct_Inherit      = Struct ("Inheritance", UBInt16("access_flags"), UBInt16("this_class"), UBInt16("super_class"), UBInt16("interfaces_count"), MetaRepeater(lambda ctx: ctx["interfaces_count"], Struct("interfaces", UBInt16("ClassIndex"))))
    Struct_FieldsCount  = UBInt16("fields_count")
    Struct_MethodsCount = UBInt16("methods_count")
    Struct_AttrbsCount  = UBInt16("attrbs_count")
