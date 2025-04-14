# -*- coding: utf-8 -*-

import os
import json
import ctypes
import idakeygen

license = idakeygen.license["payload"]["licenses"][0]

obj = {
    "licsrc": {"path": os.path.join(os.getcwd(), "idapro.hexlic")},
    "lid": license["id"],
}
obj_str = json.dumps(obj, sort_keys=True, separators=(",", ":"))

lib_ida = ctypes.CDLL("./libida.so")

class QCharVector(ctypes.Structure):
    _fields_ = [
        ("array", ctypes.c_char_p),
        ("n", ctypes.c_size_t),
        ("alloc", ctypes.c_size_t),
    ]

class QString(ctypes.Structure):
    _fields_ = [
        ("body", QCharVector),
    ]

class QStringVector(ctypes.Structure):
    _fields_ = [
        ("array", ctypes.POINTER(QString)),
        ("n", ctypes.c_size_t),
        ("alloc", ctypes.c_size_t),
    ]

# void reg_write_strlist(const qstrvec_t &in, const char *subkey);
reg_write_strlist = lib_ida.reg_write_strlist
reg_write_strlist.restype = None
reg_write_strlist.argtypes = [ctypes.POINTER(QStringVector), ctypes.c_char_p]

# int reg_int_op(const char *name, bool save, int value, const char *subkey);
reg_int_op = lib_ida.reg_int_op
reg_int_op.restype = ctypes.c_int
reg_int_op.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_int, ctypes.c_char_p]

str_obj = QString()
str_obj.body.array = obj_str.encode()
str_obj.body.n = len(obj_str) + 1
str_obj.body.alloc = len(obj_str) + 1

vec_obj = QStringVector()
vec_obj.array = ctypes.pointer(str_obj)
vec_obj.n = 1
vec_obj.alloc = 1

lib_ida.reg_write_strlist(ctypes.pointer(vec_obj), f"Licenses\\{license['product_id']}.{license['edition_id']}".encode())

reg_int_op(b"Use90ShortcutSet", True, 1, None)
reg_int_op(b"EULA 90", True, 1, None)
reg_int_op(b"LicensePrevWarnTime", True, 0, None)
reg_int_op(b"AutoCheckUpdates", True, 0, None)
reg_int_op(b"AutoUseLumina", True, 0, None)
reg_int_op(b"InformedAboutUpdates3", True, 1, None)
reg_int_op(b"The decompiler assumes that the segment   s  is read only because of its  s  All data references to ", True, 1, b"Hidden Messages")
