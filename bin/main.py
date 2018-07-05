#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')))

from check_workspace import helper

from optparse import OptionParser

usage = "%prog options arguments"
version="%prog 1.0"
parser = OptionParser(usage=usage, description="check yields and shape for WS", version=version)

(options,args) = parser.parse_args()
option_dir = {
    "limitToTable":helper.tabulize_limit,
    "combYields": helper.get_total_yields,
}
if len(args) < 1:
    parser.print_help()
    print option_dir.keys()
    exit(1)

if args[0] not in option_dir.keys():
    print option_dir.keys
    exit(1)
else:
    exe = option_dir[args[0]]
    exe(args[1])
