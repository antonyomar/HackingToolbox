import argparse
import PyPDF2
import re
import sys
import os
import exifread
import sqlite3

from searcher import Searcher
from utils import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--regex', dest='regex', required=False, help='Regex searching')
    parser.add_argument('-m', '--meta', dest='meta', required=False, help='PDF Metadata searching')
    parser.add_argument('-s', '--string', dest='hidden_meta', required=False, help='PDF Hidden metadata')
    parser.add_argument('-e', '--exif', dest='exif', help='IMAGE metadata searching')
    parser.add_argument('-v', '--visited', dest='visited', help='Browser history (Firefox)')
    parser.add_argument('-c', '--cookie', dest='cookie', help='Browser cookie (Firefox)')
    args = parser.parse_args()

    if args.regex:
        Searcher.search_string(args.regex)
    elif args.meta:
        Searcher.search_meta(args.meta)
    elif args.exif:
        Searcher.search_exif(args.exif)
    elif args.visited:
        Searcher.search_history(args.visited)
    elif args.cookie:
        Searcher.search_cookie(args.cookie)
    elif args.hidden_meta:
        Searcher.search_string(args.hidden_meta)
