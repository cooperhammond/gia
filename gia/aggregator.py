import os
import sys
import time
import subprocess
import platform
from urllib.parse import urlencode
from urllib.request import urlretrieve
import multiprocessing
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


CHROME_DRIVER_LOC = os.environ.get("CHROME_DRIVER_LOC")
IMAGE_URLS_SCRIPT = \
    "urls=Array.from(document.querySelectorAll('.rg_i')).map(el=> el.hasAttribute('data-src')?el.getAttribute('data-src'):el.getAttribute('data-iurl'));" + \
    "\n" + "window.open('data:text/csv;charset=utf-8,' + escape(urls.join('\\n')));"
ON_WSL = "microsoft" in platform.uname()[3].lower()


class ImageAggregator:

    def __init__(self, destination, classes, query_sets, default_depth=0, max_workers=8):
        self.sys_destination = Path(destination)
        self.python_dest = self.sys_destination

        self.max_workers = max_workers
        self.classes = classes

        if ON_WSL:
            self.python_dest = Path(
                subprocess.check_output(
                    'wslpath "%s"' % self.sys_destination, 
                    shell=True
                ).decode('utf-8').strip("\n"))

        gimages_url = 'https://www.google.com/search?tbm=isch&'
        self.query_sets = []
        for index, query_set in enumerate(query_sets):
            for i, query in enumerate(query_set):
                query_str = query
                query_depth = default_depth
                if type(query) == list:
                    query_str = query[0]
                    query_depth = query[1]

                url = gimages_url + urlencode({'q': query_str})
                query_set[i] = [url, query_depth]

                
            self.query_sets.append(query_set)

    def grab_urls(self):
        # automatically download files to the specified folder
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('prefs', {
            'download.default_directory' : str(self.sys_destination)
        })

        if ON_WSL:
            # spawns chromedriver instance safely on WSL
            os.system('cmd.exe /c "%s" &' % CHROME_DRIVER_LOC)
        else:
            os.system(CHROME_DRIVER_LOC)

        # default port (always used) for chromedriver is 9515
        driver = webdriver.Chrome(port=9515, options=opts)

        for index, query_set in enumerate(self.query_sets):

            for query in query_set:
                url = query[0]
                depth = query[1]

                # open up url
                driver.get(url)
                
                # this loop will scroll down the page and force more images to load.
                # usually can grab ~350 images compared to the 80 grabbed from not scrolling
                for i in range(0, depth):
                    html = driver.find_element_by_tag_name('html')
                    html.send_keys(Keys.END)
                    time.sleep(2)

                # download image urls
                driver.execute_script(IMAGE_URLS_SCRIPT)

                # following snippet will rename the downloaded urls from "download" to 
                # <corresponding-class>.csv
                current_filename = self.python_dest/'download'
                target_filename = self.python_dest/(self.classes[index] + '.csv')
                # if a target class has already downloaded a url set, append
                # the urls to the last file
                if os.path.exists(target_filename):
                    while not os.path.exists(current_filename):
                        time.sleep(0.1)
                    file_in = open(current_filename, 'r')
                    file_out = open(target_filename, 'a')
                    for line in file_in:
                        file_out.write(line)
                    file_out.close()
                    os.remove(current_filename)
                else:
                    while not os.path.exists(str(current_filename)):
                        time.sleep(0.1)
                    os.rename(current_filename, target_filename)

        time.sleep(2)
        driver.quit()

    def grab_images(self):
        for c in self.classes:
            print('downloading images for class "%s"' % c)
            image_dest = Path(self.python_dest/c)
            image_dest.mkdir(parents=True, exist_ok=True)
            self.download_images(self.python_dest/(c + '.csv'), image_dest)
            # verify_images(Path(self.python_dest/c), delete=True, max_size=1000)

    def download_images(self, filename, destination):
        f = open(filename, 'r')
        lines = f.read().split("\n")
        f.close()
        urls = [url for url in lines if url != ""]
        tasks = []

        queue = multiprocessing.Manager().Queue()

        max = len(str(len(urls)))
        for index, url in enumerate(urls):
            filename = destination / ("00" + ("0" * (max - len(str(index)))) + str(index) + ".jpg")
            tasks.append((url, filename, queue)) 

        pool = multiprocessing.Pool(self.max_workers)
        download_map = pool.map_async(self.dl, tasks)

        downloaded = 0
        while not download_map.ready():
            for _ in range(queue.qsize()):
                downloaded += queue.get()

            i = downloaded
            n = len(tasks)
            j = (i + 1) / n
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%% %s/%s" % ('='*int(20*j), 100*j, i, n))
            sys.stdout.flush()
        print("")

    def dl(self, pair):
        urlretrieve(pair[0], pair[1])
        pair[2].put(1)

    def aggregate(self):
        self.grab_urls()
        self.grab_images()