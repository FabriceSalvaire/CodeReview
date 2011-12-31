#! /usr/bin/env python
# -*- Mode: Python -*-

#####################################################################################################

import argparse
import sys

#####################################################################################################

from Diff import FileDiffBuffer, Diff2Way

#####################################################################################################

parser = argparse.ArgumentParser(description='Patience Diff.')

parser.add_argument('file_a', metavar='File_a',
                    help='')
parser.add_argument('file_b', metavar='File_b',
                    help='')

parser.add_argument('--patience', dest='matcher',
                    action='store_const', const='patience', default='patience',
                    help="Use the patience difference algorithm")
parser.add_argument('--difflib', dest='matcher',
                    action='store_const', const='difflib', default='patience',
                    help="Use python\'s difflib algorithm")

args = parser.parse_args()

#####################################################################################################

file_a = open(args.file_a, 'rb').readlines()
file_b = open(args.file_b, 'rb').readlines()

diff_file_a = FileDiffBuffer(file_a, 'A')
diff_file_b = FileDiffBuffer(file_b, 'B')

diff2way = Diff2Way(diff_file_a, diff_file_b)

print diff2way.hunks

#####################################################################################################
#
# End
#
#####################################################################################################
