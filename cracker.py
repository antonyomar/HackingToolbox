import hashlib
import sys
import os
import time
import string
import urllib.request, urllib.response, urllib.error

from PyPDF2.errors import PdfReadError

from utils import *
import getpass
import PyPDF2

BLOCKSIZE = 65535


class Cracker:

    def __init__(self):
        self._start = time.time()  # private variable

    @staticmethod
    def work_dict(md5, dico, order):
        Cracker.crack_dict(md5, dico, order)

    @staticmethod
    def open_hash(md5):
        hash = open(md5, 'r')
        hashMd5 = hash.readlines()
        return hashMd5[0].strip('\n')

    @staticmethod
    def crack_dict(md5, dico, order):
        """
        :param order: cracking order
        :param md5: hash file path
        :param dico: dictionary file path
        :return: cracking result
        """
        success = False
        print('DICTIONARY CRACKING: ')
        try:
            dict = open(dico, 'rb')
            hashmd5 = Cracker.open_hash(md5)

            if Order.ASC == order:
                wordlist = reversed(list(dict.readlines()))
            else:
                wordlist = dict.readlines()
            for mdp in wordlist:
                # mdp = mdp.strip('\n').decode('utf-8')
                mdpmd5 = hashlib.md5(mdp).hexdigest()

                if hashmd5 == mdpmd5:
                    print(Color.GREEN + "[+] Password found : " + mdp.decode('utf-8') + '\r (' + mdpmd5 + ')' + Color.END)
                    success = True
                    sys.exit(0)

            if not success:
                print('[-] Password not found :(')


        except FileNotFoundError:
            print(Color.RED + '[!] Error: File not found!' + Color.END)

    @staticmethod
    def crack_brute(md5, length, currentpass=[]):
        """
        :param md5: hash file path
        :param length: password length
        :param currentpass: incremented password
        :return:
        """
        # caracts = string.printable
        # caracts = string.ascii_letters
        caracts = string.digits
        hashmd5 = Cracker.open_hash(md5)

        if length >= 1:
            if len(currentpass) == 0:
                current = ['a' for _ in range(length)]
                Cracker.crack_brute(md5, length, current)
            else:
                for c in caracts:
                    currentpass[length - 1] = c
                    currentmd5 = hashlib.md5(("".join(currentpass) + '\n').encode('utf8')).hexdigest()

                    print('BRUTE FORCE CRACKING: ')
                    print('Cracking password: ' + "".join(currentpass))
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    if hashmd5 == currentmd5:
                        print('BRUTE FORCE CRACKING: ')
                        print(Color.GREEN + "[+] Password found: " + "".join(
                            currentpass) + ' (' + hashmd5 + ')' + Color.END)
                        sys.exit(0)

                    else:
                        Cracker.crack_brute(md5, length - 1, currentpass)


    @staticmethod
    def crack_online(hashmd5):
        print('ONLINE CRACKING: ')
        try:
            useragent = "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
            headers = {"USER-AGENT": useragent}
            url = 'https://www.google.com/search?hl=fr&q=' + hashmd5
            request = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(request).read()
            if ('not found' and 'Aucun document ne correspond aux termes de recherche') not in str(response):
                print(Color.GREEN + '[+] Result found at: ' + url + Color.END)
                sys.exit(0)
            else:
                print('[-] Result not found :(')

        except urllib.error.HTTPError as e:
            print(Color.RED + '[!] HTTP ERROR : ' + str(e.code) + Color.END)
        except urllib.error.URLError as e:
            print(Color.RED + '[!] URL ERROR : ' + str(e.reason) + Color.END)

    @staticmethod
    def gen_md5(path):

        file = open(path, 'rb')
        buf = file.read(BLOCKSIZE)
        hasher = hashlib.md5()

        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
        hashmd5 = open('res/hashmd5.txt', 'w')
        hashmd5.write(hasher.hexdigest())
        hashmd5.close()
        print("[+] Generated hash: " + hasher.hexdigest())
        print("Saved at : hashmd5.txt")
        sys.exit(0)

    @staticmethod
    def crack_pattern(md5, pattern, index=0):
        maj = string.ascii_uppercase
        min = string.ascii_lowercase
        num = string.digits

        hashmd5 = Cracker.open_hash(md5)
        currpass = pattern

        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('PATTERN CRACKING: ')
        print('Cracking password: ' + currpass)
        if index < len(pattern):
            if pattern[index] == '+':
                for letter in maj:
                    currpass = pattern.replace('+', letter, 1)
                    if hashmd5 == hashlib.md5(currpass.join('\n').encode('utf8')).hexdigest():
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                        print('PATTERN CRACKING: ')
                        print(Color.GREEN + '[+] Password found : ' + currpass + ' (' + hashmd5 + ')' + Color.END)
                        sys.exit(0)
                    Cracker.crack_pattern(md5, currpass, index + 1)
            if pattern[index] == '#':
                for letter in min:
                    currpass = pattern.replace('#', letter, 1)
                    if hashmd5 == hashlib.md5(currpass.join('\n').encode('utf8')).hexdigest():
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                        print('PATTERN CRACKING: ')
                        print(Color.GREEN + '[+] Password found : ' + currpass + ' (' + hashmd5 + ')' + Color.END)
                        sys.exit(0)
                    Cracker.crack_pattern(md5, currpass, index + 1)
            if pattern[index] == '@':
                for letter in num:
                    currpass = pattern.replace('@', letter, 1)
                    if hashmd5 == hashlib.md5((currpass + '\n').encode('utf8')).hexdigest():
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                        print('PATTERN CRACKING: ')
                        print(Color.GREEN + '[+] Password found : ' + currpass + ' (' + hashmd5 + ')' + Color.END)
                        sys.exit(0)

                    Cracker.crack_pattern(md5, currpass, index + 1)


    @staticmethod
    def crack_allinone(md5, dico, pattern, length):
        hashmd5 = Cracker.open_hash(md5)
        Cracker.crack_dict(md5, dico, False)
        Cracker.crack_pattern(md5, pattern)
        Cracker.crack_brute(md5, length)
        Cracker.crack_online(hashmd5)

    @staticmethod
    def protect_file(path):
        print('PDF ENCRYPTION:')
        file = open(path, 'rb')
        pdfWriter = PyPDF2.PdfFileWriter()
        pdfReader = PyPDF2.PdfFileReader(path)
        try:
            for page_num in range(pdfReader.numPages):
                pdfWriter.addPage(pdfReader.getPage(page_num))

        except PdfReadError as e:
            print('[-] Sorry, document seems to be already encrypted!')
            sys.exit(1)
        passwd = getpass.getpass(prompt='Enter password: ')
        pdfWriter.encrypt(passwd)
        filename = path.split('.')[0]
        cpath = filename + "_crypted.pdf"

        with open(cpath, 'wb') as pdf:
            pdfWriter.write(pdf)
        print('[+] File successfully encrypted at: ' + cpath)

    def decrypt_file(path):
        print('PDF DECRYPTION:')
        file = open(path, 'rb')
        pdfWriter = PyPDF2.PdfFileWriter()
        pdfReader = PyPDF2.PdfFileReader(path)
        if pdfReader.isEncrypted:
            passwd = getpass.getpass(prompt="Enter password: ")

            pdfReader.decrypt(passwd)

            try:
                for page_num in range(pdfReader.numPages):
                    pdfWriter.addPage(pdfReader.getPage(page_num))
                [filename, ext] = path.split('.')
                dpath = filename + '_decrypted.' + ext
                with open(dpath, 'wb') as new_file:
                    pdfWriter.write(new_file)
                print(Color.GREEN + '[+] File successfully decrypted at: ' + dpath + Color.END)

            except PdfReadError as e:
                print('[-] Password error, please try again...')
                sys.exit(1)
        else:
            print('[-] File already decrypted!')
