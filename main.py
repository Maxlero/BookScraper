import os
import re
import time
import collections
from selenium import webdriver
from PyPDF2 import PdfFileMerger, PdfFileReader


# 101 pages at once maximum
def download_book():
    download_dir = "/home/maxlero/PycharmProjects/Library/Book/"
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs', {
        "plugins.plugins_list": [{"enabled": False,
                                  "name": "Chrome PDF Viewer"}],
        "download": {
            "prompt_for_download": False,
            "default_directory": download_dir
        }
    })

    browser = webdriver.Chrome(executable_path='/home/maxlero/PycharmProjects/Library/chromedriver',
                               chrome_options=options)

    browser.set_script_timeout(2)
    browser.set_page_load_timeout(2)

    book = 'ISBN9789850628558'
    chapter_amount = 100
    pages_amount = 600

    # starting values
    chapter = 4
    page = 507

    # counts 101 pages
    counter = 0
    for chapter_x in range(0, chapter_amount + 1):
        for page_x in range(0, pages_amount + 1):

            if counter > 100:
                break

            url = 'http://www.studentlibrary.ru/cgi-bin/mb4x?usr_data=gd-image(doc,' + str(
                book) + '-SCN' + str("%.4d" % chapter) + ',' + str(
                "%.4d" % page) + '.pdf,-3,,00000000,080133ecfe2360ac05db537maxlero)&hide_Cookie=yes'

            try:
                browser.get(url)
                print("getting " + "%.4d" % chapter + " " + "%.4d" % page)
                time.sleep(2)
                page += 1
                counter += 1
            except:
                print("NEXT chapter " + "%.4d" % chapter + " " + "%.4d" % page)
                chapter += 1

    time.sleep(10)
    browser.close()


def main():
    folder = 'Book'
    book_dir = "/home/maxlero/PycharmProjects/Library/" + folder + "/"

    # pdf files to merge
    files = []
    for x in os.listdir(book_dir):
        files.append(x)

    # sort
    array = {}
    for fname in files:
        text = re.sub(r"([a-z0-9 ]*\()", "", fname)
        text = re.sub(r"([a-z ).]*)", "", text)
        array.update({"%.3d" % int(text): fname})
    od = collections.OrderedDict(sorted(array.items()))

    # merge
    merger = PdfFileMerger()
    for x, y in enumerate(od):
        # print(od[y])
        merger.append(PdfFileReader(open(os.path.join(folder, od[y]), 'rb')))

    merger.write("book.pdf")


if __name__ == "__main__":
    main()
