# !usr/bin/env python3
# coding : utf-8

import argparse
from cracker import *
import multiprocessing
import atexit
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MD5 CRACKING')
    parser.add_argument('-m', '--md5', dest='hash', required=False, help='MD5 hash file path')
    parser.add_argument('-d', '--dico', dest="dico", required=False, help="Dictionary file path")
    parser.add_argument('-l', '--length', dest='length', required=False, help='Brute force cracking', type=int)
    parser.add_argument('-g', '--gen', dest='gen', required=False, help='Generate MD5 password')
    parser.add_argument('-n', '--net', dest='net', required=False, help='Online cracking')
    parser.add_argument('--proc', dest='proc', help='Multiprocessing cracking')
    parser.add_argument('--pattern', dest='pattern', required=False, help='Pattern cracking')
    parser.add_argument('-f', '--file', dest='file', required=False, help='Apply operation to the file')
    parser.add_argument('-p', '--protect', dest='protect', required=False, help='Protect pdf with password')
    parser.add_argument('-c', '--clearprotect', dest='clearprotect', required=False, help='Decrypt pdf with password')
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

        attempt = 0
        # while True:
        #     cracking = done_queue.get()
        #     if cracking == 'Successful':
        #         ps1.kill()
        #         ps2.kill()
        #         break
        #     elif cracking == 'Failed':
        #         attempt += 1
        #         if attempt == len(processes):
        #             print('Multiprocessing failed!!!')
        #             break

    work_queue = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()

    if args.dico and not args.length:
        if args.proc:
            pcrack_dict(args.hash, args.dico)
        else:
            Cracker.crack_dict(args.hash, args.dico, False)
    elif args.length and not args.dico:
        Cracker.crack_brute(args.hash, args.length)
    elif args.gen:
        Cracker.gen_md5(args.gen)
    elif args.net:
        Cracker.crack_online(args.net)
    elif args.pattern:
        Cracker.crack_pattern(args.hash, args.pattern)
    elif args.protect:
        Cracker.protect_file(args.protect)
    elif args.clearprotect:
        Cracker.decrypt_file(args.clearprotect)
