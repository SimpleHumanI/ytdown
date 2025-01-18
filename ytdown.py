#! /bin/python3
"""
    this program uses y2down.cc api for handle
    youtube links 
"""

from tqdm import tqdm
from requests import get
from re import match
from argparse import ArgumentParser
from os import rename
from re import compile

from litdm import litdm

global urls
urls = list()

class handle_args():
    def __init__(self):
        self.parse = ArgumentParser(description="download single/multiple media from youtube")
        self.parse.add_argument("url", nargs="?")
        self.parse.add_argument("-f", "--file", help="file with multiple url separated with newline")
        self.parse.add_argument("-F", "--format", help="mp4 qualities and other formats: (360,480,720,1080), mp3, m4a, webm, wav, ogg, flac, opus")
        self.parse.add_argument("-n", "--filename", help="specific file name except youtube video title")

        self.argv, self.argv_unknown = self.parse.parse_known_args()

    def no_arg_passed(self):
        values = vars(self.argv).values()
        no_arg = True
        for value in values:
            if value != None:
                no_arg = False
        return no_arg
    
    def help_page(self):
        self.parse.print_help()
        exit (1)

class ytdown:
    def __init__(self, url, _type, file_format:str='', file_name:str=''):
        self.filename = file_name 
        self.fileformat = "360" 

        if _type == "url":
            self.single_url(url, file_format)
        if _type == "filename":
            if len(urls) != 0 :
                self.write_single_file(url, file_format)
        elif _type == "file":
            file_content = read_file(url)
            self.multi_url(url)
        
    def single_url(self, url, file_format):
        """
        converting url with conv_url() function 
        then show progress in progress bar to user
        """

        if self.is_link_valid(url):
            try:
                compared_url = self.conv_url(url, file_format)
            except:
                print("failed to create download link")
                exit(1)
        
        with tqdm(total=(1000), ncols=100) as stat_bar:
            old_stat = 0
            while True: 
                download_url = get(compared_url).json()
                stat = download_url["progress"]
                text = download_url["text"]
                stat_bar.set_description("convert to direct link : {}".format(text))
                
                if download_url["success"] == 1:
                    stat_bar.total = stat_bar.n
                    break
                if old_stat != stat:
                        stat_bar.update(stat)
        urls.append(download_url["download_url"])
    
    def read_file(self):
        pass

    def write_single_file(self, file_format, filename=''):
        if file_format in ("360", "480", "720", "1080") or not file_format:
            file_format = "mp4"
        if not filename:
            filename = self.filename
        filename = filename.replace(" ", "_")
       
        try:
            downloading = litdm(url=urls[0], filename=filename)
            downloading.start_threads()
            rename(filename, (filename + "." + file_format))
        except:
            print("Download failed, no response from source")
            exit(1)

    def conv_url(self, url, file_format):
        """
        convert youtube url to downloadable file link
        """
        if not file_format:
            file_format = self.fileformat
        if not file_format in ("360", "480", "720", "1080", "mp3", "m4a", "webm", "wav", "ogg", "flac", "opus"):
            print("wrong file format, you should pass one of valid formats to the -F option")
            print("valid formats: 360, 480, 720, 1080, mp3, m4a, webm, wav, ogg, flac, opus")
            exit(1)

        compare_url = f"https://loader.to/ajax/download.php?format={file_format}&url={url}"
        req = get(compare_url).json()
        _id  = req["id"]
        if not self.filename:
            self.filename = req["title"] 
         
        compare_id_link = f"https://p.oceansaver.in/ajax/progress.php?id={_id}"
        return compare_id_link

    def is_link_valid(self, link):
        check = compile(r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})$')
        return bool(check.match(link))

if __name__ == "__main__":
    arguments = handle_args()

    if arguments.no_arg_passed() or not arguments.argv.url:
        arguments.help_page()
    
    youtube = ytdown(arguments.argv.url, "url",
                     arguments.argv.format, arguments.argv.filename)
    youtube.write_single_file(arguments.argv.format)


