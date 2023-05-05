import hashlib
import sys
import time
import string
import urllib.request, urllib.response, urllib.error
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
                    print(Color.GREEN + "PASSWORD FOUND : " + mdp.decode('utf-8') + '\r (' + mdpmd5 + ')' + Color.END)
                    success = True
            if not success:
                print(Color.RED + 'PASSWORD NOT FOUND :(' + Color.END)

        except FileNotFoundError:
            print('Error: File not found!')

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
                    currentmd5 = hashlib.md5(("".join(currentpass)+'\n').encode('utf8')).hexdigest()
                    print(currentmd5)
                    print('Cracking password: ' + "".join(currentpass))
                    if hashmd5 == currentmd5:
                        print(Color.GREEN + "PASSWORD FOUND : " + "".join(
                            currentpass) + ' (' + hashmd5 + ')' + Color.END)
                        sys.exit(1)
                    else:
                        Cracker.crack_brute(md5, length - 1, currentpass)

    @staticmethod
    def crack_online(md5):
        try:
            useragent = "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
            headers = {'USER-AGENT': useragent}
            url = 'https://www.google.com/search?hl=fr&q=' + md5
            request = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(request).read()
            if 'not found' not in str(response):
                print('RESULT FOUND AT ' + url)

        except urllib.error.HTTPError as e:
            print(Color.RED + 'HTTP ERROR : ' + str(e.code) + Color.END)
        except urllib.error.URLError as e:
            print(Color.RED + 'URL ERROR : ' + str(e.reason) + Color.END)

    @staticmethod
    def gen_md5(path):

        file = open(path, 'rb')
        buf = file.read(BLOCKSIZE)
        hasher = hashlib.md5()

        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
        hashmd5 = open('hashmd5.txt', 'w')
        hashmd5.write(hasher.hexdigest())
        hashmd5.close()
        print("GENERATED HASH: " + hasher.hexdigest())
        print("Saved at : hashmd5.txt")
        sys.exit(0)

    @staticmethod
    def crack_pattern(md5, pattern, index=0):
        maj = string.ascii_uppercase
        min = string.ascii_lowercase
        num = string.digits

        hashmd5 = Cracker.open_hash(md5)
        if index < len(pattern):
            if pattern[index] in maj + min + num:
                Cracker.crack_pattern(md5, pattern, index + 1)
            else:
                if pattern[index] == '+':
                    for letter in maj:
                        currpass = pattern.replace('+', letter, 1)
                        if hashmd5 == hashlib.md5(currpass.encode('utf8')).hexdigest():
                            print(Color.GREEN + 'PASSWORD FOUND :) ' + currpass + ' (' + hashmd5 + ')' + Color.END)
                            sys.exit(0)
                        Cracker.crack_pattern(md5, currpass, index + 1)
                if pattern[index] == '#':
                    for letter in min:
                        currpass = pattern.replace('#', letter, 1)
                        if hashmd5 == hashlib.md5(currpass.encode('utf8')).hexdigest():
                            print(Color.GREEN + 'PASSWORD FOUND :) ' + currpass + ' (' + hashmd5 + ')' + Color.END)
                            sys.exit(0)
                        Cracker.crack_pattern(md5, currpass, index + 1)
                if pattern[index] == '$':
                    for letter in num:
                        currpass = pattern.replace('$', letter, 1)
                        if hashmd5 == hashlib.md5(currpass.encode('utf8')).hexdigest():
                            print(Color.GREEN + 'PASSWORD FOUND :) ' + currpass + ' (' + hashmd5 + ')' + Color.END)
                            sys.exit(0)
                        Cracker.crack_pattern(md5, currpass, index + 1)

    @staticmethod
    def protect_file(path):
        file = open(path, 'rb')
        pdfWriter = PyPDF2.PdfFileWriter()

        pdfReader = PyPDF2.PdfFileReader(path)
        for page_num in range(pdfReader.numPages):
            pdfWriter.addPage(pdfReader.getPage(page_num))
        passwd = getpass.getpass(prompt='Enter password: ')
        pdfWriter.encrypt(passwd)
        with open(path, 'wb') as pdf:
            pdfWriter.write(pdf)
        print(Color.GREEN + 'File encrypted at: ' + path)

    def decrypt_file(path):
        file = open(path, 'rb')
        pdfWriter = PyPDF2.PdfFileWriter()
        pdfReader = PyPDF2.PdfFileReader(path)
        if pdfReader.isEncrypted:
            passwd = 'https://t.me/LiensUtiles'
            pdfReader.decrypt(passwd)

            for page_num in range(pdfReader.numPages):
                pdfWriter.addPage(pdfReader.getPage(page_num))
            [filename, ext] = path.split('.')
            with open(filename + '_decrypted.' + ext, 'wb') as new_file:
                pdfWriter.write(new_file)
            print('File successfully decrypted at: ' + path)
        else:
            print('File already decrypted!')
