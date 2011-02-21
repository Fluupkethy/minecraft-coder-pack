from   construct import *
import StringIO
import copy

class InfoBase():
    InfoStruct = None
    Tag        = None

    def __init__(self, stream, cp_index):
        self.instream      = stream
        self.data          = None
        self.constant_pool = None

        self.renamed       = False

        self.index         = cp_index

        if stream:
            self.read_stream()

    def read_stream(self):
        self.data = self.InfoStruct.parse_stream(self.instream)

    def write_stream(self, outstream):
        UBInt8("tag").build_stream(self.Tag, outstream)
        self.InfoStruct.build_stream(self.data, outstream)

    def link_cpool(self, constant_pool):
        self.constant_pool = constant_pool

    def get_class(self):
        return ''

    def set_class(self,name):
        pass

    def get_desc(self):
        return ''

    def set_desc(self, name):
        pass

    def get_name(self):
        return ''

    def set_name(self, name):
        pass

    def get_nameindex(self):
        try:
            return self.data.NameIndex
        except:
            return -1
            
    def set_nameindex(self, index):
        try:
            #We check if it exist
            a = self.data.NameIndex
            self.data.NameIndex = index
        except:
            pass
        

class RefBase(InfoBase):
    def get_class(self):
        return self.constant_pool[self.data.ClassIndex - 1].get_name()

    def set_class(self,name):
        self.constant_pool[self.data.ClassIndex - 1].set_name(name)

    def get_desc(self):
        return self.constant_pool[self.data.NameTypeIndex - 1].get_desc()

    def set_desc(self, name):
        self.constant_pool[self.data.NameTypeIndex - 1].set_desc(name)

    def get_name(self):
        return self.constant_pool[self.data.NameTypeIndex - 1].get_name()

    def set_name(self, name):
        self.constant_pool[self.data.NameTypeIndex - 1].set_name(name)

    def get_nameindex(self):
        return self.constant_pool[self.data.NameTypeIndex -1].data.NameIndex

    def set_nameindex(self, index):
        self.constant_pool[self.data.NameTypeIndex -1].data.NameIndex = index

class NameIndexBase(InfoBase):
    def get_name(self):
        return self.constant_pool[self.data.NameIndex - 1].get_name()

    def set_name(self, name):
        self.constant_pool[self.data.NameIndex - 1].set_name(name)

class InfoFieldRef(RefBase):
    InfoStruct = Struct("FieldRefInfo",  UBInt16("ClassIndex"), UBInt16("NameTypeIndex"))
    Tag        = 9
    TypePrim   = "Ref"
    TypeSec    = "Field"

class InfoMethodRef(RefBase):
    InfoStruct = Struct("MethodRefInfo", UBInt16("ClassIndex"), UBInt16("NameTypeIndex"))
    Tag        = 10
    TypePrim   = "Ref"
    TypeSec    = "Method"

class InfoInterRef(RefBase):
    InfoStruct = Struct("InterfRefInfo", UBInt16("ClassIndex"), UBInt16("NameTypeIndex"))
    Tag        = 11
    TypePrim   = "Ref"
    TypeSec    = "Interface"

class InfoClass(NameIndexBase):
    InfoStruct = Struct("ClassInfo",     UBInt16("NameIndex"))
    Tag        = 7
    TypePrim   = "Class"
    TypeSec    = None

class InfoString(NameIndexBase):
    InfoStruct = Struct("StringInfo",    UBInt16("NameIndex"))
    Tag        = 8
    TypePrim   = "String"
    TypeSec    = None

class InfoInt(InfoBase):
    InfoStruct = Struct("IntInfo",       UBInt32("Bytes"))
    Tag        = 3
    TypePrim   = "Int"
    TypeSec    = None

class InfoFloat(InfoBase):
    InfoStruct = Struct("FloatInfo",     UBInt32("Bytes"))
    Tag        = 4
    TypePrim   = "Float"
    TypeSec    = None

class InfoLong(InfoBase):
    InfoStruct = Struct("LongInfo",      UBInt32("HighBytes"), UBInt32("LowBytes"))
    Tag        = 5
    TypePrim   = "Long"
    TypeSec    = None

class InfoDouble(InfoBase):
    InfoStruct = Struct("DoubleInfo",    UBInt32("HighBytes"), UBInt32("LowBytes"))
    Tag        = 6
    TypePrim   = "Double"
    TypeSec    = None

class InfoNameType(InfoBase):
    InfoStruct = Struct("NameTypeInfo",  UBInt16("NameIndex"), UBInt16("DescIndex"))
    Tag        = 12
    TypePrim   = "NameType"
    TypeSec    = None

    def get_name(self):
        return self.constant_pool[self.data.NameIndex - 1].get_name()

    def set_name(self, name):
        self.constant_pool[self.data.NameIndex - 1].set_name(name)

    def get_desc(self):
        return self.constant_pool[self.data.DescIndex - 1].get_name()

    def set_desc(self, name):
        self.constant_pool[self.data.DescIndex - 1].set_name(name)

class InfoUTF8(InfoBase):
    InfoStruct = Struct("Utf8Info",      PascalString("String", length_field = UBInt16("length"), encoding='utf8'))
    Tag        = 1
    TypePrim   = "UTF8"
    TypeSec    = None

    def __init__(self, stream, cp_index):
        InfoBase.__init__(self, stream, cp_index)
        self.newstring = self.data.String


    def get_desc(self):
        return self.data.String

    def set_desc(self, name):
        self.newstring = name

    def get_name(self):
        return self.data.String

    def set_name(self, name):
        self.newstring = name
        
    def apply_changes(self):
        self.data.String = self.newstring

class InfoDummy(InfoBase):
    InfoStruct = None
    Tag        = None
    TypePrim   = "Dummy"
    TypeSec    = None

    def read_stream(self):
        pass

    def write_stream(self, streamout):
        pass



InfoType = {7  : InfoClass,
            9  : InfoFieldRef,
            10 : InfoMethodRef,
            11 : InfoInterRef,
            8  : InfoString,
            3  : InfoInt,
            4  : InfoFloat,
            5  : InfoLong,
            6  : InfoDouble,
            12 : InfoNameType,
            1  : InfoUTF8}
