#! /bin/python3

from tqdm import tqdm
from requests import get
from argparse import ArgumentParser
global urls
urls = list()

class handle_args:
    def __init__(self):
        self.parse = ArgumentParser(description="download single/multiple media from youtube")
        self.parse.add_argument("-f", "--file", help="file with multiple url separated with newline")
        self.parse.add_argument("-u", "--url", help="single url to download media")
        self.parse.add_argument("-o", "--output", help="file path and file name")
        self.argv = self.parse.parse_args()

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
    def __init__(self, content, _type):
      #  self.urls = []

        if _type == "url":
            self.single_url(content)
        if _type == "output":
            if len(urls) != 0 :
                self.write_single_file(content)
        elif _type == "file":
            file_content = read_file(content)
            self.multi_url(content)
        
    def single_url(self, url):
        """
        converting url with conv_url() function 
        then show progress in progress bar to
        user
        """
        compared_url = self.conv_url(url)
        
        with tqdm(total=(10000), ncols=100) as stat_bar:
            old_stat = 0
            while True: 
                download_url = get(compared_url).json()
                stat = download_url["progress"]
                text = download_url["text"]
                stat_bar.set_description("{}% | status : {}".format(stat, text))
                
                if download_url["success"] == 1:
                    stat_bar.total = stat_bar.n
                    break
                if old_stat != stat:
                        stat_bar.update(stat)
        urls.append(download_url["download_url"])
    
    def multi_url(self, urls):
        pass 

    def read_file(self):
        pass

    def write_single_file(self, filename):
        """
        write to single file my postfix
        mp3 for now . other formats not 
        supported yet!
        """
        file_content = get(urls[0]).content
        with open(filename + ".mp3", "wb") as file:
            file.write(file_content)

    def conv_url(self, url):
        """
        convert youtube url to downloadable file link
        note : using y2down.cc api
        """
        compare_url = f"https://loader.to/ajax/download.php?format=mp3&url={url}"
        _id  = get(compare_url).json()["id"]
        compare_id_link = f"https://p.oceansaver.in/ajax/progress.php?id={_id}"
        return compare_id_link

if __name__ == "__main__":
    arguments = handle_args()

    if arguments.no_arg_passed():
        arguments.help_page()
    
    if arguments.argv.file != None:
        youtube = ytdown(arguments.argv.file, "file")
    elif arguments.argv.url != None:
        youtube = ytdown(arguments.argv.url, "url")
    
    if arguments.argv.output != None:
        print(f"make {arguments.argv.output}.mp3 file...",end='')
        ytdown(arguments.argv.output, "output")
        print("\ndone")
    else:
        for i in urls:
            print("----\ndownload link:", i)


