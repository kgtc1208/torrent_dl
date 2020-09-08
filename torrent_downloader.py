from selenium.webdriver import ChromeOptions, Chrome
import time
import os
import imapclient
import pyzmail
import getpass


def run_torrent(download_dir):
    os.chdir(download_dir)
    files = [os.path.join(download_dir, filename) for filename in os.listdir('.')]
    latest_file = sorted(files, key=os.path.getctime)[-1]
    os.startfile(latest_file)


def connect_and_download(src_url, download_dir):
    opts = ChromeOptions()
    prefs = {'download.default_directory': fr'{download_dir}'}
    opts.add_experimental_option("prefs", prefs)
    driver = Chrome("C:/Users/hp-user/PycharmProjects/chromedriver.exe", options=opts)
    driver.get(src_url)
    parent_element = driver.find_element_by_class_name("item-download-options")
    lnk = parent_element.find_element_by_partial_link_text("TORRENT")
    time.sleep(5)
    lnk.click()
    time.sleep(10)
    run_torrent(download_dir)
    driver.close()


def read_email():
    download_dir = input("Enter download directory: ")
    imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    while True:
        try:
            em = input("Enter email: ")
            pw = getpass.getpass(prompt="Password: ")
            imapObj.login(em, pw)
        except:
            print("Password or Username incorrect\n")
            pass
        else:
            print("Login Successful\n")
            break
    latest_email = None
    while True:
        imapObj.select_folder("INBOX", readonly=True)
        UIDs = imapObj.gmail_search("archive.org")
        rawMessage = imapObj.fetch(UIDs, ["BODY[]"])

        if UIDs:
            message = pyzmail.PyzMessage.factory(rawMessage[UIDs[-1]][b"BODY[]"])
            if UIDs[-1] == latest_email:
                time.sleep(120)
                print("New torrent is same as the last one")
            else:
                print("Downloading new torrent")
                latest_email = UIDs[-1]
                src_url = message.text_part.get_payload().decode(message.text_part.charset).split()[0]
                connect_and_download(src_url, download_dir)
                time.sleep(120)
        else:
            print("No new torrents")
            time.sleep(120)


read_email()
