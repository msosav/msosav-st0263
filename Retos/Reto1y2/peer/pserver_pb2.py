# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pserver.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rpserver.proto\"\x19\n\x04\x46ile\x12\x11\n\tfile_name\x18\x01 \x01(\t\".\n\x08UserData\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1c\n\x08Username\x12\x10\n\x08username\x18\x01 \x01(\t\"\x1f\n\x08Response\x12\x13\n\x0bstatus_code\x18\x01 \x01(\x05\x32\xda\x01\n\x07PServer\x12\x1d\n\x05Login\x12\t.UserData\x1a\t.Response\x12\x1e\n\x06Logout\x12\t.Username\x1a\t.Response\x12\'\n\x13\x44ownloadFileRequest\x12\x05.File\x1a\t.Response\x12 \n\x0c\x44ownloadFile\x12\x05.File\x1a\t.Response\x12%\n\x11UploadFileRequest\x12\x05.File\x1a\t.Response\x12\x1e\n\nUploadFile\x12\x05.File\x1a\t.Responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pserver_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FILE']._serialized_start=17
  _globals['_FILE']._serialized_end=42
  _globals['_USERDATA']._serialized_start=44
  _globals['_USERDATA']._serialized_end=90
  _globals['_USERNAME']._serialized_start=92
  _globals['_USERNAME']._serialized_end=120
  _globals['_RESPONSE']._serialized_start=122
  _globals['_RESPONSE']._serialized_end=153
  _globals['_PSERVER']._serialized_start=156
  _globals['_PSERVER']._serialized_end=374
# @@protoc_insertion_point(module_scope)
