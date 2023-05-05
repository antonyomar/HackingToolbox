# !usr/bin/env python3
# coding : utf-8

import argparse
from cracker import *
import multiprocessing
import atexit
import re
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Md5 cracking tools')
    parser.add_argument('-m', '--md5', dest='hash_file', required=False, help='MD5 hash file pathman')
    parser.add_argument('-d', '--dico', dest="dict_file", required=False, help="Dictionary file path")
    parser.add_argument('-l', '--length', dest='length', required=False, help='Brute force cracking', type=int)
    parser.add_argument('-g', '--gen', dest='plaintext_file', required=False, help='Generate MD5 password')
    parser.add_argument('-n', '--net', dest='hash_string', required=False, help='Online cracking')
    parser.add_argument('--proc', dest='multi_proc', help='Multiprocessing cracking')
    parser.add_argument('--pattern', dest='pattern', required=False, help='Pattern cracking')
    parser.add_argument('-f', '--file', dest='file', required=False, help='Apply operation to the file')
    parser.add_argument('-p', '--protect', dest='pdf_file', required=False, help='Protect pdf with password')
    parser.add_argument('-c', '--clearprotect', dest='pdf_protected_file', required=False, help='Decrypt pdf with password')
    parser.add_argument('-a', '--all', dest="all_in_one", required=False, help="Launch all methods cracking")
    args = parser.parse_args()

    # os.chdir('/home/antony/Hack/Dico')
    # current = os.getcwd()
    # print('Current directory: ' + current)
    start = time.time()


    def display_time():
        sec = time.time() - start

        if sec < 60:
            sec = int(sec * 100) / 100
            print('Duration: ', str(sec), ' sec')
        else:
            min = sec / 60
            sec = sec % 60
            if min < 60:
                print("Duration: %s min %s sec" % (format(min), format(sec)))
            else:
                hour = min / 60
                min = min % 60
                print(f"Duration: {format(hour)} hour {format(min)} min {format(sec)} sec")


    def format(t):
        t = int(t + .5)
        if t < 10:
            t = '0' + str(t)
        return str(t)


    atexit.register(display_time)


    def pcrack_dict(md5, dico):
        """
        Parallelism cracking password
        :return:
        """
        # cracking descendant
        ps1 = multiprocessing.Process(target=Cracker.work_dict, args=(md5, dico, False))
        ps1.start()
        print("Processes 1 staring")
        # cracking ascendant
        ps2 = multiprocessing.Process(target=Cracker.work_dict, args=(md5, dico, True))
        ps2.start()
        print("Processes 2 starting")

    if args.all_in_one:
        Cracker.crack_allinone(args.hash_file, args.dict_file, args.pattern, args.length)
    elif args.dict_file and not args.length:
        if args.multi_proc:
            pcrack_dict(args.hash_file, args.dict_file)
        else:
            Cracker.crack_dict(args.hash_file, args.dict_file, False)
    elif args.length and not args.dict_file:
        Cracker.crack_brute(args.hash_file, args.length)
    elif args.plaintext_file:
        Cracker.gen_md5(args.plaintext_file)
    elif args.hash_string:
        Cracker.crack_online(args.hash_string)
    elif args.pattern:
        Cracker.crack_pattern(args.hash_file, args.pattern)
    elif args.pdf_file:
        Cracker.protect_file(args.pdf_file)
    elif args.pdf_protected_file:
        Cracker.decrypt_file(args.pdf_protected_file)

