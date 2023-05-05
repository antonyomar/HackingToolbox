import time
import PyPDF2
import exifread
import re
import os
import sys
import sqlite3
from utils import Color

class Searcher:
    def __init__(self):
        self._start = time.time()

    @staticmethod
    def search_meta(pdf_path):
        pdf_file = PyPDF2.PdfFileReader(pdf_path, 'rb')
        pdf_meta = pdf_file.getDocumentInfo()

        print('METADATA PDF: ')
        for meta in pdf_meta:
            print(meta + ': ' + pdf_meta[meta])

    @staticmethod
    def search_exif(img_path):
        with open(img_path, 'rb') as image:
            exif = exifread.process_file(image)

        if not exif:
            print('[-] Metadata EXIF don\'t exist')
        else:
            print("METADATA EXIF:")
            for tag in exif.keys():
                print(tag + ' : ' + str(exif[tag]))

    def _convert_to_degress(value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)

        return d + (m / 60.0) + (s / 3600.0)

    @staticmethod
    def search_gps(self, img_path):
        with open(img_path, 'rb') as image:
            exif = exifread.process_file(image)
            if not exif:
                print("[-] Metadata EXIF don't exist!")
            else:
                latitude = exif.get('GPS GPSLatitude')
                longitude = exif.get('GPS GPSLongitude')
                latitude_ref = exif.get('GPS GPSLatitudeRef')
                longitude_ref = exif.get('GPS GPSLongitudeRef')

                if latitude and longitude and latitude_ref and longitude_ref:
                    lat = self._convert_to_degress(latitude)
                    long = self._convert_to_degress(longitude)
                    if str(latitude_ref) != 'N':
                        lat = 0 - lat
                    if str(longitude_ref) != 'E':
                        long = 0 - long
                        print("http://maps.google.com/maps?q=loc:%s,%s" % (str(lat), str(long)))

    def search_string(pdf_path):

        with open(pdf_path, 'rb') as file:
            content = file.read()

        # regex = re.compile("hello", re.IGNORECASE)
        regex = re.compile("(Title)[\S\s]+", re.I)
        print('RESULTS SEARCH:')
        for match in re.finditer(regex, content.decode('utf8', 'backslashreplace')):
            print(match.group())

    def search_history(places_sqlite):
        # ex for linux: /home/antonyomar/.mozilla/firefox/esr/.../places.sqlite
        # ex for windows: C:\\Users\Antonyomar\AppData\Roaming\Mozilla\Firefox\Profiles\...\places.sqlite
        try:
            conn = sqlite3.connect(places_sqlite)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT url, datetime(last_visit_date/1000000, \"unixepoch\"), title FROM moz_places")

            os.chdir('/home')
            filepath = os.getcwd() + '/history_log.html'

            # path = Path(path)
            # if path.is_file()

            if not os.path.exists(filepath):
                print('FIREFOX HISTORY: ')
                with open(filepath, 'a') as log:
                    header = '<!DOCTYPE html>' \
                             ' <head>' \
                             '  <title> Browser history </title>' \
                             '  <style> tr,th,td {border : solid 1px black} </style>' \
                             ' </head>' \
                             ' <body>' \
                             '  <table>' \
                             '   <tr><th> URL </th> <th> DATE </th></tr>'
                    log.write(header)

                    for row in cursor.fetchall():
                        url = row[0]
                        date = row[1]
                        title = row[2]
                        log.write('<tr><td>' + '<a href="' + str(url) + '">' + str(
                            title) + '</a>' + '</td><td>' + str(
                            date) + '</td></tr>')

                    footer = ' </table></body>'
                    log.write(footer)
                    print(Color.GREEN + '[+] Browse history search at ' + filepath + Color.END)

            else:
                os.remove(filepath)
                Searcher.search_history(places_sqlite)

        except Exception as e:
            print(Color.RED + 'ERROR :' + str(e) + Color.END)
            sys.exit(1)

    def search_cookie(cookies_sqlite):

        try:
            conn = sqlite3.connect(cookies_sqlite)
            cursor = conn.cursor()
            # Unknown table name case
            # cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            # cursor.execute("SELECT * FROM moz_cookies")
            # print(cursor.fetchone())
            # print(cursor.description)

            cursor.execute("SELECT name, value, host, path FROM moz_cookies")
            os.chdir('/home')
            filepath = os.getcwd() + '/cookie_log.html'

            if not os.path.exists(filepath):
                print('FIREFOX COOKIE: ')
                with open(filepath, 'a') as log:
                    header = '<!DOCTYPE html>' \
                             ' <head>' \
                             '  <title> Browser cookie </title>' \
                             '  <style> tr,th,td {border : solid 1px black} </style>' \
                             ' </head>' \
                             ' <body>' \
                             '  <table>' \
                             '   <tr><th> NAME </th> <th> VALUE </th> <th> HOST</th> <th> PATH </th> </tr>'
                    log.write(header)
                    for row in cursor.fetchall():
                        name = row[0]
                        value = row[1]
                        host = row[2]
                        path = row[3]
                        log.write(
                            '<tr><td>' + str(name) + '</td><td>' + str(value) + '</td><td>' + '<a href="' +
                            str(host) + '">' + str(host) + '</a>' + '</td><td>' + str(path) + '</td></tr>')

                    footer = ' </table></body>'
                    log.write(footer)

                    print(Color.GREEN + '[+] Browse cookie search at ' + filepath + Color.END)

            else:
                os.remove(filepath)
                Searcher.search_cookie(cookies_sqlite)
        except Exception as e:
            print(Color.RED + '[!] Error in searching cookies : ' + str(e) + Color.END)

