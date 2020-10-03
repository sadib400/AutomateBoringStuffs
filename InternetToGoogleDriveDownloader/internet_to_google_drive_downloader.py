# -*- coding: utf-8 -*-
"""Internet to google drive downloader
   Author: Muhammad Abdullah Jubayer
   email: jubayr.py@gmail.com

   Attribution: https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
    
"""

from google.colab import drive 
drive.mount('/content/gdrive')

import os
import sys
import requests

file_url = str(input("Enter your direct download link: "))

file_name = os.path.basename(file_url)


with open(f"/content/gdrive/My Drive/{file_name}", "wb") as f:
        print (f"Downloading {file_name}")

        response = requests.get(file_url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[{0}{1}]".format('=' * done,  ' ' * (50-done) ) )    
                sys.stdout.flush()

