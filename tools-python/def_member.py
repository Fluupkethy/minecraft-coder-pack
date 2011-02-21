from   construct import *
import StringIO

class BaseDef():
    def __init__(self, stream, cpool, index):
        self.instream      = stream
        self.data          = None
        self.constant_pool = cpool
        self.attributes    = None
        self.index         = index

        self.read_stream()

    def read_stream(self):
        self.data = self.InfoStruct.parse_stream(self.instream)
        self.attributes = []
        for iattrb in range(self.data.AttributesCount):
            self.attributes.append(AttribDef(self.instream, self.constant_pool, -1))

    def write_stream(self, outstream):
        self.InfoStruct.build_stream(self.data, outstream)
        for attrb in self.attributes:
            attrb.InfoStruct.build_stream(attrb.data, outstream)

    def link_cpool(self, constant_pool):
        self.constant_pool = constant_pool

    def get_desc(self):
        return self.constant_pool[self.data.DescriptorIndex - 1].get_name()

    def set_desc(self, name):
        self.constant_pool[self.data.DescriptorIndex - 1].set_name(name)

    def get_name(self):
        return self.constant_pool[self.data.NameIndex - 1].get_name()

    def set_name(self, name):
        self.constant_pool[self.data.NameIndex - 1].set_name(name)

    def get_nameindex(self):
        return self.data.NameIndex

class MethodDef(BaseDef):
    InfoStruct = Struct("MethodInfo",    UBInt16("AccessFlags"), UBInt16("NameIndex"), UBInt16("DescriptorIndex"), UBInt16("AttributesCount"))
    
class FieldDef (BaseDef):
    InfoStruct = Struct("FieldInfo",     UBInt16("AccessFlags"), UBInt16("NameIndex"), UBInt16("DescriptorIndex"), UBInt16("AttributesCount"))
    
class AttribDef(BaseDef):
    InfoStruct = Struct("AttributeInfo", UBInt16("NameIndex"),   UBInt32("AttributLength"),  MetaField("Info", lambda ctx: ctx["AttributLength"]))

    def read_stream(self):
        self.data = self.InfoStruct.parse_stream(self.instream)

    def write_stream(self, outstream):
        self.InfoStruct.build_stream(self.data, outstream)

    def get_desc(self):
        return ''

    def set_desc(self, name):
        pass
