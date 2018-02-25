import os
import re
import time
import collections
from selenium import webdriver
from PyPDF2 import PdfFileMerger, PdfFileReader

# Global VARS
folder_number = 2
download_dir = "/home/maxlero/PycharmProjects/BookScraper/Book"


def init_browser():
    global folder_number
    global download_dir

    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs', {
        "plugins.plugins_list": [{"enabled": False,
                                  "name": "Chrome PDF Viewer"}],
        "download": {
            "prompt_for_download": False,
            "default_directory": download_dir + "/" + str(folder_number) + "/"
        }
    })

    browser = webdriver.Chrome(executable_path='/home/maxlero/PycharmProjects/Library/chromedriver',
                               chrome_options=options)

    browser.set_script_timeout(2)
    browser.set_page_load_timeout(2)

    return browser


def change_first_file_name():
    for x in os.listdir(download_dir):
        for y in os.listdir(download_dir + "/" + x):
            if y == "mb4x.pdf":
                os.rename(download_dir + "/" + x + "/" + y, download_dir + "/" + x + "/" + "mb4x (0).pdf")
                break


def download_book(ISBN, start_chapter=0, start_page=2, chapter_amount=500, pages_amount=2000):
    global folder_number

    book = ISBN
    chapter_amount = chapter_amount
    pages_amount = pages_amount

    # starting values
    chapter = start_chapter
    page = start_page

    # counts 101 pages
    counter = 0

    # TODO stop counter
    # stop_counter = chapter_amount

    browser = init_browser()

    for chapter_x in range(0, chapter_amount + 1):
        for page_x in range(0, pages_amount + 1):

            if counter > 100:
                browser.close()

                counter = 0
                folder_number += 1
                browser = init_browser()
                # break

            url = 'http://www.studentlibrary.ru/cgi-bin/mb4x?usr_data=gd-image(doc,' + str(
                book) + '-SCN' + str("%.4d" % chapter) + ',' + str(
                "%.4d" % page) + '.pdf,-1,,00000000,070133ed01224f569aca537maxlero)&hide_Cookie=yes'

            try:
                browser.get(url)
                print("getting " + "%.4d" % chapter + " " + "%.4d" % page)
                time.sleep(2)
                page += 1
                counter += 1
            except:
                # stop_counter -= 1
                print("NEXT chapter " + "%.4d" % chapter + " " + "%.4d" % page)
                chapter += 1

            # if not stop_counter:
            #     break

    time.sleep(5)
    browser.close()


def main():
    global download_dir

    download_book('ISBN9785444422625', 0, 2)
    folder = 'Book'

    change_first_file_name()

    for x in os.listdir(download_dir):
        # folder is empty?
        if not os.listdir(download_dir + "/" + x):
            continue

        # pdf files to merge
        files = []
        for y in os.listdir(download_dir + "/" + x):
            files.append(y)
        print(files)

        # sort
        array = {}
        for fname in files:
            text = re.sub(r"([a-z0-9 ]*\()", "", fname)
            text = re.sub(r"([a-z ).]*)", "", text)
            array.update({"%.3d" % int(text): fname})
        od = collections.OrderedDict(sorted(array.items()))

        # merge
        merger = PdfFileMerger()
        for i, j in enumerate(od):
            # print(od[y])
            merger.append(PdfFileReader(open(os.path.join(folder + "/" + x, od[j]), 'rb')))

        merger.write(download_dir + "/" + x + ".pdf")
        print("Folder " + x + " done")

    # Final concatenation
    all_files = [f for f in os.listdir(download_dir + "/")]
    files = []
    for x in all_files:
        if x.endswith(('.pdf', '.PDF')):
            files.append(x)
    print(files)

    # sort
    array = {}
    for fname in files:
        text = re.sub(r"([a-z0-9 ]*\()", "", fname)
        text = re.sub(r"([a-z ).]*)", "", text)
        array.update({"%.3d" % int(text): fname})

    od = collections.OrderedDict(sorted(array.items()))

    # merge
    merger = PdfFileMerger()
    for i, j in enumerate(od):
        merger.append(PdfFileReader(open(os.path.join(folder, od[j]), 'rb')))

    merger.write(download_dir + "/book.pdf")


if __name__ == "__main__":
    main()
